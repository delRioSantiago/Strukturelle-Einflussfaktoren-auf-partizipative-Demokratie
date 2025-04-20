import requests
import zipfile
import io
import os
import pandas as pd
import glob

def load_and_average_wdi_indicator(
    wdi_code: str,
    years: list[int],
    raw_path: str,
    processed_path: str,
    compute_variance: bool = False
) -> tuple[pd.DataFrame, pd.DataFrame | None, pd.DataFrame | None]:

    """
    Lädt einen WDI-Indikator von der Weltbank, berechnet den Durchschnitt über einen Zeitraum und die mittlere Varianz der Variable pro Land in diesem Zeitraum.

    Args:
        wdi_code (str): indicator code z. B. "NY.GDP.PCAP.CD"
        years (list of int): Liste der Jahre (z. B. [2010, 2015, 2020])
        raw_path (str): Speicherort für entpackte CSVs
        processed_path (str): Speicherort für Output-Dateien
        compute_variance (bool): Wenn True, wird zusätzlich zur Mittelwertberechnung auch die mittlere Varianz pro Variable (über Länder hinweg) berechnet und zurückgegeben.

    Returns:
        df_avg (DataFrame): Mittelwert pro Land für den Zeitraum.
        metadata_df (DataFrame): Metadaten des Indikators.
        df_var_compact (DataFrame | None): Zusammenfassung der Länder-Varianz (wenn aktiviert).
    """
    os.makedirs(raw_path, exist_ok=True)
    os.makedirs(processed_path, exist_ok=True)

    # Download ZIP
    url = f"https://api.worldbank.org/v2/en/indicator/{wdi_code}?downloadformat=csv"
    response = requests.get(url)
    if response.status_code != 200:
        raise ConnectionError(f"Download fehlgeschlagen mit Status {response.status_code}")
    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        z.extractall(raw_path)


    # CSV-Datei mit Daten finden
    csv_files = glob.glob(os.path.join(raw_path, f"API_{wdi_code}_DS2*.csv"))
    if not csv_files:
        raise FileNotFoundError("CSV-Datei mit Indikator nicht gefunden.")
    csv_file = csv_files[0]
    
    metadata_df = None 
    
    for fname in os.listdir(raw_path):
        file_path = os.path.join(raw_path, fname)
    
    # Speichere Metadaten-Datei separat pro Indikator
        if fname.startswith("Metadata_Country"):
            target = os.path.join(processed_path, f"Metadata_{wdi_code}.csv")
            os.replace(file_path, target)
            print(f"Metadata gespeichert: {target}")
            try:
                metadata_df = pd.read_csv(target)
            except Exception as e:
                print(f"Warnung: Metadaten konnten nicht geladen werden: {e}")
                metadata_df = None
    
        # Sonstige unerwünschte Dateien löschen
        elif not fname.lower().endswith(".csv") and os.path.isfile(file_path):
            try:
                os.remove(file_path)
            except PermissionError:
                print(f"Nicht löschbar (übersprungen): {file_path}")
    

    # Einlesen und Long-Format erzeugen
    df = pd.read_csv(csv_file, skiprows=4)
    df_long = df.melt(id_vars=["Country Name", "Country Code", "Indicator Name", "Indicator Code"],
                      var_name="year", value_name="value")
    df_long["year"] = pd.to_numeric(df_long["year"], errors="coerce")
    df_long = df_long.dropna(subset=["year", "value"])

    # Zeitraum filtern
    df_filtered = df_long[df_long["year"].isin(years)]

    # Durchschnitt berechnen
    start_year, end_year = min(years), max(years)
    df_avg = (df_filtered
      .groupby(["Country Name", "Country Code"])["value"]
      .mean()
      .reset_index()
      .rename(columns={"value": f"{wdi_code}_{start_year}_{end_year}"}))
    avg_outfile = os.path.join(processed_path, f"{wdi_code}_avg_{start_year}_{end_year}.csv")
    df_avg.to_csv(avg_outfile, index=False)
    
    # Varianz berechnen
    df_var_compact= None
    if compute_variance:
        df_var = (
        df_filtered
        .groupby(["Country Name", "Country Code"])["value"]
        .var()
        .reset_index()
        .rename(columns={"value": f"{wdi_code}_{start_year}_{end_year}_var"})
        )
        
        df_var_compact = df_var.drop(columns=["Country Name", "Country Code"]).agg(["mean", "median"]).T
        df_var_compact = df_var_compact.rename(columns={
            "mean": "Ø Varianz über Länder",
            "median": "Median Varianz über Länder"
        })
        df_var_compact["Variable"] = wdi_code
    return df_avg, metadata_df, df_var_compact
        
