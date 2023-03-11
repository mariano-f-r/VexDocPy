import os
import os.path as path
import tomllib

project_root = os.getcwd()
data = {}
try:
    with open('Vexcode.toml', 'rb') as config:
        data = tomllib.load(config)
except FileNotFoundError:
    print("No config file found, creating one...")
    comments = input("""
                     Please enter the characters used to denote
                     a comment in this project's language:\n
                """)
    with open('Vexcode.toml', 'w') as config:
        config.write(
            f'comments = "{comments}"\nignored_dirs = []\nignored_files = []\n')
        if path.exists(".git/"):
            config.write('using_git = true\n')

    with open('Vexcode.toml', 'rb') as config:
        data = tomllib.load(config)

target_files = []

try:
    for directory, subdirectories, files in os.walk(project_root):
        if data["using_git"]:
            if '.git' in directory:
                continue
        if path.basename(directory) in data["ignored_dirs"]:
            continue
        print(f'{directory}\n{subdirectories}\n{files}')
        for file in files:
            target_files.append(path.join(directory, file))
except TypeError:
    print("Error. Please verify your configuration file is correctly written")

print(data)
print(target_files)
