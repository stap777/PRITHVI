import os
import concurrent.futures
from pathlib import Path
import imdlib as imd

def download_imd_data(var_type, start_yr, end_yr, output_dir):
    """
    Downloads IMD gridded binary (.grd) data and saves it directly 
    to the target raw data subdirectory.
    """
    print(f"🔄 Starting IMD Download: {var_type.upper()} ({start_yr} to {end_yr})...")
    try:
        # FIX: Passing var_type, start_yr, and end_yr as positional arguments
        imd.get_data(
            var_type,
            start_yr,
            end_yr,
            fn_format="yearwise",
            file_dir=str(output_dir)
        )
        print(f"✅ Successfully saved {var_type.upper()} to {output_dir}")
    except Exception as e:
        print(f"❌ Error downloading {var_type.upper()}: {e}")

def create_workspace_guides(base_path):
    """Automates folder verification and drops instructional guides."""
    (base_path / "raw" / "satellite").mkdir(parents=True, exist_ok=True)
    (base_path / "raw" / "humidity").mkdir(parents=True, exist_ok=True)
    (base_path / "external").mkdir(parents=True, exist_ok=True)

def main():
    # Setup data directories relative to execution root
    data_path = Path("data")
    rain_dir = data_path / "raw" / "rainfall"
    temp_dir = data_path / "raw" / "temperature"
    
    # Ensure standard destination folders are created
    rain_dir.mkdir(parents=True, exist_ok=True)
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    print("==================================================")
    print("🌍 DIGITAL TWIN CLIMATE: RUNNING DATA INGESTION   ")
    print("==================================================\n")
    
    create_workspace_guides(data_path)
    
    # Define targets according to Hackathon scope (2020 to 2025)
    start_year = 2020
    end_year = 2025
    
    # Bundle tasks to run simultaneously using multi-threading
    tasks = [
        ("rain", start_year, end_year, rain_dir),
        ("tmax", start_year, end_year, temp_dir),
        ("tmin", start_year, end_year, temp_dir)
    ]
    
    print("⚡ Spawning parallel workers to pull IMD Rainfall & Temperature Grids...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(download_imd_data, *task) for task in tasks]
        concurrent.futures.wait(futures)
        
    print("\n🏁 Data Ingestion complete! Check your 'data/' directories.")

if __name__ == "__main__":
    main()