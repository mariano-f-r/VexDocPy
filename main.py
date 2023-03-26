import os
import os.path as path
import tomllib

project_root = os.getcwd()
data = {}
try:
    with open('VexDoc.toml', 'rb') as config:
        data = tomllib.load(config)
except FileNotFoundError:
    print("No config file found, creating one...")
    single_comments = input("""\
Please enter the characters used to denote \
a single-line comment in this project's language:\n
""")
    multi_comments = input("""\
Please enter the characters used to denote \
a multi-line comment in this project's language (separated by spaces if there are 2):\n
""").split()

    file_extension = input("""\
Please enter the file extension separated by spaces\n
    """).split()
    with open('VexDoc.toml', 'w') as config:
        config.write(
            f'single_comments = "{single_comments}"\nmulti_comments = {multi_comments}\nignored_dirs = []\nfile_extensions = {file_extension}\n')
        if path.exists(".git/"):
            config.write('using_git = true\n')

    with open('VexDoc.toml', 'rb') as config:
        data = tomllib.load(config)

target_files = []

try:
    for directory, subdirectories, files in os.walk(project_root):
        if data["using_git"]:
            if '.git' in directory:
                continue
        if path.basename(directory) in data["ignored_dirs"] or path.basename(directory) == 'docs':
            continue
        # print(f'{directory}\n{subdirectories}\n{files}')
        for file in files:
            if file[file.rindex('.'):] in data["file_extensions"]:
                target_files.append(path.join(path.relpath(directory), file))
except TypeError:
    print("Error. Please verify your configuration file is correctly written")

print(target_files)

if not path.exists(path.join(project_root, "docs/")):
    os.mkdir(path.join(project_root, "docs"))

for file in target_files:
    name, extension = path.splitext(path.basename(file))
    if not path.exists(path.join(project_root, 'docs', path.dirname(file))):
        os.makedirs(path.join(project_root, 'docs', path.dirname(file)))
    with open(path.join(project_root, file), 'r') as input_file, \
            open(path.join(project_root, 'docs/', path.dirname(file), name+'_'+extension[1:]+'_documentation.html'), 'w') as output_file:
        output_file.write(
            f"""
<html>
    <head>
        <title>VexDoc</title>
        <link rel="stylesheet" href="https://cdn.simplecss.org/simple.min.css">
    </head>
    <body>
        <header>
            <h1>Documentation from {name+extension}</h1>
        </header>
    </body>
</html>
"""
        )
        # for line in input_file:
        # print(line)
