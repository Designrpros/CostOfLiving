---
title: 🪙 Cost of Living in Europe
description: Compare cost of living across 50 European countries
---

# 🪙 Cost of Living in Europe

*Your complete guide to cost of living in Europe*

<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<style>
    #map { 
        height: 500px; 
        width: 100%; 
        border-radius: 12px; 
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        z-index: 1;
    }
</style>

<div id="map"></div>

<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script>
    var map = L.map('map').setView([48.0, 15.0], 4);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);

    L.marker([41.15, 20.17]).addTo(map).bindPopup("<b>Albania</b><br><a href='albania/'>View Guide</a>");
    L.marker([42.50, 1.52]).addTo(map).bindPopup("<b>Andorra</b><br><a href='andorra/'>View Guide</a>");
    L.marker([40.07, 45.04]).addTo(map).bindPopup("<b>Armenia</b><br><a href='armenia/'>View Guide</a>");
    L.marker([47.52, 14.55]).addTo(map).bindPopup("<b>Austria</b><br><a href='austria/'>View Guide</a>");
    L.marker([40.14, 47.57]).addTo(map).bindPopup("<b>Azerbaijan</b><br><a href='azerbaijan/'>View Guide</a>");
    L.marker([53.71, 27.95]).addTo(map).bindPopup("<b>Belarus</b><br><a href='belarus/'>View Guide</a>");
    L.marker([50.50, 4.47]).addTo(map).bindPopup("<b>Belgium</b><br><a href='belgium/'>View Guide</a>");
    L.marker([43.91, 17.67]).addTo(map).bindPopup("<b>Bosnia</b><br><a href='bosnia/'>View Guide</a>");
    L.marker([42.73, 25.48]).addTo(map).bindPopup("<b>Bulgaria</b><br><a href='bulgaria/'>View Guide</a>");
    L.marker([45.10, 15.20]).addTo(map).bindPopup("<b>Croatia</b><br><a href='croatia/'>View Guide</a>");
    L.marker([35.12, 33.42]).addTo(map).bindPopup("<b>Cyprus</b><br><a href='cyprus/'>View Guide</a>");
    L.marker([49.81, 15.47]).addTo(map).bindPopup("<b>Czechia</b><br><a href='czech/'>View Guide</a>");
    L.marker([56.26, 9.50]).addTo(map).bindPopup("<b>Denmark</b><br><a href='denmark/'>View Guide</a>");
    L.marker([58.59, 25.01]).addTo(map).bindPopup("<b>Estonia</b><br><a href='estonia/'>View Guide</a>");
    L.marker([61.92, 25.74]).addTo(map).bindPopup("<b>Finland</b><br><a href='finland/'>View Guide</a>");
    L.marker([46.22, 2.21]).addTo(map).bindPopup("<b>France</b><br><a href='france/'>View Guide</a>");
    L.marker([42.31, 43.35]).addTo(map).bindPopup("<b>Georgia</b><br><a href='georgia/'>View Guide</a>");
    L.marker([51.16, 10.45]).addTo(map).bindPopup("<b>Germany</b><br><a href='germany/'>View Guide</a>");
    L.marker([39.07, 21.82]).addTo(map).bindPopup("<b>Greece</b><br><a href='greece/'>View Guide</a>");
    L.marker([47.16, 19.50]).addTo(map).bindPopup("<b>Hungary</b><br><a href='hungary/'>View Guide</a>");
    L.marker([64.96, -19.02]).addTo(map).bindPopup("<b>Iceland</b><br><a href='iceland/'>View Guide</a>");
    L.marker([53.41, -8.24]).addTo(map).bindPopup("<b>Ireland</b><br><a href='ireland/'>View Guide</a>");
    L.marker([41.87, 12.56]).addTo(map).bindPopup("<b>Italy</b><br><a href='italy/'>View Guide</a>");
    L.marker([48.01, 66.92]).addTo(map).bindPopup("<b>Kazakhstan</b><br><a href='kazakhstan/'>View Guide</a>");
    L.marker([56.87, 24.60]).addTo(map).bindPopup("<b>Latvia</b><br><a href='latvia/'>View Guide</a>");
    L.marker([47.14, 9.52]).addTo(map).bindPopup("<b>Liechtenstein</b><br><a href='liechtenstein/'>View Guide</a>");
    L.marker([55.17, 23.88]).addTo(map).bindPopup("<b>Lithuania</b><br><a href='lithuania/'>View Guide</a>");
    L.marker([49.81, 6.12]).addTo(map).bindPopup("<b>Luxembourg</b><br><a href='luxembourg/'>View Guide</a>");
    L.marker([35.93, 14.37]).addTo(map).bindPopup("<b>Malta</b><br><a href='malta/'>View Guide</a>");
    L.marker([47.41, 28.36]).addTo(map).bindPopup("<b>Moldova</b><br><a href='moldova/'>View Guide</a>");
    L.marker([43.73, 7.42]).addTo(map).bindPopup("<b>Monaco</b><br><a href='monaco/'>View Guide</a>");
    L.marker([42.70, 19.37]).addTo(map).bindPopup("<b>Montenegro</b><br><a href='montenegro/'>View Guide</a>");
    L.marker([52.13, 5.29]).addTo(map).bindPopup("<b>Netherlands</b><br><a href='netherlands/'>View Guide</a>");
    L.marker([41.60, 21.74]).addTo(map).bindPopup("<b>North Macedonia</b><br><a href='north-macedonia/'>View Guide</a>");
    L.marker([60.47, 8.46]).addTo(map).bindPopup("<b>Norway</b><br><a href='norway/'>View Guide</a>");
    L.marker([51.91, 19.14]).addTo(map).bindPopup("<b>Poland</b><br><a href='poland/'>View Guide</a>");
    L.marker([39.39, -8.22]).addTo(map).bindPopup("<b>Portugal</b><br><a href='portugal/'>View Guide</a>");
    L.marker([45.94, 24.96]).addTo(map).bindPopup("<b>Romania</b><br><a href='romania/'>View Guide</a>");
    L.marker([55.75, 37.61]).addTo(map).bindPopup("<b>Russia</b><br><a href='russia/'>View Guide</a>");
    L.marker([43.94, 12.45]).addTo(map).bindPopup("<b>San Marino</b><br><a href='san-marino/'>View Guide</a>");
    L.marker([44.01, 21.00]).addTo(map).bindPopup("<b>Serbia</b><br><a href='serbia/'>View Guide</a>");
    L.marker([48.66, 19.69]).addTo(map).bindPopup("<b>Slovakia</b><br><a href='slovakia/'>View Guide</a>");
    L.marker([46.15, 14.99]).addTo(map).bindPopup("<b>Slovenia</b><br><a href='slovenia/'>View Guide</a>");
    L.marker([40.46, -3.74]).addTo(map).bindPopup("<b>Spain</b><br><a href='spain/'>View Guide</a>");
    L.marker([60.12, 18.64]).addTo(map).bindPopup("<b>Sweden</b><br><a href='sweden/'>View Guide</a>");
    L.marker([46.81, 8.22]).addTo(map).bindPopup("<b>Switzerland</b><br><a href='switzerland/'>View Guide</a>");
    L.marker([41.00, 28.97]).addTo(map).bindPopup("<b>Turkey</b><br><a href='turkey/'>View Guide</a>");
    L.marker([55.37, -3.43]).addTo(map).bindPopup("<b>UK</b><br><a href='uk/'>View Guide</a>");
    L.marker([48.37, 31.16]).addTo(map).bindPopup("<b>Ukraine</b><br><a href='ukraine/'>View Guide</a>");
    L.marker([41.90, 12.45]).addTo(map).bindPopup("<b>Vatican</b><br><a href='vatican/'>View Guide</a>");
</script>

## 🏆 Top 10 Cheapest

| # | Country | Rent | Meal | Beer |
|---|---------|------|------|------|
| 1 | 🇬🇷 Greece | 550€ | 15€ | 5€ |
| 2 | 🇷🇴 Romania | 600€ | 12€ | 3€ |
| 3 | 🇭🇺 Hungary | 650€ | 10€ | 2.80€ |
| 4 | 🇧🇬 Bulgaria | 669€ | 10€ | 2.69€ |
| 5 | 🇪🇪 Estonia | 698€ | 15€ | 6€ |
| 6 | 🇷🇸 Serbia | 700€ | 12€ | 3.20€ |
| 7 | 🇭🇷 Croatia | 700€ | 12€ | 4€ |
| 8 | 🇵🇱 Poland | 1,000€ | 10€ | 4.30€ |
| 9 | 🇨🇿 Czechia | 1,000€ | 9.50€ | 2.40€ |
| 10 | 🇮🇹 Italy | 1,000€ | 15€ | 5€ |

## 🏔️ Northern Europe (6)

| Country | Rent | → |
|---------|------|---|
| 🇳🇴 [Norway](norway/) | 1,603€ | → |
| 🇸🇪 [Sweden](sweden/) | 1,404€ | → |
| 🇩🇰 [Denmark](denmark/) | 1,775€ | → |
| 🇫🇮 [Finland](finland/) | 1,300€ | → |
| 🇪🇪 [Estonia](estonia/) | 698€ | → |
| 🇮🇸 [Iceland](iceland/) | 1,800€ | → |
| 🇱🇻 [Latvia](latvia/) | 550€ | → |
| 🇱🇹 [Lithuania](lithuania/) | 650€ | → |

## 🏗️ Eastern Europe (6)

| Country | Rent | → |
|---------|------|---|
| 🇵🇱 [Poland](poland/) | 1,000€ | → |
| 🇨🇿 [Czechia](czech/) | 1,000€ | → |
| 🇭🇺 [Hungary](hungary/) | 650€ | → |
| 🇷🇴 [Romania](romania/) | 600€ | → |
| 🇷🇸 [Serbia](serbia/) | 700€ | → |
| 🇧🇬 [Bulgaria](bulgaria/) | 669€ | → |
| 🇧🇾 [Belarus](belarus/) | 350€ | → |
| 🇲🇩 [Moldova](moldova/) | 400€ | → |
| 🇺🇦 [Ukraine](ukraine/) | 400€ | → |
| 🇷🇺 [Russia](russia/) | 600€ | → |
| 🇰🇿 [Kazakhstan](kazakhstan/) | 300€ | → |

## ☀️ Southern Europe (6)

| Country | Rent | → |
|---------|------|---|
| 🇪🇸 [Spain](spain/) | 1,350€ | → |
| 🇵🇹 [Portugal](portugal/) | 1,100€ | → |
| 🇮🇹 [Italy](italy/) | 1,000€ | → |
| 🇬🇷 [Greece](greece/) | 550€ | → |
| 🇭🇷 [Croatia](croatia/) | 700€ | → |
| 🇲🇹 [Malta](malta/) | 1,100€ | → |
| 🇦🇱 [Albania](albania/) | 400€ | → |
| 🇦🇩 [Andorra](andorra/) | 1,200€ | → |
| 🇧🇦 [Bosnia](bosnia/) | 300€ | → |
| 🇨🇾 [Cyprus](cyprus/) | 900€ | → |
| 🇲🇪 [Montenegro](montenegro/) | 500€ | → |
| 🇲🇰 [Macedonia](north-macedonia/) | 300€ | → |
| 🇸🇲 [San Marino](san-marino/) | 800€ | → |
| 🇹🇷 [Turkey](turkey/) | 500€ | → |
| 🇻🇦 [Vatican](vatican/) | N/A | → |

## 🔵 Central Europe (3)

| Country | Rent | → |
|---------|------|---|
| 🇩🇪 [Germany](germany/) | 1,270€ | → |
| 🇦🇹 [Austria](austria/) | 1,077€ | → |
| 🇨🇭 [Switzerland](switzerland/) | 2,580€ | → |
| 🇸🇰 [Slovakia](slovakia/) | 600€ | → |
| 🇸🇮 [Slovenia](slovenia/) | 750€ | → |
| 🇱🇮 [Liechtenstein](liechtenstein/) | 2,200€ | → |

## 🌊 Western Europe (5)

| Country | Rent | → |
|---------|------|---|
| 🇬🇧 [UK](uk/) | 2,530€ | → |
| 🇮🇪 [Ireland](ireland/) | 2,118€ | → |
| 🇳🇱 [Netherlands](netherlands/) | 2,260€ | → |
| 🇧🇪 [Belgium](belgium/) | 1,125€ | → |
| 🇫🇷 [France](france/) | 2,000€ | → |
| 🇱🇺 [Luxembourg](luxembourg/) | 1,800€ | → |
| 🇲🇨 [Monaco](monaco/) | 6,000€ | → |

## ⛰️ Caucasus (3)

| Country | Rent | → |
|---------|------|---|
| 🇬🇪 [Georgia](georgia/) | 600€ | → |
| 🇦🇲 [Armenia](armenia/) | 500€ | → |
| 🇦🇿 [Azerbaijan](azerbaijan/) | 450€ | → |

## 📊 Statistics

- 50 Countries
- 300+ Cities
- Cheapest: 550€ (Greece)
- Most Expensive: 2,580€ (Switzerland)

*Data: Numbeo.com, March 2026*
