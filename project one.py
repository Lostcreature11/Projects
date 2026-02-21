
import logging
import shutil
from pathlib import Path

CATEGORIES = {
    ".py": "Python_Code",
    ".txt": "Documents",
    ".pdf": "Documents",
    ".docx": "Documents",
    ".jpg": "Images",
    ".jpeg": "Images",
    ".png": "Images",
    ".mp3": "Audio",
    ".mp4": "Videos",
}

LOG_FILE = "organizer.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ------------------- FUNCTIONS -------------------

def resolve_conflict(target_path: Path) -> Path:
    counter = 1
    new_path = target_path
    while new_path.exists():
        new_name = f"{target_path.stem}({counter}){target_path.suffix}"
        new_path = target_path.parent / new_name
        counter += 1
    return new_path


def organize_directory(source: Path, destination: Path, dry_run=False):
    moved_files = 0
    errors = 0

    for item in source.rglob("*"):
        try:
            if item.is_file():
                ext = item.suffix.lower()
                category = CATEGORIES.get(ext, "Other")
                target_dir = destination / category

                if not target_dir.exists():
                    if not dry_run:
                        target_dir.mkdir(parents=True, exist_ok=True)

                target_path = target_dir / item.name

                if target_path.exists():
                    target_path = resolve_conflict(target_path)

                logging.info(f"Moving {item} → {target_path}")
                print(f"Moving: {item.name} → {category}")

                if not dry_run:
                    shutil.move(str(item), str(target_path))

                moved_files += 1

        except PermissionError:
            logging.error(f"Permission denied: {item}")
            errors += 1
        except Exception as e:
            logging.error(f"Error processing {item}: {e}")
            errors += 1

    print("\nSummary:")
    print(f"Files moved: {moved_files}")
    print(f"Errors: {errors}")


if __name__ == "__main__":
    print("==== Automated File Organizer ====")

    source_input = input("Enter the SOURCE folder path: ").strip()
    destination_input = input("Enter the DESTINATION folder path: ").strip()
    dry_choice = input("Do you want dry-run mode? (yes/no): ").strip().lower()

    source_path = Path(source_input)
    destination_path = Path(destination_input)

    if not source_path.exists():
        print("Source folder does not exist. Exiting.")
    else:
        dry_mode = True if dry_choice == "yes" else False
        organize_directory(source_path, destination_path, dry_mode)

        
