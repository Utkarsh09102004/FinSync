import kagglehub
import os
import shutil
import sys

def download_and_move_dataset():
    # Download latest version
    path = kagglehub.dataset_download("jazidesigns/financial-accounting")
    
    print("Path to dataset files:", path)
    
    # Get current directory where this script is running
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Move all files from downloaded path to current directory
    try:
        file_count = 0
        for item in os.listdir(path):
            source = os.path.join(path, item)
            destination = os.path.join(current_dir, item)
            
            if os.path.isfile(source):
                shutil.move(source, destination)
                print(f"Moved: {item}")
                file_count += 1
                
        print(f"Successfully moved {file_count} files to: {current_dir}")
    except Exception as e:
        print(f"Error moving files: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    download_and_move_dataset()