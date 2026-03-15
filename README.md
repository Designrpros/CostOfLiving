# 🪙 Cost of Living - Europe Guide

A comprehensive cost of living guide for 27 European countries with 10 cities each.

![Material Design](https://img.shields.io/badge/MkDocs-Material-purple?style=flat&logo=markdown)

## 🚀 Quick Start

### Option 1: MkDocs (Recommended - Beautiful!)

```bash
# Install
pip install mkdocs-material

# Run
cd europa
mkdocs serve
```

Then open http://localhost:8080

### Option 2: Simple Python Server

```bash
cd europa
python3 -m http.server 8080
```

Open http://localhost:8080/index.html

## 📁 Structure

```
europa/
├── index.html              ← Material Design landing page
├── mkdocs.yml              ← MkDocs configuration
├── start.sh               ← Quick start script
│
├── norway/
│   ├── overview.md        ← Country data
│   ├── overview.html      ← Country page
│   └── byer/alle.md      ← Cities
│
├── sweden/
├── greece/
└── ... (27 countries)
```

## 🎨 Features

- **27 Countries** - All European countries
- **270 Cities** - 10 cities per country
- **Sorted by price** - Cheapest to most expensive
- **Material Design** - Modern, clean UI
- **Search** - Quick country search
- **Responsive** - Works on mobile

## 📊 Data

| Stat | Value |
|------|-------|
| Countries | 27 |
| Cities | 270 |
| Cheapest Rent | 550€ (Greece) |
| Most Expensive | 2,580€ (Switzerland) |

## 🛠️ Customization

Edit `mkdocs.yml` to change:
- Theme colors
- Navigation structure
- Site metadata

## 📝 Data Source

- **Numbeo.com** (March 2026)
- Exchange rate: ~11.5 NOK/EUR

---

**Built with** ❤️ **by Alcatelz** ☀️