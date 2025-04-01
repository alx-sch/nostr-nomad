import glob
import zipfile
import os

def extract_zips(folder_path):
    """Extracts all ZIP files in the given folder into 'unzipped/{zip_name}' subfolders."""
    zip_files = glob.glob(os.path.join(folder_path, "*.zip"))
    unzipped_folder = os.path.join(folder_path, "unzipped")

    os.makedirs(unzipped_folder, exist_ok=True)  # Ensure the 'unzipped' folder exists

    for zip_file in zip_files:
        try:
            zip_name = os.path.splitext(os.path.basename(zip_file))[0]  # Get ZIP name without extension
            extract_folder = os.path.join(unzipped_folder, zip_name)

            os.makedirs(extract_folder, exist_ok=True)  # Create unique subfolder for each ZIP

            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                zip_ref.extractall(extract_folder)

        except zipfile.BadZipFile:
            print(f"Skipping {zip_file} (corrupted or invalid)")
            
