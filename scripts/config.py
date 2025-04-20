
# Analysezeitraum
YEARS = list(range(2015, 2020)) 
VARIANCE_ANALYSIS = False

# Pfade
RAW_PATH = "../data/raw/"
PROCESSED_PATH = "../data/processed/"
RESULTS_PATH = "../results/"

# WDI-Indikatoren (Code → sprechender Name)
WDI_INDICATORS = {
    "NY.GDP.PCAP.CD", # BIP pro Kopf (in USD)
    "SE.ADT.LITR.ZS", # Alphabetisierungsrate
    "SP.URB.TOTL.IN.ZS", # Urbanisierungsgrad
    "IT.NET.USER.ZS", # Anteil der Internetnutzer:innen
    "SP.POP.TOTL", # Gesamtbevölkerung
    "SL.UEM.TOTL.ZS", # Arbeitslosenquote
    "FP.CPI.TOTL.ZG", # Inflationsrate (jährlich, in %)
    "SE.XPD.TOTL.GD.ZS", # Bildungsausgaben (in % des BIP)
    "NE.CON.PRVT.ZS", # Private Konsumausgaben (in % des BIP)
    "SH.XPD.CHEX.PC.CD", # Gesundheitsausgaben pro Kopf (in USD)
    "SI.POV.GINI" # GINI-Index (Einkommensungleichheit)
}

# V-Dem-Variablen zur Kontextanalyse
VDEM_VARIABLES = [
    "v2x_partipdem", # Index für partizipative Demokratie
    "v2x_rule", # Rechtsstaatlichkeit – Einschränkung der Exekutive durch unabhängige Instanzen
    "v2x_jucon", # Judizielle Unabhängigkeit – Unabhängigkeit der Justiz von anderen Staatsgewalten
    "v2xlg_legcon", # Legislative Kontrolle über die Exekutive
    "v2x_corr", # Korruptionswahrnehmung auf systemischer Ebene
    "v2mecenefi", # Medienzensur im Internet – Umfang staatlicher Eingriffe
    "v2xeg_eqaccess", # Gleichheit des politischen Zugangs für soziale Gruppen
    "v2xeg_eqdr", # Ressourcengleichheit – Gleichverteilung öffentlicher Güter
    "v2xeg_eqprotec", # Rechtsschutz – Gleichheit beim Zugang zu bürgerlichen Rechten
    "v2clsocgrp", # Gleichheit bürgerlicher Rechte für soziale Gruppen
    "v2dlconslt", # Konsultation gesellschaftlicher Gruppen bei politischen Entscheidungen
    "v2dlengage", # Zivilgesellschaftliche Beteiligung auf lokaler Ebene
    "v2eldonate", # Regelungen zu privaten Spenden an politische Parteien
    "v2elpubfin", # Transparenz der Wahlkampffinanzierung
    "v2elrstrct", # Regulierung politischer Werbung im Wahlkampf
    "v2psplats", # Vielfalt politischer Parteien und Programme
]

VDEM_DOWNLOAD_URL = "https://v-dem.net/media/datasets/V-Dem-CY-FullOthers-v15_csv.zip"

# Zielvariable
TARGET_VARIABLE = "v2x_partipdem"

# Barro-Lee Variable 
BARRO_LEE_FILENAME = "BL2013_MF1599_v2.2.csv"


CLUSTERING_VARIABLES = [
    "NY.GDP.PCAP.CD",
    "SP.URB.TOTL.IN.ZS",
    "IT.NET.USER.ZS",
    "Avg Years Schooling",
    "SI.POV.GINI"
]