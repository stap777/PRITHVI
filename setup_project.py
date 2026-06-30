import os
from pathlib import Path

def create_project_structure():
    # Define the base directory
    base_name = "DigitalTwinClimate"
    base_dir = Path(base_name)
    
    # Define all the subdirectories based on your requirements
    folders = [
        "data/raw/rainfall",
        "data/raw/temperature",
        "data/raw/satellite",
        "data/raw/humidity",
        "data/raw/soil_moisture",
        "data/processed",
        "data/external",
        "src",
        "notebooks",
        "models",
        "outputs"
    ]
    
    print(f"Creating project structure for: {base_name}...\n")
    
    # 1. Create all folders (parents=True ensures nested folders are created)
    for folder in folders:
        folder_path = base_dir / folder
        folder_path.mkdir(parents=True, exist_ok=True)
        print(f"📁 Created: {folder_path}")
        
    # 2. Create the README.md file
    readme_path = base_dir / "README.md"
    readme_path.touch(exist_ok=True)
    
    # Add a title to the README
    with open(readme_path, "w") as f:
        f.write("# AI-Powered Digital Twin of India's Climate\n\nProject setup initialized.")
    print(f"📄 Created: {readme_path}")
    
    print("\n✅ Project structure created successfully!")

if __name__ == "__main__":
    create_project_structure()