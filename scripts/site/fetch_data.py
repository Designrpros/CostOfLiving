"""Fetch open price data for every country into data/prices.json.

Sources, all free to reuse with credit:
  Eurostat prc_ppp_ind_1   price level indices by category, EU27 = 100
  World Bank PA.NUS.PRVT.PLI  household price level, United States = 100
  ECB EXR                  euro reference rates
  Statistics Norway 09895  average rents by city and rooms

Run yearly (Eurostat and the World Bank publish once a year):
  python3 scripts/site/fetch_data.py
"""
import json
import sys
import urllib.request
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from countries import CODES, CATEGORIES, OVERALL  # noqa: E402

OUT = Path(__file__).resolve().parents[2] / "data" / "prices.json"


def get_json(url, body=None):
    request = urllib.request.Request(url, data=json.dumps(body).encode() if body else None,
                                     headers={"Content-Type": "application/json", "User-Agent": "costofliving.no data sync"})
    with urllib.request.urlopen(request, timeout=90) as response:
        return json.load(response)


def jsonstat_rows(d):
    """Yield ({dimension: category}, value) for every cell of a JSON-stat 2.0 dataset."""
    dims = d["id"]
    keys = [sorted(d["dimension"][k]["category"]["index"], key=d["dimension"][k]["category"]["index"].get) for k in dims]
    sizes = d["size"]
    for flat, value in d["value"].items() if isinstance(d["value"], dict) else enumerate(d["value"]):
        if value is None:
            continue
        i, cell = int(flat), {}
        for k, size, cats in reversed(list(zip(dims, sizes, keys))):
            cell[k] = cats[i % size]
            i //= size
        yield cell, value


def eurostat():
    url = ("https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/prc_ppp_ind_1"
           "?indic_ppp=PLI_EU27_2020&sinceTimePeriod=2023&lang=EN&" +
           "&".join(f"ppp_cat18={c}" for c in [OVERALL, *CATEGORIES]))
    d = get_json(url)
    latest = {}
    for cell, value in jsonstat_rows(d):
        geo, cat, year = cell["geo"], cell["ppp_cat18"], int(cell["time"])
        slot = latest.setdefault(geo, {})
        if cat not in slot or slot[cat][0] < year:
            slot[cat] = (year, round(value, 1))
    return {"updated": d.get("updated"), "by_geo": latest}


def world_bank():
    url = ("https://api.worldbank.org/v2/country/all/indicator/PA.NUS.PRVT.PLI"
           "?format=json&per_page=20000&date=2020:2026")
    meta, rows = get_json(url)
    latest = {}
    for r in rows:
        if r["value"] is None:
            continue
        iso3, year = r["countryiso3code"], int(r["date"])
        if iso3 not in latest or latest[iso3][0] < year:
            latest[iso3] = (year, round(r["value"], 1))
    return {"updated": meta.get("lastupdated"), "by_iso3": latest}


def ecb_rates():
    d = get_json("https://data-api.ecb.europa.eu/service/data/EXR/D..EUR.SP00.A?lastNObservations=1&format=jsondata")
    series_dims = d["structure"]["dimensions"]["series"]
    currencies = next(x for x in series_dims if x["id"] == "CURRENCY")["values"]
    cur_pos = [x["id"] for x in series_dims].index("CURRENCY")
    days = d["structure"]["dimensions"]["observation"][0]["values"]
    rates, day = {}, None
    for key, series in d["dataSets"][0]["series"].items():
        obs_key, obs = next(iter(series["observations"].items()))
        rates[currencies[int(key.split(":")[cur_pos])]["id"]] = obs[0]
        day = days[int(obs_key)]["id"]
    return {"date": day, "per_eur": rates}


def ssb_rents():
    """Statistics Norway, average monthly rent by price zone and rooms, latest year."""
    zones = {"00": ("All of Norway", None), "01": ("Oslo & Bærum", "oslo"), "03": ("Bergen", "bergen"),
             "04": ("Trondheim", "trondheim"), "05": ("Stavanger", "stavanger")}
    d = get_json("https://data.ssb.no/api/v0/en/table/09895", {
        "query": [{"code": "Soner2", "selection": {"filter": "item", "values": list(zones)}},
                  {"code": "AntRom", "selection": {"filter": "item", "values": ["1", "2", "3"]}},
                  {"code": "ContentsCode", "selection": {"filter": "item", "values": ["Husleie"]}},
                  {"code": "Tid", "selection": {"filter": "top", "values": ["1"]}}],
        "response": {"format": "json-stat2"}})
    table, year = {}, None
    for cell, value in jsonstat_rows(d):
        table.setdefault(cell["Soner2"], {})[cell["AntRom"]] = value
        year = int(cell["Tid"])
    rows = [{"place": name, "city": city, "rooms": {r: table.get(z, {}).get(r) for r in ("1", "2", "3")}}
            for z, (name, city) in zones.items()]
    rows.append(rows.pop(0))  # the national average last
    return {"norway": {"source": "ssb", "year": year, "currency": "NOK", "rows": rows}}


def main():
    euro, wb = eurostat(), world_bank()
    countries = {}
    for slug, (geo, iso3, currency) in CODES.items():
        e = euro["by_geo"].get(geo, {})
        countries[slug] = {
            "geo": geo, "iso3": iso3, "currency": currency,
            "eurostat": {cat: {"year": y, "pli": v} for cat, (y, v) in e.items()} or None,
            "worldbank": ({"year": wb["by_iso3"][iso3][0], "pli_us": wb["by_iso3"][iso3][1]}
                          if iso3 in wb["by_iso3"] else None),
        }
    eu_wb = wb["by_iso3"].get("EUU")
    data = {
        "fetched": date.today().isoformat(),
        "eurostat_updated": euro["updated"],
        "worldbank_updated": wb["updated"],
        "worldbank_eu": {"year": eu_wb[0], "pli_us": eu_wb[1]} if eu_wb else None,
        "ecb": ecb_rates(),
        "rents": ssb_rents(),
        "countries": countries,
    }
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n")
    have_e = sum(1 for c in countries.values() if c["eurostat"])
    have_w = sum(1 for c in countries.values() if c["worldbank"])
    none = [s for s, c in countries.items() if not c["eurostat"] and not c["worldbank"]]
    print(f"{OUT}: Eurostat {have_e}, World Bank {have_w}, neither {none}")


if __name__ == "__main__":
    main()
