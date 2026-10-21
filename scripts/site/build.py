"""Build costofliving.no as plain HTML from open data and the site's markdown.

  python3 scripts/site/fetch_data.py   # once a year, or when a source updates
  python3 scripts/site/build.py        # writes site/

The numbers come from data/prices.json (see fetch_data.py). The words come from
docs/: each country's index.md gives its facts, phrases and links, each city's
page its places to stay and things to do, and the guides are rendered as they
are. Price tables copied from Numbeo are left out. URLs are the ones MkDocs
made, so /norway/ and /norway/cities/oslo/ stay where Google found them.

The look is template/global.css and the .tmpl files, first drawn as the Norway
page in Peak's Site Builder.
"""
import html
import json
import re
import shutil
import statistics
import sys
from urllib.parse import quote
from datetime import date
from pathlib import Path
from string import Template

import markdown

sys.path.insert(0, str(Path(__file__).parent))
from countries import CATEGORIES, OVERALL, REGIONS, region_of  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"
OUT = ROOT / "site"
TEMPLATES = Path(__file__).parent / "template"
SITE = "https://costofliving.no"

DATA = json.loads((ROOT / "data" / "prices.json").read_text())
COUNTRIES = DATA["countries"]

# The closest guide for a country no source publishes a price level for.
STAND_IN = {"monaco": "france", "liechtenstein": "switzerland", "vatican": "italy"}

SOURCES = {
    "eurostat": ('<a href="https://ec.europa.eu/eurostat/databrowser/view/prc_ppp_ind_1/default/table">Eurostat, '
                 'prc_ppp_ind_1</a>: price level indices, EU27 = 100, {year}. Reuse authorised with acknowledgement.'),
    "worldbank": ('<a href="https://data.worldbank.org/indicator/PA.NUS.PRVT.PLI">World Bank, PA.NUS.PRVT.PLI</a>: '
                  'household price level, United States = 100, {year}. CC BY 4.0.'),
    "ssb": ('<a href="https://www.ssb.no/en/statbank/table/09895">Statistics Norway, table 09895</a>: rental market '
            'survey, {year}. CC BY 4.0.'),
    "ecb": ('<a href="https://data.ecb.europa.eu/data/datasets/EXR">European Central Bank</a> reference rate, {date}: '
            '1 € = {rate} {currency}.'),
}

NUMBER_WORDS = ["No", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Eleven",
                "Twelve"]


def template(name):
    return Template((TEMPLATES / name).read_text())


LAYOUT = template("layout.tmpl")
e = html.escape


# MARK: Numbers

def overall(slug):
    """A country's household price level against the EU (= 100), with where it came from and the year."""
    c = COUNTRIES.get(slug) or {}
    if c.get("eurostat") and OVERALL in c["eurostat"]:
        x = c["eurostat"][OVERALL]
        return x["pli"], "eurostat", x["year"]
    if c.get("worldbank"):
        return round(c["worldbank"]["pli_us"] / EU_ON_US * 100, 1), "worldbank", c["worldbank"]["year"]
    return None, None, None


def eu_on_us():
    """The EU's price level on the World Bank's United States = 100 scale, from every country both
    sources cover. The World Bank publishes no EU total for this indicator; the ratio is steady."""
    ratios = [c["worldbank"]["pli_us"] / c["eurostat"][OVERALL]["pli"] * 100
              for c in COUNTRIES.values() if c.get("eurostat") and OVERALL in c["eurostat"] and c.get("worldbank")]
    return statistics.median(ratios)


EU_ON_US = eu_on_us()


def pct(value):
    """'+29%' or '−8%' for a price level against 100."""
    p = round(value - 100)
    return f"+{p}%" if p > 0 else (f"−{-p}%" if p < 0 else "±0%")


def money(n):
    return f"{round(n):,}"


def words_list(items):
    items = [i.lower() for i in items]
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + " and " + items[-1]


# MARK: Markdown

FRONT = re.compile(r"\A---\n(.*?)\n---\n", re.S)


def read_md(path):
    text = path.read_text()
    meta = {}
    m = FRONT.match(text)
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
        text = text[m.end():]
    return meta, text


def clean_heading(h):
    return re.sub(r"^[^\w(]+", "", h).strip()


def sections(text):
    """[(heading, body)] split at '## '; the text before the first heading is ('', body)."""
    out, heading, body = [], "", []
    for line in text.splitlines():
        if line.startswith("## "):
            out.append((heading, "\n".join(body)))
            heading, body = clean_heading(line[3:]), []
        else:
            body.append(line)
    out.append((heading, "\n".join(body)))
    return out


def table(body):
    """The rows of the first markdown table in a section, header and rule left out."""
    rows = [line for line in body.splitlines() if line.strip().startswith("|")]
    out = []
    for line in rows[2:]:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        out.append([re.sub(r"^\*\*(.*)\*\*$", r"\1", c) for c in cells])
    return out


def url_for(path):
    """The URL MkDocs gave a page under docs/."""
    rel = path.relative_to(DOCS)
    if rel.name == "index.md":
        return "/" + (str(rel.parent) + "/" if str(rel.parent) != "." else "")
    return "/" + str(rel.with_suffix("")) + "/"


def without_numbeo(text):
    return "\n".join(line for line in text.splitlines() if "numbeo" not in line.lower())


def render_md(text, src):
    out = markdown.markdown(text, extensions=["tables"])

    def fix(m):
        target, anchor = m.group(1), m.group(2) or ""
        if re.match(r"[a-z]+:", target):
            return m.group(0)
        resolved = (src.parent / target).resolve()
        try:
            return f'href="{url_for(resolved)}{anchor}"'
        except ValueError:
            return m.group(0)

    out = re.sub(r'href="([^"#]+\.md)(#[^"]*)?"', fix, out)
    # Links out open as before; a page's own links stay in the tab.
    return re.sub(r'<a href="(https?://)', r'<a rel="noopener" href="\1', out)


def inline_md(text, src):
    return re.sub(r"^<p>(.*)</p>$", r"\1", render_md(text, src).strip(), flags=re.S)


# Links that earn a commission: Travelpayouts' redirects and referral codes.
AFFILIATE = re.compile(r"https?://(tp\.media/r\?|www\.airbnb\.com/c/|[^\"]*/referral/)")
DISCLOSURE = ('<p class="disclosure">Some links {where} are affiliate links: if you book through them, '
              "costofliving.no may earn a commission, at no extra cost to you.</p>")


def mark_affiliates(content, url):
    """rel="sponsored" on every link that earns a commission, and a note in each card or article that has one."""
    def sponsor(m):
        attrs = re.sub(r'\s*rel="[^"]*"', "", m.group(1))
        return f'<a rel="sponsored noopener"{attrs}>' if AFFILIATE.search(attrs) else m.group(0)

    content = re.sub(r"<a(\s[^>]*)>", sponsor, content)
    if url == "/affiliate/":  # the page says so in its first line
        return content
    content = re.sub(r'(<section class="card[^"]*">.*?)(\n?\s*</section>)',
                     lambda m: m.group(1) + ("\n      " + DISCLOSURE.format(where="in this section")
                                             if 'rel="sponsored' in m.group(1) else "") + m.group(2),
                     content, flags=re.S)
    if '<article class="prose">' in content and 'rel="sponsored' in content:
        content = content.replace('<article class="prose">',
                                  '<article class="prose">\n' + DISCLOSURE.format(where="on this page"), 1)
    return content


# MARK: Cards

def card(span, kicker, title, body, sub="", extra_class=""):
    sub_html = f'\n      <p class="sub">{sub}</p>' if sub else ""
    cls = f"card span-{span}" + (f" {extra_class}" if extra_class else "")
    return (f'    <section class="{cls}">\n      <div class="kicker">{kicker}</div>\n'
            f'      <h2>{title}</h2>{sub_html}\n{body}\n    </section>')


def category_card(name, cats):
    values = sorted(((label, cats[code]["pli"]) for code, label in CATEGORIES.items() if code in cats),
                    key=lambda x: -x[1])
    scale = max(210, max(v for _, v in values) + 10)
    rows = []
    for label, v in values:
        cheap = " cheap" if v < 100 else ""
        rows.append(f'        <li class="bar"><span class="bar-label">{e(label)}</span><span class="bar-track">'
                    f'<span class="bar-fill{cheap}" style="width:{v / scale * 100:.1f}%"></span>'
                    f'<span class="bar-eu" style="left:{100 / scale * 100:.1f}%"></span></span>'
                    f'<span class="bar-val{cheap}">{pct(v)}</span></li>')
    year = next(iter(cats.values()))["year"]
    body = ('      <ul class="bars">\n' + "\n".join(rows) + '\n      </ul>\n'
            f'      <div class="legend"><span><i></i>EU average</span><span>Eurostat, {year}</span></div>')
    return card(7, "Price level by category", "What costs more, and how much", body,
                f"EU average = 100. The bar's length is {e(name)}'s price level for the same basket.")


def compare_card(slug, name, span):
    me, _, _ = overall(slug)
    region = region_of(slug)
    others = [(s, overall(s)[0]) for s in REGIONS[region] if s != slug and overall(s)[0] is not None]
    above = sorted([o for o in others if o[1] >= me], key=lambda o: o[1])[:2]
    below = sorted([o for o in others if o[1] < me], key=lambda o: -o[1])[:2]
    shown = above + below + [(slug, me), ("eu", 100.0)]
    shown.sort(key=lambda o: -o[1])
    scale = max(v for _, v in shown) * 1.07
    rows = []
    for s, v in shown:
        if s == "eu":
            label, cls = "🇪🇺 EU", "row eu"
        else:
            flag, cname = PAGES[s]["flag"], PAGES[s]["name"]
            label = f'{flag} {e(cname)}' if s == slug else f'<a href="/{s}/">{flag} {e(cname)}</a>'
            cls = "row me" if s == slug else "row"
        rows.append(f'      <div class="{cls}"><span>{label}</span><span class="fill" style="width:{v / scale * 100:.1f}%">'
                    f'</span><span class="num">{round(v)}</span></div>')
    pricier = [o for o in others if o[1] > me]
    if not others:
        title = "Against the EU"
    elif not pricier:
        title = f"The priciest in {region}"
    elif len(pricier) == len(others):
        title = f"The cheapest in {region}"
    else:
        nearest = min(pricier, key=lambda o: o[1])[0]
        title = f"Cheaper than {e(PAGES[nearest]['name'])}"
    body = "\n".join(rows)
    wb = COUNTRIES[slug].get("worldbank")
    if wb:
        d = round(wb["pli_us"] - 100)
        word = f"{abs(d)}% cheaper" if d < 0 else (f"{d}% dearer" if d > 0 else "The same")
        body += (f'\n      <div class="stat"><b>{word}</b><span>than the United States for the same household '
                 f'spending (World Bank, {wb["year"]})</span></div>')
    return card(span, "Against its neighbours", title, body, "Household spending, EU average = 100.", "compare")


def rent_card(slug, only_city=None):
    rents = DATA["rents"].get(slug)
    if not rents:
        return None, []
    rate = DATA["ecb"]["per_eur"].get(rents["currency"])
    rows = [r for r in rents["rows"] if only_city is None or r["city"] in (only_city, None)]
    if only_city and not any(r["city"] == only_city for r in rows):
        return None, []
    lines = []
    for r in rows:
        sub = "national average" if r["city"] is None else ("the capital" if r["city"] == "oslo" else "")
        cells = [f'<td class="city">{e(r["place"])}' + (f"<small>{sub}</small>" if sub else "") + "</td>"]
        for n in ("1", "2", "3"):
            v = r["rooms"].get(n)
            if v is None:
                cells.append('<td class="na">—</td>')
            elif rate:
                cells.append(f'<td><b>€{money(v / rate)}</b><small>{money(v)} kr</small></td>')
            else:
                cells.append(f'<td><b>{money(v)} {rents["currency"]}</b></td>')
        lines.append("          <tr>" + "".join(cells) + "</tr>")
    body = ('      <table class="rent">\n        <thead><tr><th>Where</th><th>1 room</th><th>2 rooms</th>'
            '<th>3 rooms</th></tr></thead>\n        <tbody>\n' + "\n".join(lines) + "\n        </tbody>\n      </table>")
    if any(v is None for r in rows for v in r["rooms"].values()):
        body += '\n      <p class="sub" style="margin:12px 0 0">— too few flats of that size in the survey to give an average.</p>'
    sub = (f"Average rents in {rents['year']} from Statistics Norway's rental market survey"
           + (f", in kroner and in euros at {rate:.2f} kr per euro." if rate else "."))
    used = ["ssb"] + (["ecb"] if rate else [])
    return card(12, "Rent", "What a flat costs a month", body, sub), used


def sources_card(used, slug):
    c = COUNTRIES[slug]
    items = []
    for key in used:
        if key == "eurostat":
            items.append(SOURCES[key].format(year=c["eurostat"][OVERALL]["year"]))
        elif key == "worldbank":
            items.append(SOURCES[key].format(year=c["worldbank"]["year"]))
        elif key == "ssb":
            items.append(SOURCES[key].format(year=DATA["rents"][slug]["year"]))
        elif key == "ecb":
            cur = DATA["rents"][slug]["currency"]
            items.append(SOURCES[key].format(date=DATA["ecb"]["date"], rate=DATA["ecb"]["per_eur"][cur], currency=cur))
    if "worldbank" in used and "eurostat" not in used:
        items.append(f"Against the EU: the World Bank's level divided by the EU's on the same scale "
                     f"({EU_ON_US:.1f}, from the countries both sources cover).")
    body = "      <ol>\n" + "\n".join(f"        <li>{i}</li>" for i in items) + "\n      </ol>"
    return (f'    <section class="card span-12 sources">\n      <div class="kicker">Where the numbers come from</div>\n'
            f'{body}\n    </section>')


# MARK: Pages

PAGES = {}  # slug -> what the country's markdown says, read once


def read_country(slug):
    path = DOCS / slug / "index.md"
    meta, text = read_md(path)
    title = meta.get("title") or re.search(r"^# (.+)$", text, re.M).group(1)
    flag_match = re.match(r"^((?:[\U0001F1E6-\U0001F1FF]{2})|\S+)\s+(.+)$", title)
    flag, name = (flag_match.group(1), flag_match.group(2)) if flag_match else ("", title)
    secs = sections(without_numbeo(text))
    facts, phrases, more = [], [], []
    for heading, body in secs:
        h = heading.lower()
        if any(k in h for k in ("resident", "currency", "practical living")):
            facts += table(body)
        elif "phrases" in h:
            phrases = table(body)
        elif heading and not any(k in h for k in ("cost of living", "cities")):
            more.append((heading, body))
    cities = []
    for city_path in sorted((DOCS / slug / "cities").glob("*.md")):
        cmeta, ctext = read_md(city_path)
        ctitle = cmeta.get("title") or re.search(r"^# (.+)$", ctext, re.M).group(1)
        cname = re.sub(r"^\W+", "", ctitle).split(" - ")[0].strip()
        cities.append({"slug": city_path.stem, "name": cname, "path": city_path})
    PAGES[slug] = {"flag": flag, "name": name, "facts": facts, "phrases": phrases, "more": more,
                   "cities": cities, "path": path}


FACT_LABELS = {"Status": "Status", "Stay Rules": "Stay", "Healthcare": "Healthcare", "Currency": "Currency",
               "Digital Banking": "Banking", "Payment": "Paying", "English Level": "English",
               "Essential App": "Getting around"}


def facts_card(p):
    if not p["facts"]:
        return None
    rows = []
    for row in p["facts"]:
        if len(row) < 2:
            continue
        label = FACT_LABELS.get(row[0], row[0])
        value = row[1]
        stars = re.match(r"^(⭐+)", value)
        if stars:
            value = f"{len(stars.group(1))} out of 5"
        rows.append(f"        <div><dt>{e(label)}</dt><dd>{inline_md(value, p['path'])}</dd></div>")
    return card(4, "Living there", "The basics", '      <dl class="facts" style="margin-top:14px">\n'
                + "\n".join(rows) + "\n      </dl>")


def phrases_card(p):
    if not p["phrases"]:
        return None
    rows = "\n".join(f"        <dt>{e(a)}</dt><dd>{e(b)}</dd>" for a, b, *_ in p["phrases"] if a and b)
    return card(4, "Say it locally", f"{NUMBER_WORDS[len(p['phrases'])] if len(p['phrases']) < 13 else len(p['phrases'])} phrases",
                f'      <dl class="phrases" style="margin-top:14px">\n{rows}\n      </dl>')


def cities_card(slug, p):
    if not p["cities"]:
        return None
    n = len(p["cities"])
    count = NUMBER_WORDS[n] if n < len(NUMBER_WORDS) else str(n)
    links = "\n".join(f'        <a href="/{slug}/cities/{c["slug"]}/">{e(c["name"])}</a>' for c in p["cities"])
    return card(4, "Cities", f"{count} place{'s' if n != 1 else ''} to live",
                f'      <div class="cities" style="margin-top:14px;grid-template-columns:1fr 1fr">\n{links}\n      </div>')


def more_cards(sections_, src, span=6):
    cards = []
    for heading, body in sections_:
        if not body.strip():
            continue
        cards.append(card(span, "More", e(heading), f'      <div class="prose">{render_md(body, src)}</div>'))
    return cards


def verdict(slug, name):
    v, source, year = overall(slug)
    if v is None:
        stand_in = STAND_IN.get(slug)
        text = f"No official price level is published for {e(name)}."
        if stand_in:
            text += f' <a href="/{stand_in}/">{e(PAGES[stand_in]["name"])}</a> is the closest guide.'
        return "—", "none", text
    p = round(v - 100)
    if p == 0:
        return "±0%", "", f"Everyday spending in {e(name)} costs about the same as the EU average."
    more = "more" if p > 0 else "less"
    return pct(v), ("cheap" if p < 0 else ""), f"Everyday spending in {e(name)} costs {abs(p)}% {more} than the EU average."


def country_lede(slug, name):
    cats = COUNTRIES[slug].get("eurostat") or {}
    values = sorted(((CATEGORIES[c], cats[c]["pli"]) for c in CATEGORIES if c in cats), key=lambda x: -x[1])
    parts = []
    if values:
        top = [l for l, _ in values[:3]]
        bottom = [l for l, _ in values[-3:]][::-1]
        parts.append(f"{words_list(top).capitalize()} cost the most compared with the rest of Europe; "
                     f"{words_list(bottom)} the least.")
    elif overall(slug)[0] is not None:
        parts.append(f"Eurostat publishes no breakdown by category for {name}, so this is the World Bank's "
                     f"overall household price level, set against the EU.")
    elif slug in STAND_IN:
        parts.append(f"Neither Eurostat nor the World Bank covers {name}. The nearest country they do is "
                     f"{PAGES[STAND_IN[slug]]['name']}, whose page has prices by category.")
    rents = DATA["rents"].get(slug)
    if rents:
        rate = DATA["ecb"]["per_eur"].get(rents["currency"])
        all_v = [(r, n, r["rooms"][n]) for r in rents["rows"] for n in ("1", "3") if r["rooms"].get(n)]
        low = min(all_v, key=lambda x: x[2])
        high = max(all_v, key=lambda x: x[2])
        def eur(x):
            return f"€{money(round(x[2] / rate, -1))}" if rate else f"{money(x[2])} {rents['currency']}"
        def where(x):
            return "nationally" if x[0]["city"] is None else "in " + x[0]["place"].split(" &")[0]
        parts.append(f"Rents run from about {eur(low)} a month for {'one room' if low[1] == '1' else 'three rooms'} "
                     f"{where(low)} to {eur(high)} for {'three rooms' if high[1] == '3' else 'one room'} {where(high)}.")
    return " ".join(parts)


def page(title, description, url, content):
    return LAYOUT.substitute(title=e(title), description=e(description), canonical=SITE + quote(url),
                             content=mark_affiliates(content, url),
                             year=date.today().year)


def write(url, text):
    path = OUT / url.strip("/") / "index.html" if url != "/" else OUT / "index.html"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    BUILT.append(url)


BUILT = []


def build_country(slug):
    p = PAGES[slug]
    name = p["name"]
    v, source, year = overall(slug)
    num, cls, text = verdict(slug, name)
    used, cards = [], []
    cats = COUNTRIES[slug].get("eurostat") or {}
    has_categories = any(c in cats for c in CATEGORIES)
    if has_categories:
        cards.append(category_card(name, cats))
        used.append("eurostat")
    if v is not None:
        cards.append(compare_card(slug, name, 5 if has_categories else 12))
        if COUNTRIES[slug].get("worldbank"):
            used.append("worldbank")
    rent, rent_sources = rent_card(slug)
    if rent:
        cards.append(rent)
        used += rent_sources
    small = [c for c in (facts_card(p), phrases_card(p), cities_card(slug, p)) if c]
    if len(small) == 2:
        small = [c.replace("span-4", "span-6", 1) for c in small]
    cards += small
    cards += more_cards(p["more"], p["path"])
    if used:
        cards.append(sources_card(list(dict.fromkeys(used)), slug))
    content = template("country.tmpl").substitute(
        region=e(region_of(slug)), year_label=f"{year} price levels" if year else "price levels",
        flag=p["flag"], name=e(name), verdict_num=num, verdict_class=cls, verdict_text=text,
        lede=e(country_lede(slug, name)), cards="\n\n".join(cards))
    if v is not None:
        gap = round(v - 100)
        title = (f"Cost of living in {name} {year}: {abs(gap)}% {'above' if gap > 0 else 'below'} the EU average"
                 if gap else f"Cost of living in {name} {year}: level with the EU average")
        desc = (f"How {name}'s prices compare with the EU average, category by category, and with its neighbours. "
                f"Open data from Eurostat and the World Bank" + (", with rents from Statistics Norway." if rent else "."))
    else:
        title = f"Cost of living in {name}"
        desc = f"Living in {name}: the basics, its cities and useful links."
    write(f"/{slug}/", page(title, desc, f"/{slug}/", content))


def build_city(slug, city):
    p = PAGES[slug]
    meta, text = read_md(city["path"])
    text = without_numbeo(text)
    secs = [(h, b) for h, b in sections(text) if h and not any(k in h.lower() for k in ("cost of living", "back"))]
    num, cls, vtext = verdict(slug, p["name"])
    v = overall(slug)[0]
    if v is not None:
        vtext = (f"{e(city['name'])} is in {e(p['name'])}, where everyday spending costs "
                 f"{abs(round(v - 100))}% {'more' if v >= 100 else 'less'} than the EU average.")
    used, cards = [], []
    rent, rent_sources = rent_card(slug, only_city=city["slug"])
    lede = f'Prices by category, neighbours and sources are on the <a href="/{slug}/">{e(p["name"])} page</a>.'
    if rent:
        cards.append(rent)
        used += rent_sources
        lede = (f"Rents below are {e(city['name'])}'s own, from Statistics Norway; everything else is "
                f"{e(p['name'])}'s, on the <a href=\"/{slug}/\">{e(p['name'])} page</a>.")
    cards += more_cards(secs, city["path"])
    others = [c for c in p["cities"] if c["slug"] != city["slug"]]
    if others:
        links = "\n".join(f'        <a href="/{slug}/cities/{c["slug"]}/">{e(c["name"])}</a>' for c in others)
        cards.append(card(12, "Cities", f"More of {e(p['name'])}",
                          f'      <div class="cities" style="margin-top:14px">\n        <a href="/{slug}/">'
                          f'{p["flag"]} {e(p["name"])} <span>overview</span></a>\n{links}\n      </div>'))
    if overall(slug)[0] is not None:
        used.insert(0, overall(slug)[1])
    if used:
        cards.append(sources_card(list(dict.fromkeys(used)), slug))
    # The old pages embedded Google Maps' legacy iframe, which Google no longer serves.
    osm = "https://www.openstreetmap.org/search?query=" + quote(f"{city['name']}, {p['name']}")
    lede += f' <a href="{osm}" rel="noopener">See {e(city["name"])} on the map ↗</a>'
    content = template("city.tmpl").substitute(
        country_url=f"/{slug}/", country=f'{p["flag"]} {e(p["name"])}', region=e(region_of(slug)),
        name=e(city["name"]), verdict_num=num, verdict_class=cls, verdict_text=vtext,
        lede=lede, cards="\n\n".join(cards))
    url = f"/{slug}/cities/{city['slug']}/"
    title = f"Cost of living in {city['name']}, {p['name']}"
    desc = (f"Living in {city['name']}: " + (f"rents from Statistics Norway, " if rent else "")
            + f"places to stay, things to do and how {p['name']} compares with the EU.")
    write(url, page(title, desc, url, content))


def build_home():
    ranked = sorted(((s, overall(s)[0]) for s in COUNTRIES if overall(s)[0] is not None), key=lambda x: x[1])
    scale = max(v for _, v in ranked) * 1.05
    rows = []
    for s, v in ranked:
        cheap = " cheap" if v < 100 else ""
        src = "" if overall(s)[1] == "eurostat" else "<small>World Bank</small>"
        rows.append(f'      <div class="row"><span><a href="/{s}/">{PAGES[s]["flag"]} {e(PAGES[s]["name"])}</a>{src}</span>'
                    f'<span class="bar-track"><span class="bar-fill{cheap}" style="width:{v / scale * 100:.1f}%"></span>'
                    f'<span class="bar-eu" style="left:{100 / scale * 100:.1f}%"></span></span>'
                    f'<span class="bar-val{cheap}">{pct(v)}</span></div>')
    missing = [s for s in COUNTRIES if overall(s)[0] is None]
    no_data = ""
    if missing:
        links = ", ".join(f'<a href="/{s}/">{e(PAGES[s]["name"])}</a>' for s in missing)
        no_data = f'<p class="sub" style="margin:14px 0 0">No official price level is published for {links}.</p>'
    regions = []
    for region, slugs in REGIONS.items():
        links = []
        for s in slugs:
            v = overall(s)[0]
            tag = "" if v is None else f'<span class="{"cheap" if v < 100 else "dear"}">{pct(v)}</span>'
            links.append(f'<a href="/{s}/">{PAGES[s]["flag"]} {e(PAGES[s]["name"])} {tag}</a>')
        regions.append(f'        <div><h3>{e(region)}</h3><div class="cities" style="grid-template-columns:1fr">'
                       + "".join(links) + "</div></div>")
    guides = "\n".join(f'        <a href="{url}">{e(title)}</a>' for url, title in ARTICLE_TITLES)
    years = sorted({overall(s)[2] for s, _ in ranked})
    content = template("home.tmpl").substitute(
        year_label=f"{years[-1]} price levels", count=len(COUNTRIES), rank_rows="\n".join(rows), no_data=no_data,
        regions="\n".join(regions), guides=guides)
    write("/", page("Cost of living in Europe: every country against the EU average",
                    f"How expensive {len(COUNTRIES)} European countries are compared with the EU average, by category, "
                    "with rents and city guides. Open data from Eurostat and the World Bank.", "/", content))


ARTICLE_TITLES = []


def build_articles():
    country_dirs = set(COUNTRIES)
    for path in sorted(DOCS.rglob("*.md")):
        rel = path.relative_to(DOCS)
        if rel.parts[0] in country_dirs or rel.parts[0].startswith("_") or rel == Path("index.md"):
            continue
        meta, text = read_md(path)
        text = without_numbeo(text)
        h1 = re.search(r"^# (.+)$", text, re.M)
        title = meta.get("title") or (h1.group(1) if h1 else rel.stem)
        clean = clean_heading(title)
        url = url_for(path)
        ARTICLE_TITLES.append((url, clean))
        body = render_md(text, path)
        write(url, page(f"{clean} | Cost of Living", meta.get("description", clean), url,
                        template("article.tmpl").substitute(body=body)))


def build_about():
    body = f"""<h1>About the data</h1>
<p>Every number on this site comes from open data that anyone may reuse, and each page says which.</p>
<h2>Price levels</h2>
<p><a href="https://ec.europa.eu/eurostat/databrowser/view/prc_ppp_ind_1/default/table">Eurostat's price level
indices</a> compare what the same basket of goods and services costs in each country, with the EU average set to
100. A country at 129 is 29% dearer than the EU average for that basket; one at 92 is 8% cheaper. Eurostat
publishes them yearly for the EU, the EEA, Switzerland, the United Kingdom and the candidate countries, broken
down by category. Reuse is authorised provided the source is acknowledged.</p>
<p>For countries Eurostat does not cover, the overall level comes from the
<a href="https://data.worldbank.org/indicator/PA.NUS.PRVT.PLI">World Bank</a> (CC BY 4.0), which sets the United
States to 100. It is moved onto the EU scale by dividing by the EU's level on the same scale, {EU_ON_US:.1f},
worked out from the countries both sources cover. Those pages have no breakdown by category.</p>
<h2>Rents</h2>
<p>Rents come from national statistics offices, one country at a time, starting with
<a href="https://www.ssb.no/en/statbank/table/09895">Statistics Norway's rental market survey</a> (CC BY 4.0).
Countries without one show price levels only.</p>
<h2>Exchange rates</h2>
<p>Kroner and other currencies are converted with the
<a href="https://data.ecb.europa.eu/data/datasets/EXR">European Central Bank's reference rates</a>, last read on
{DATA["ecb"]["date"]}.</p>
<h2>Updates</h2>
<p>The data was last fetched on {DATA["fetched"]}. Eurostat and the World Bank publish once a year.</p>"""
    write("/about/", page("About the data | Cost of Living",
                          "Where the numbers on costofliving.no come from: Eurostat, the World Bank, Statistics Norway "
                          "and the ECB.", "/about/", template("article.tmpl").substitute(body=body)))


def build_extras():
    shutil.copy(TEMPLATES / "global.css", OUT / "global.css")
    shutil.copytree(DOCS / "assets", OUT / "assets", dirs_exist_ok=True)
    if (DOCS / "CNAME").exists():
        shutil.copy(DOCS / "CNAME", OUT / "CNAME")
    (OUT / "404.html").write_text(page("Not found | Cost of Living", "This page does not exist.", "/404.html",
                                       template("article.tmpl").substitute(
                                           body='<h1>Not found</h1><p>That page is not here. '
                                                '<a href="/">Every country</a> is one tap away.</p>')))
    today = DATA["fetched"]
    urls = "\n".join(f"  <url><loc>{SITE}{quote(u)}</loc><lastmod>{today}</lastmod></url>" for u in BUILT)
    (OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n'
                                     '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                                     f"{urls}\n</urlset>\n")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    for slug in COUNTRIES:
        read_country(slug)
    build_articles()
    for slug in COUNTRIES:
        build_country(slug)
        for city in PAGES[slug]["cities"]:
            build_city(slug, city)
    build_home()
    build_about()
    build_extras()
    print(f"{OUT}: {len(BUILT)} pages, EU on the World Bank scale {EU_ON_US:.1f}")


if __name__ == "__main__":
    main()
