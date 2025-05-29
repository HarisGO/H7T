# tools/project_initializer.py

import os

def main():
    """
    Initializes a new project with a basic directory structure.
    """
    print("--- Project Initializer ---")

    project_name = input("Enter the project name: ").strip()
    if not project_name:
        print("Project name cannot be empty. Aborting.")
        return

    author_name = input("Enter the author's name (optional): ").strip()

    print(f"\nCreating project '{project_name}'...")

    try:
        # Create root project directory
        os.makedirs(project_name, exist_ok=True)
        print(f"  Created directory: {project_name}/")

        # Define common subdirectories
        subdirs = ['src', 'tests', 'docs', 'assets']
        for subdir in subdirs:
            path = os.path.join(project_name, subdir)
            os.makedirs(path, exist_ok=True)
            print(f"  Created directory: {project_name}/{subdir}/")

        # Create README.md
        readme_path = os.path.join(project_name, 'README.md')
        with open(readme_path, 'w') as f:
            f.write(f"# {project_name}\n\n")
            if author_name:
                f.write(f"Author: {author_name}\n\n")
            f.write("## Overview\n\n[Add project description here]\n\n")
            f.write("## Setup\n\n```bash\n# Installation steps\n```\n\n")
        print(f"  Created file: {project_name}/README.md")

        # Create a basic .gitignore
        gitignore_path = os.path.join(project_name, '.gitignore')
        with open(gitignore_path, 'w') as f:
            f.write("# Python\n")
            f.write("__pycache__/\n")
            f.write("*.pyc\n")
            f.write("*.pyo\n")
            f.write("*.pyd\n")
            f.write(".Python\n")
            f.write("env/\n")
            f.write("venv/\n")
            f.write("*.egg-info/\n")
            f.write(".pytest_cache/\n")
            f.write("\n# OS specific\n")
            f.write(".DS_Store\n")
            f.write("Thumbs.db\n")
        print(f"  Created file: {project_name}/.gitignore")

        print(f"\nProject '{project_name}' successfully initialized!")
        print(f"You can find it at: {os.path.abspath(project_name)}")

    except Exception as e:
        print(f"An error occurred during project initialization: {e}")

# Do NOT call main() here. H7T does that automatically.
