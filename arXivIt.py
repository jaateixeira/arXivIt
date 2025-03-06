import os
import re
import tarfile
import shutil
import argparse
from pathlib import Path

# Valid file extensions
VALID_TEX_EXTENSIONS = {".tex", ".bbl", ".bib"}
VALID_FIGURE_EXTENSIONS = {".ps", ".eps", ".jpeg", ".jpg", ".gif", ".png", ".pdf"}

# arXiv filename requirements
ARXIV_FILENAME_REGEX = re.compile(r"^[a-zA-Z0-9_.-]+$")

def validate_sources_and_figures(folder):
    """
    Validate LaTeX sources and figures in the folder.
    """
    for root, _, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root, file)
            ext = os.path.splitext(file)[1].lower()

            # Check for valid LaTeX sources
            if ext in VALID_TEX_EXTENSIONS:
                if not os.path.getsize(file_path) > 0:
                    print(f"Warning: Empty file detected: {file_path}")
                continue

            # Check for valid figures
            if ext in VALID_FIGURE_EXTENSIONS:
                if not os.path.getsize(file_path) > 0:
                    print(f"Warning: Empty file detected: {file_path}")
                continue

            # If the file is not a valid source or figure, warn the user
            print(f"Warning: Invalid file format: {file_path}")

def flatten_tex_file(main_tex_path):
    """
    Flatten the main .tex file by combining all \input and \include statements.
    """
    with open(main_tex_path, "r") as f:
        content = f.read()

    def replace_input_include(match):
        include_file = match.group(1)
        include_path = os.path.join(os.path.dirname(main_tex_path), include_file)
        if os.path.exists(include_path):
            with open(include_path, "r") as f:
                return f.read()
        else:
            print(f"Warning: File not found: {include_path}")
            return ""

    # Replace \input and \include statements
    content = re.sub(r"\\input\{(.*?)\}", replace_input_include, content)
    content = re.sub(r"\\include\{(.*?)\}", replace_input_include, content)

    # Write the flattened content back to the main .tex file
    with open(main_tex_path, "w") as f:
        f.write(content)

def check_filenames(folder):
    """
    Check that filenames comply with arXiv's strict requirements.
    """
    for root, _, files in os.walk(folder):
        for file in files:
            if not ARXIV_FILENAME_REGEX.match(file):
                print(f"Error: Invalid filename: {file}")
                raise ValueError(f"Filename '{file}' does not comply with arXiv requirements.")

def remove_unused_files(folder, main_tex_path):
    """
    Remove files not referenced by the main .tex file.
    """
    with open(main_tex_path, "r") as f:
        content = f.read()

    referenced_files = set()
    for root, _, files in os.walk(folder):
        for file in files:
            if file in content:
                referenced_files.add(os.path.join(root, file))

    for root, _, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root, file)
            if file_path not in referenced_files and file != os.path.basename(main_tex_path):
                print(f"Removing unused file: {file_path}")
                os.remove(file_path)

def replace_symlinks(folder):
    """
    Replace symbolic links with hard copies.
    """
    for root, _, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.islink(file_path):
                target_path = os.path.realpath(file_path)
                print(f"Replacing symlink: {file_path} -> {target_path}")
                os.unlink(file_path)
                shutil.copy2(target_path, file_path)

def remove_hidden_files(folder):
    """
    Remove hidden files and directories (e.g., .gitignore).
    """
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.startswith("."):
                file_path = os.path.join(root, file)
                print(f"Removing hidden file: {file_path}")
                os.remove(file_path)
        for dir in dirs:
            if dir.startswith("."):
                dir_path = os.path.join(root, dir)
                print(f"Removing hidden directory: {dir_path}")
                shutil.rmtree(dir_path)

def validate_bbl_file(folder, main_tex_path):
    """
    Ensure the .bbl file matches the name of the main .tex file.
    """
    main_tex_name = os.path.splitext(os.path.basename(main_tex_path))[0]
    bbl_file = os.path.join(folder, f"{main_tex_name}.bbl")
    if not os.path.exists(bbl_file):
        print(f"Error: .bbl file not found: {bbl_file}")
        raise FileNotFoundError(f".bbl file '{bbl_file}' does not exist.")

def create_tar_file(folder, output_path):
    """
    Create a .tar file from the folder.
    """
    with tarfile.open(output_path, "w:gz") as tar:
        tar.add(folder, arcname=os.path.basename(folder))

def main():
    parser = argparse.ArgumentParser(description="Prepare a LaTeX project for arXiv submission.")
    parser.add_argument("folder", help="Path to the LaTeX project folder.")
    args = parser.parse_args()

    folder = args.folder
    main_tex_path = os.path.join(folder, "main.tex")  # Assume main.tex is the main file

    if not os.path.exists(main_tex_path):
        raise FileNotFoundError(f"Main .tex file not found: {main_tex_path}")

    print("Validating sources and figures...")
    validate_sources_and_figures(folder)

    print("Flattening main .tex file...")
    flatten_tex_file(main_tex_path)

    print("Checking filenames...")
    check_filenames(folder)

    print("Removing unused files...")
    remove_unused_files(folder, main_tex_path)

    print("Replacing symlinks...")
    replace_symlinks(folder)

    print("Removing hidden files...")
    remove_hidden_files(folder)

    print("Validating .bbl file...")
    validate_bbl_file(folder, main_tex_path)

    print("Creating .tar file...")
    output_tar_path = f"{folder}_arxiv.tar.gz"
    create_tar_file(folder, output_tar_path)

    print(f"Done! arXiv-ready .tar file created: {output_tar_path}")

if __name__ == "__main__":
    main()
