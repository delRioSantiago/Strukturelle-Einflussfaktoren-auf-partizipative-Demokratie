import pandas as pd
import os
import pycountry
from config import RAW_PATH, PROCESSED_PATH, BARRO_LEE_FILENAME

COUNTRY_FIXES = {
    "Cote dIvoire": "Côte d'Ivoire",  
    "Democratic Republic of the Congo": "Congo, The Democratic Republic of the", 
    "Swaziland": "Eswatini",
    "Dominican Rep.": "Dominican Republic",
    "China, Hong Kong Special Administrative Region": "Hong Kong",
    "China, Macao Special Administrative Region": "Macao",
    "Iran (Islamic Republic of)": "Iran",
    "Republic of Korea": "South Korea",
    "Turkey": "Türkiye",
    "Libyan Arab Jamahiriya": "Libya",
    "Reunion": "Réunion",
}

def get_iso3(country_name):
    try:
        return pycountry.countries.lookup(country_name).alpha_3
    except LookupError:
        return None

def load_barro_lee_subset(target_year: int) -> pd.DataFrame:

    """
    Lädt Barro-Lee-Daten für ein bestimmtes Jahr (z. B. 2010) und speichert sie gefiltert und umbenannt.

    Args:
        target_year (int): Jahr, das ausgewählt werden soll
    """
    path_to_csv=os.path.join(RAW_PATH, BARRO_LEE_FILENAME)    
    output_path=os.path.join(PROCESSED_PATH, "barro_lee_2010.csv")
    if not os.path.exists(path_to_csv):
        raise FileNotFoundError(f"Datei nicht gefunden: {path_to_csv}")
    df = pd.read_csv(path_to_csv)

    # Nur das gewünschte Jahr
    df = df[df["year"] == target_year]

    # Auswahl der benötigten Spalten
    df = df[["country"] + ["yr_sch"]]
    rename_map={
            "yr_sch": "Avg Years Schooling",
        }
    df = df.rename(columns={
        "country": "Country Name",
        **rename_map
    })

    df["Country Name"] = df["Country Name"].replace(COUNTRY_FIXES)
    df["Country Code"] = df["Country Name"].apply(get_iso3)
    missing_iso = df[df["Country Code"].isna()]
    if not missing_iso.empty:
        print("Keine ISO-Codes gefunden für folgende Länder:")
        print(missing_iso["Country Name"].tolist())
    df.to_csv(output_path, index=False)
    print(f" Barro-Lee Daten für {target_year} gespeichert unter: {output_path}")
    
    return df


