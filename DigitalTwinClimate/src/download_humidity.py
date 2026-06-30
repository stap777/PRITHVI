import cdsapi
import os

os.makedirs("data/raw/humidity", exist_ok=True)

client = cdsapi.Client()

client.retrieve(
    "reanalysis-era5-single-levels",
    {
        "product_type": "reanalysis",
        "variable": "2m_temperature",
        "year": "2024",
        "month": "01",
        "day": "01",
        "time": "12:00",
        "data_format": "netcdf",
        "download_format": "unarchived"
    },
    "data/raw/humidity/test.nc"
)

print("Download completed.")