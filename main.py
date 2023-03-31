import os
from sys import exit
import os.path as path
import tomllib

project_root = os.getcwd()
config = {}
# STARTVEXDOC
# TITLE Config Parsing
"""startsummary
This section handles parsing the config file,
and creating one if does not exist.
endsummary"""
try:
    with open('VexDoc.toml', 'rb') as config:
        config = tomllib.load(config)
except FileNotFoundError:
    print("No config file found, creating one...")
    single_comments = input("""\
Please enter the characters used to denote \
a single-line comment in this project's language \
(this is how VexDoc will detect when to start documenting):\n
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
        config = tomllib.load(config)

target_files = []
# ENDVEXDOC

# STARTVEXDOC
# TITLE File Parsing
"""startsummary
This next part loops through all files in the project directory,
checking them against the config file to make sure everything matches up
endsummary"""
try:
    for directory, subdirectories, files in os.walk(project_root):
        if config["using_git"]:
            if '.git' in directory:
                continue
        if path.basename(directory) in config["ignored_dirs"] or path.basename(directory) == 'docs':
            continue
        # print(f'{directory}\n{subdirectories}\n{files}')
        for file in files:
            if file[file.rindex('.'):] in config["file_extensions"]:
                target_files.append(path.join(path.relpath(directory), file))
except KeyError:
    print("Error. Please verify your configuration file is correctly written")
    exit(1)
# ENDVEXDOC

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
<!DOCTYPE html>
<html>
    <head>
        <title>Docs from {name+extension}</title>
        <link rel="stylesheet" href="https://cdn.simplecss.org/simple.min.css">
        <style>
            code {{
                font-size: 0.9rem;
            }}
            body {{
                grid-template-columns: 1fr 90% 1fr;
            }}
        </style>
    </head>
    <body>
        <header>
            <h1>Documentation from {name+extension}</h1>
        </header>
        <p>The following code is found at {project_root + file[1:]}</p>
"""
        )
        reading_vexdoc = False
        reading_summary = False
        for line in input_file:
            if line == f'{config["single_comments"]}STARTVEXDOC\n':
                reading_vexdoc = True
                output_file.write(
                    """
        <section>
"""
                )
                continue
            elif line == f"{config['single_comments']}ENDVEXDOC\n":
                output_file.write(
                    """\
            </code></pre>
        </section>
"""
                )
                reading_vexdoc = False

            if reading_vexdoc:
                if line.startswith(f"{config['single_comments']}TITLE"):
                    output_file.write(
                        f"<h2>{line[len(config['single_comments']+'TITLE'):len(line)-1]}</h2>\n")
                    continue
                elif line.lower().startswith(f"{config['multi_comments'][0]}startsummary"):
                    reading_summary = True
                    output_file.write(
                        """
            <p>
"""
                    )
                    continue
                elif line.lower().startswith(f"endsummary{config['multi_comments'][-1]}"):
                    reading_summary = False
                    output_file.write(
                        """
            </p>
            <pre><code>\
"""
                    )
                    continue

                output_file.write(f"{line}")
