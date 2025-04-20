# Forschungsprojekt: Einfluss struktureller Faktoren auf partizipative Demokratie

## Projektziel
Ziel ist es, mittels Feature-Analyse und Clustering zu untersuchen, wie strukturelle Rahmenbedingungen (z. B. Bildung, Medienfreiheit, Ungleichheit) mit dem Grad partizipativer Demokratie zusammenhängen. 

## Datenquellen
| Quelle     | Beschreibung                                  |
|------------|-----------------------------------------------|
| V-Dem      | Demokratie-Indikatoren (v15), insb. `v2x_partipdem` |
| Weltbank   | Sozial- & Wirtschaftsindikatoren (WDI, u.a. BIP, Bildung, Urbanisierung) |
| Barro-Lee  | Durchschnittliche Schulbildung (bis 2010)     |

## Methodik
### 1. Feature Importance Analyse
- Zielvariable: `v2x_partipdem` (Participatory Democracy Index)
- Verfahren: Random Forest
- Ziel: Identifikation relevanter erklärender Variablen (global & innerhalb von Clustern)

### 2. Clustering
- Kontextbasierte Segmentierung der Länder (K-Means)
- Input: sozioökonomische Indikatoren (z. B. Urbanisierung, Internetnutzung, Bildungsniveau)
- Ziel: Vergleich partizipativer Demokratie unter strukturell ähnlichen Ländern

### 3. Varianz- & Abdeckungsanalyse
- Durchschnittliche Varianz je Variable (nach Ländern gruppiert)
- Ziel: Auswahl eines geeigneten Zeitraums für stabile Mittelwerte

## Konfiguration (`config.py`)
```python
YEARS = list(range(2015, 2020))  # Analysezeitraum
RAW_PATH = "data/raw/"
PROCESSED_PATH = "data/processed/"
TARGET_VARIABLE = "v2x_partipdem"
```
> Der Barro-Lee-Datensatz muss manuell heruntergeladen und gespeichert werden als BL2013_MF1599_v2.2.csv im Ordner data/raw/   
> Downloadlink: https://github.com/barrolee/BarroLeeDataSet/blob/master/BLData/BL2013_MF1599_v2.2.csv

## Technische Voraussetzungen

- **Python-Version**: >= 3.10  
- Benötigte Libraries:  
  `pandas`, `numpy`, `matplotlib`, `seaborn`, `scikit-learn`, `requests`, `pycountry`, `zipfile`, `glob`

## Durchläufe der Varianz-Analyse

### Lauf 1: Zeitraum 2010–2019
- Ziel: Maximale Abdeckung
- Ergebnis: Höhere Streuung in vielen Variablen
- Beispiel: Ø Varianz über Länder: 0.0215

### Lauf 2: Zeitraum 2015–2019
- Ziel: Robustere Mittelwerte durch geringere Varianz
- Ergebnis: Deutlich niedrigere Streuung
- Beispiel: Ø Varianz über Länder: 0.0114
- → Dieser Zeitraum wurde für die weitere Analyse gewählt

> Hinweis: Die Varianz-Ergebnisse befinden sich in `data/processed/df_var_summary_*.csv`


## Ordnerstruktur

```
data/
  ├── raw/               # Rohdaten (WDI ZIPs, V-Dem etc.)
  ├── processed/         # Vorverarbeitete Daten (z. B. df_master.csv)
        ├── variance/    # Varianz-Ergebnisse pro Indikator

scripts/
  ├── load_wdi.py
  ├── load_vdem.py
  ├── load_barro_lee.py
  └── config.py

notebooks/
  └── Selbststudium.ipynb
```

## Autor / Kontakt
- Name: [Dein Name]
- Universität / Institution (optional)
- Kontakt: [optional]
