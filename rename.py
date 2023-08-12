from genericpath import isfile
import os

CACHE_FOLDER = "rename_cache"

def create_cache_folder():
    if not os.path.exists(CACHE_FOLDER):
        os.mkdir(CACHE_FOLDER)

def save_cache(original_names, group_name):
    create_cache_folder()
    cache_file = os.path.join(CACHE_FOLDER, f"{group_name}_cache.txt")
    with open(cache_file, "w") as f:
        for new_name, old_name in original_names.items():
            f.write(f"{new_name},{old_name}\n")

def load_cache(group_name):
    cache_file = os.path.join(CACHE_FOLDER, f"{group_name}_cache.txt")
    original_names = {}
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            lines = f.readlines()
            for line in lines:
                new_name, old_name = line.strip().split(',')
                original_names[new_name] = old_name
    return original_names

def display_history(original_names, folder_path):
    print("===== History of Changed Names =====")
    for new_name, old_name in original_names.items():
        old_file_path = os.path.join(folder_path, old_name)
        new_file_path = os.path.join(folder_path, new_name)
        print(f"{new_name} (Old: {old_name})")
        print(f"  Location: {old_file_path}")
        print()

def list_cache_groups():
    print("===== List of Cache Groups =====")
    cache_files = [f for f in os.listdir(CACHE_FOLDER) if f.endswith("_cache.txt")]
    for cache_file in cache_files:
        group_name = cache_file.replace("_cache.txt", "")
        print(group_name)
        
def list_files_in_folder(folder_path):
    print(f"===== Files in {folder_path} =====")
    files = os.listdir(folder_path)
    for file_name in files:
        full_path = os.path.join(folder_path, file_name)
        if os.path.isfile(full_path):
            print(file_name)
            
def rename_files(folder_path, change_type, num_chars=0, substring_to_remove="", group_name="default"):
    # Get a list of all files in the folder
    files = os.listdir(folder_path)

    # Dictionary to store original filenames
    original_names = load_cache(group_name)

    # Iterate over each file in the folder
    for file_name in files:
        if os.path.isfile(os.path.join(folder_path, file_name)):
            base_name, extension = os.path.splitext(file_name)
            
            if change_type == "remove_front":
                new_file_name = base_name[num_chars:] + extension  
            elif change_type == "remove_back":
                new_file_name = base_name + extension[:-num_chars]  
            elif change_type == "edit":
                new_base_name = input(f"Enter new base name for '{file_name}' (press Enter to keep original): ")
                if not new_base_name:
                    new_file_name = file_name
                else:
                    new_file_name = new_base_name + extension
            elif change_type == "remove_substring":
                new_file_name = base_name.replace(substring_to_remove, "") + extension
            else:
                print("Invalid change type.")
                return
            
            old_file_path = os.path.join(folder_path, file_name)
            new_file_path = os.path.join(folder_path, new_file_name)
            
            # Check if the destination file already exists before renaming
            if os.path.exists(new_file_path):
                print(f"File '{new_file_name}' already exists. Skipping renaming.")
            else:
                original_names[new_file_name] = file_name  # Store the original filename
                try:
                    os.rename(old_file_path, new_file_path)
                    print(f'Renamed {file_name} to {new_file_name}')
                except Exception as e:
                    print(f"Error renaming {file_name}: {e}")

    save_cache(original_names, group_name)

    return original_names

def revert_rename(folder_path, group_name):
    original_names = load_cache(group_name)
    for new_name, old_name in original_names.items():
        old_file_path = os.path.join(folder_path, new_name)
        new_file_path = os.path.join(folder_path, old_name)
        try:
            os.rename(old_file_path, new_file_path)
            print(f'Reverted {new_name} to {old_name}')
        except Exception as e:
            print(f"Error reverting {new_name}: {e}")

def delete_cache(group_name):
    cache_file = os.path.join(CACHE_FOLDER, f"{group_name}_cache.txt")
    if os.path.exists(cache_file):
        os.remove(cache_file)
        print(f"Cache for group '{group_name}' deleted.")

def main():
    folder_path = r'Input'  # Replace with the path to your folder

    while True:
        # Menu screen
        print("===== File Renaming Menu =====")
        print("1. Rename files - Remove letters from the front")
        print("2. Rename files - Remove letters from the back")
        print("3. Rename files - Edit filenames")
        print("4. Rename files - Remove substring from filenames")
        print("5. Revert renaming")
        print("6. Display history of changed names")
        print("7. Delete cache for group")
        print("8. List cache groups")
        print("9. List files in folder")
       
        print("10. Quit")

        # Process user input
        choice = input("Enter your choice (1-11): ")

        if choice == "1":
            num_chars = int(input("Enter the number of characters to remove from the front: "))
            group_name = input("Enter group name (default if empty): ")
            original_names = rename_files(folder_path, "remove_front", num_chars, group_name=group_name)

        elif choice == "2":
            num_chars = int(input("Enter the number of characters to remove from the back: "))
            group_name = input("Enter group name (default if empty): ")
            original_names = rename_files(folder_path, "remove_back", num_chars, group_name=group_name)

        elif choice == "3":
            group_name = input("Enter group name (default if empty): ")
            original_names = rename_files(folder_path, "edit", group_name=group_name)

        elif choice == "4":
            substring_to_remove = input("Enter the substring to remove from filenames: ")
            group_name = input("Enter group name (default if empty): ")
            original_names = rename_files(folder_path, "remove_substring", 0, substring_to_remove, group_name=group_name)

        elif choice == "5":
            group_name = input("Enter group name (default if empty): ")
            revert_rename(folder_path, group_name)
            print("Reversion completed.\n")

        elif choice == "6":
            group_name = input("Enter group name (default if empty): ")
            original_names = load_cache(group_name)
            display_history(original_names, folder_path)

        elif choice == "7":
            group_name = input("Enter group name (default if empty): ")
            delete_cache(group_name)

        elif choice == "8":
            list_cache_groups()

        elif choice == "9":
            list_files_in_folder(folder_path)

        elif choice == "10":
            # Quit the program
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please enter a valid option.\n")

if __name__ == "__main__":
    main()