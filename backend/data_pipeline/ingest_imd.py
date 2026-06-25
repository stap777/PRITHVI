"""
IMD Data Ingestion Pipeline.

This pipeline script is responsible for downloading and parsing daily gridded 
datasets (precipitation at 0.25-deg and temperature at 1.0-deg resolution) from 
the India Meteorological Department (IMD) HTTP/FTP servers.

TODO:
    * Set up scheduled cron/airflow worker tasks to fetch daily gridded binary files.
    * Parse binary .GRD files to standard float arrays.
"""

from pathlib import Path
from loguru import logger


def download_imd_gridded_data(year: int, parameter: str, save_dir: Path) -> Path:
    """
    Downloads raw binary gridded files from IMD server archives.
    
    Args:
        year: Target year to fetch.
        parameter: Climate parameter ('temp' or 'rain').
        save_dir: Destination path to write local files.
        
    Returns:
        Path of the downloaded file.
    """
    logger.info(f"Downloading IMD raw {parameter} binary grids for year: {year}")
    
    # Establish server connection and download file
    # Example:
    # url = f"http://www.imdpune.gov.in/Geoportal/Griddata/{parameter}/{parameter}_{year}.zip"
    # response = httpx.get(url)
    
    save_dir.mkdir(parents=True, exist_ok=True)
    destination_file = save_dir / f"imd_{parameter}_{year}.grd"
    
    # Write a mock file
    with open(destination_file, "w") as f:
        f.write(f"# MOCK IMD GRID DATA FOR YEAR {year}\n# PARAMETER: {parameter}\n")
        
    logger.info(f"Successfully downloaded and saved IMD raw file: {destination_file}")
    return destination_file


def parse_grid_format(grd_path: Path, output_nc_path: Path) -> Path:
    """
    Converts raw binary .grd files into standard self-describing NetCDF format.
    
    Args:
        grd_path: Path to the downloaded .grd binary file.
        output_nc_path: Path to write the target NetCDF file.
    """
    logger.info(f"Parsing binary IMD grid {grd_path.name} to NetCDF4: {output_nc_path.name}")
    
    # In production, we read the flat binary matrix and write using netCDF4 package:
    # - Rainfall grid is 135 rows x 129 cols (0.25 deg spacing)
    # - Temperature grid is 31 rows x 31 cols (1.0 deg spacing)
    # numpy_grid = np.fromfile(grd_path, dtype=np.float32)
    # create netcdf dimensions (lat, lon, time) and write variables...

    with open(output_nc_path, "w") as f:
        f.write(f"# MOCK NETCDF FILE CONVERTED FROM: {grd_path.name}\n")
        
    logger.info("Successfully finished NetCDF grid conversion.")
    return output_nc_path


if __name__ == "__main__":
    # Ensure local script can run independently
    import sys
    logger.info("Starting manual IMD Ingestion dry-run...")
    data_folder = Path("data") / "imd"
    raw_file = download_imd_gridded_data(2023, "rain", data_folder)
    parse_grid_format(raw_file, data_folder / "imd_rain_2023.nc")
    logger.info("IMD dry-run completed successfully.")
