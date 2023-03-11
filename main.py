import os

project_root = os.getcwd()
target_files = []

for directory, subdirectories, files in os.walk(project_root):
    print(f'{directory}\n{subdirectories}\n{files}')
    for file in files:
        target_files.append(os.path.join(directory, file))

print(target_files)
