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

data_gdf_description = """
- geometry - active GeoDataFrame geometry
- Depth - Depth of the sample. Values: 0_10, 10_20, 20_30. Dtype: object.
- POINTID - Unique identifier of the LUCAS survey point. 8-digit number. Dtype: int64.
- pH_CaCl2 - pH measured in a CaCl2 solution. Range: 2–10. Dtype: float64.
- pH_H2O - pH measured in a soil-water suspension. Range: 2–10. Dtype: float64.
- EC - Electrical conductivity. Unit: mS/m, LOD: 0.1. Dtype: float64.
- OC - Organic carbon content at depth 0-20 cm. Unit: g/kg, LOD: 2. Dtype: float64.
- CaCO3 - Carbonates content at depth 0-20 cm. Unit: g/kg, LOD: 1. Dtype: float64.
- P - Phosphorus content. Unit: mg/kg, LOD: 10. Dtype: float64.
- N - Total nitrogen content. Unit: g/kg, LOD: 0.2. Dtype: float64.
- K - Extractable potassium content. Unit: mg/kg, LOD: 10. Dtype: float64.
- OC (20-30 cm) - Organic carbon content at depth 20-30 cm. Unit: g/kg, LOD: 2. Dtype: float64.
- CaCO3 (20-30 cm) - Carbonates content at depth 20-30 cm. Unit: g/kg, LOD: 1. Dtype: float64.
- Ox_Al - Aluminum oxylate. Unit: mg/kg. Dtype: float64.
- Ox_Fe - Iron oxylate. Unit: mg/kg. Dtype: float64.
- NUTS_0 - NUTS code for the country where the sample was taken. Based on GPS coordinates. Dtype: object.
- NUTS_1 - NUTS 1 code for the location. Derived from survey data. Dtype: object.
- NUTS_2 - NUTS 2 code for the location. Derived from survey data. Dtype: object.
- NUTS_3 - NUTS 3 code for the location. Derived from survey data. Dtype: object.
- TH_LAT - Theoretical latitude. Coordinates in decimal degrees. Dtype: float64.
- TH_LONG - Theoretical longitude. Coordinates in decimal degrees. Dtype: float64.
- SURVEY_DATE - Date of the survey. Dtype: datetime64[ms].
- Elev - Elevation from surveyor GPS. Unit: meters. Dtype: int64.
- LC - LUCAS Land Cover code. Derived from Eurostat. Dtype: object.
- LU - LUCAS Land Use code. Derived from Eurostat. Dtype: object.
- LC0_Desc - Main land cover class description. Derived from Eurostat. Dtype: object.
- LC1_Desc - Detailed land cover class description. Derived from Eurostat. Dtype: object.
- LU1_Desc - Detailed land use class description. Derived from Eurostat. Dtype: object.
- Country - Country of the sample location. Derived from survey data. Dtype: object.
- geometry - Geometry of the sample point. Shapefile data. Dtype: geometry.
"""