import subprocess
import json
import sys

def backup_flatpak_packages(backup_file):
    try:
        # Get the list of installed Flatpak applications
        result = subprocess.run(['flatpak', 'list', '--app', '--columns=application'], capture_output=True, text=True, check=True)
        packages = result.stdout.splitlines()

        # Remove the header ("Application ID") from the list
        packages = packages[1:]

        # Write the package list to a JSON file
        with open(backup_file, 'w') as f:
            json.dump(packages, f, indent=4)
        print(f"Backup complete. Packages saved to {backup_file}")
    
    except subprocess.CalledProcessError as e:
        print(f"Error during backup: {e}")
        sys.exit(1)

def restore_flatpak_packages(backup_file):
    try:
        # Load the package list from the JSON file
        with open(backup_file, 'r') as f:
            packages = json.load(f)
        
        # Install each package from the backup
        for package in packages:
            print(f"Installing {package}...")
            subprocess.run(['flatpak', 'install', '--assumeyes', package], check=True)
        print(f"Restore complete. All packages installed.")
    
    except subprocess.CalledProcessError as e:
        print(f"Error during restore: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"Backup file {backup_file} not found.")
        sys.exit(1)

def main():
    if len(sys.argv) != 3:
        print("Usage: python flatpak_backup.py <backup|restore> <backup_file>")
        sys.exit(1)

    action = sys.argv[1]
    backup_file = sys.argv[2]

    if action == 'backup':
        backup_flatpak_packages(backup_file)
    elif action == 'restore':
        restore_flatpak_packages(backup_file)
    else:
        print("Invalid action. Use 'backup' or 'restore'.")
        sys.exit(1)

if __name__ == '__main__':
    main()
