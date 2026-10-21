"""Every country on the site: its URL slug, region, and the codes each data
source knows it by (Eurostat geo, World Bank ISO3, ISO 4217 currency)."""

REGIONS = {
    "Northern Europe": ["norway", "sweden", "denmark", "finland", "estonia", "iceland", "latvia", "lithuania"],
    "Eastern Europe": ["poland", "czech", "hungary", "romania", "serbia", "bulgaria", "belarus", "moldova",
                       "ukraine", "russia", "kazakhstan"],
    "Southern Europe": ["spain", "portugal", "italy", "greece", "croatia", "malta", "albania", "andorra", "bosnia",
                        "cyprus", "montenegro", "north-macedonia", "san-marino", "turkey", "vatican"],
    "Central Europe": ["germany", "austria", "switzerland", "slovakia", "slovenia", "liechtenstein"],
    "Western Europe": ["uk", "ireland", "netherlands", "belgium", "france", "luxembourg", "monaco"],
    "Caucasus": ["georgia", "armenia", "azerbaijan"],
}

# slug: (Eurostat geo, World Bank ISO3, currency)
CODES = {
    "norway": ("NO", "NOR", "NOK"), "sweden": ("SE", "SWE", "SEK"), "denmark": ("DK", "DNK", "DKK"),
    "finland": ("FI", "FIN", "EUR"), "estonia": ("EE", "EST", "EUR"), "iceland": ("IS", "ISL", "ISK"),
    "latvia": ("LV", "LVA", "EUR"), "lithuania": ("LT", "LTU", "EUR"),
    "poland": ("PL", "POL", "PLN"), "czech": ("CZ", "CZE", "CZK"), "hungary": ("HU", "HUN", "HUF"),
    "romania": ("RO", "ROU", "RON"), "serbia": ("RS", "SRB", "RSD"), "bulgaria": ("BG", "BGR", "EUR"),
    "belarus": ("BY", "BLR", "BYN"), "moldova": ("MD", "MDA", "MDL"), "ukraine": ("UA", "UKR", "UAH"),
    "russia": ("RU", "RUS", "RUB"), "kazakhstan": ("KZ", "KAZ", "KZT"),
    "spain": ("ES", "ESP", "EUR"), "portugal": ("PT", "PRT", "EUR"), "italy": ("IT", "ITA", "EUR"),
    "greece": ("EL", "GRC", "EUR"), "croatia": ("HR", "HRV", "EUR"), "malta": ("MT", "MLT", "EUR"),
    "albania": ("AL", "ALB", "ALL"), "andorra": ("AD", "AND", "EUR"), "bosnia": ("BA", "BIH", "BAM"),
    "cyprus": ("CY", "CYP", "EUR"), "montenegro": ("ME", "MNE", "EUR"), "north-macedonia": ("MK", "MKD", "MKD"),
    "san-marino": ("SM", "SMR", "EUR"), "turkey": ("TR", "TUR", "TRY"), "vatican": ("VA", None, "EUR"),
    "germany": ("DE", "DEU", "EUR"), "austria": ("AT", "AUT", "EUR"), "switzerland": ("CH", "CHE", "CHF"),
    "slovakia": ("SK", "SVK", "EUR"), "slovenia": ("SI", "SVN", "EUR"), "liechtenstein": ("LI", "LIE", "CHF"),
    "uk": ("UK", "GBR", "GBP"), "ireland": ("IE", "IRL", "EUR"), "netherlands": ("NL", "NLD", "EUR"),
    "belgium": ("BE", "BEL", "EUR"), "france": ("FR", "FRA", "EUR"), "luxembourg": ("LU", "LUX", "EUR"),
    "monaco": ("MC", "MCO", "EUR"),
    "georgia": ("GE", "GEO", "GEL"), "armenia": ("AM", "ARM", "AMD"), "azerbaijan": ("AZ", "AZE", "AZN"),
}

# Eurostat COICOP 2018 categories shown on a country page, in the words a reader uses.
CATEGORIES = {
    "A0101": "Food & soft drinks",
    "A0102": "Alcohol & tobacco",
    "A0103": "Clothing & shoes",
    "A0104": "Housing & utilities",
    "A0105": "Furniture & household",
    "A0106": "Health",
    "A0107": "Transport",
    "A0108": "Phone & internet",
    "A0109": "Recreation & culture",
    "A0111": "Restaurants & hotels",
    "A0112": "Personal care & services",
}
OVERALL = "E011"  # household final consumption expenditure

def region_of(slug):
    return next(r for r, slugs in REGIONS.items() if slug in slugs)

ALL = [s for slugs in REGIONS.values() for s in slugs]
assert set(ALL) == set(CODES), set(ALL) ^ set(CODES)
