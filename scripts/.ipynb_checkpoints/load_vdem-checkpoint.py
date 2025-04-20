import os
import requests
import zipfile
import io
import pandas as pd

def load_vdem_subset(
    years,
    variables,
    download_url,
    raw_path,
    processed_path,
    save_as,
    compute_variance=False,
):
    """
    Lädt den V-Dem-Datensatz herunter, entpackt ihn und speichert nur die
    ausgewählten Variablen und Jahre – ohne Aggregation über Jahre.

    Args:
        years (list of int): Liste der Jahre (z. B. [2010, 2015, 2020])
        variables (list of str): Liste der Variablencodes (z. B. ["v2x_partipdem", "v2x_rule"])
        download_url (str): URL zur ZIP-Datei des V-Dem-Datensatzes
        raw_path (str): Speicherort für entpackte Rohdaten
        processed_path (str): Speicherort für gefilterte Daten
        save_as (str): Dateiname der Ausgabedatei (CSV)

    Returns:
        pd.DataFrame: Gefilterter DataFrame mit Ländern, Jahren, Variablen
    """

    os.makedirs(raw_path, exist_ok=True)
    os.makedirs(processed_path, exist_ok=True)

    print("Lade V-Dem ZIP-Datei herunter ...")
    try:
        response = requests.get(download_url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Download fehlgeschlagen: {e}")

    print("Entpacke ZIP-Datei ...")
    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        z.extractall(raw_path)

    # CSV-Datei einlesen
    csv_filename = "V-Dem-CY-Full+Others-v15.csv"
    csv_path = os.path.join(raw_path, csv_filename)
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV-Datei nicht gefunden: {csv_path}")

    print("Lade und filtere CSV-Datei ...")
    all_columns = ["country_name", "country_text_id", "year"] + variables
    df = pd.read_csv(csv_path, usecols=lambda col: col in all_columns, low_memory=False)

    df = df[df["year"].isin(years)]
    df.rename(columns={
        "country_name": "Country Name",
        "country_text_id": "Country Code"
    }, inplace=True)

    print("Berechne Durchschnitt pro Land ...")
    df_avg = df.groupby(["Country Name", "Country Code"])[variables].mean().reset_index()
    output_file = os.path.join(processed_path, save_as)
    df_avg.to_csv(output_file, index=False)
    print(f"V-Dem-Durchschnitt gespeichert unter: {output_file}")

    df_var_compact = None
    if compute_variance:
        print("Berechne Varianz pro Land ...")
        df_var = df.groupby(["Country Name", "Country Code"])[variables].var().reset_index()
        df_var = df_var.rename(columns={var: f"{var}_var" for var in variables})
        df_var_compact = df_var.drop(columns=["Country Name", "Country Code"]).agg(["mean", "median"]).T
        df_var_compact = df_var_compact.rename(columns={
            "mean": "Ø Varianz über Länder",
            "median": "Median Varianz über Länder"
        })
        df_var_compact["Variable"] = df_var_compact.index.str.replace("_var", "", regex=False)
        df_var_compact = df_var_compact.reset_index(drop=True)
    return df_avg, df_var_compact
        