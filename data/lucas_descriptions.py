import pandas as pd

numerical_features = pd.DataFrame({
    "Column Name": [
        "pH_CaCl2", "pH_H2O", "EC", "OC", "CaCO3", "P", "N", "K", 
        "OC (20-30 cm)", "CaCO3 (20-30 cm)", "Ox_Al", "Ox_Fe", "TH_LAT", "TH_LONG", "Elev"
    ],
    "Description": [
        "pH measured in a CaCl2 solution", 
        "pH measured in a suspension of soil in water", 
        "Electrical conductivity in mS/m", 
        "Organic carbon content (at depth 0-20 cm) in g/kg", 
        "Carbonates content (at depth 0-20 cm) in g/kg", 
        "Phosphorus content in mg/kg", 
        "Total nitrogen content in g/kg", 
        "Extractable potassium content in mg/kg", 
        "Organic carbon content at the depth 20-30 cm in g/kg", 
        "Carbonates content at the depth 20-30 cm in g/kg", 
        "Aluminum oxalate content in mg/kg", 
        "Iron oxalate content in mg/kg", 
        "Theoretical latitude in decimal degrees", 
        "Theoretical longitude in decimal degrees", 
        "Elevation in meters from surveyor GPS"
    ],
    "LOD/Measurement Range": [
        "2 – 10", "2 – 10", "0.1", "2", "1", "10", "0.2", "10", 
        "2", "1", "-", "-", "-", "-", "-"
    ]
})

non_numerical_features = pd.DataFrame({
    "Column Name": [
        "Depth", "POINTID", "Country", "NUTS_0", "NUTS_1", "NUTS_2", "NUTS_3", 
        "SURVEY_DATE", "LC", "LU", "LC0_Desc", "LC1_Desc", "LU1_Desc"
    ],
    "Description": [
        "Value indicating the depth of the sample", 
        "Unique identifier of the LUCAS survey point", 
        "The full name of the country where the soil sample was collected.",
        "NUTS code for the country where the sample was taken", 
        "NUTS 1 code for the location where the sample was taken", 
        "NUTS 2 code for the location where the sample was taken", 
        "NUTS 3 code for the location where the sample was taken", 
        "Date of the survey", 
        "LUCAS Land Cover Code", 
        "LUCAS Land Use Code", 
        "Main Land Cover class description", 
        "Detailed Land Cover class description", 
        "Detailed Land Use class description"
    ]
})

nuts_to_country = {
    "AT": "Austria",
    "BE": "Belgium",
    "BG": "Bulgaria",
    "CY": "Cyprus",
    "CZ": "Czech Republic",
    "DE": "Germany",
    "DK": "Denmark",
    "EE": "Estonia",
    "EL": "Greece",
    "ES": "Spain",
    "FI": "Finland",
    "FR": "France",
    "HR": "Croatia",
    "HU": "Hungary",
    "IE": "Ireland",
    "IT": "Italy",
    "LT": "Lithuania",
    "LU": "Luxembourg",
    "LV": "Latvia",
    "MT": "Malta",
    "NL": "Netherlands",
    "PL": "Poland",
    "PT": "Portugal",
    "RO": "Romania",
    "SE": "Sweden",
    "SI": "Slovenia",
    "SK": "Slovakia",
    "UK": "United Kingdom",
}
