# VexDoc

VexDoc is a small Python script (<150 LOC) meant to help my Vex Robotics team and others at my school easily print out documentation for code to go in their engineering notebooks, as well as making documentation easy (by letting you do it as you go).
It relies only on the standard Python library, to make it as portable as possible (a future version will be written in Rust to improve this).

## Installation
Please ensure you have a version of Python installed. If you are on Linux like me, you do not have to worry.
Otherwise, please make your way to [the official Python website](https://python.org) and install the appropriate executable.

Once you have done that, open the terminal and clone the repository in a location OUTSIDE the project you wish to document by running this command:
```
git clone https://github.com/sergeant-savage/VexDocPy.git
```

## First Run
Once you have the script on your system, change your current directory to the root of the project you wish to document.
Now, run the script by running this command, substituting the directory for the appropriate one:
```
python3 <absolute or relative path to script>
```

At this point, VexDoc will scaffold out a config file if none is found.
VexDoc's config is written in [TOML](https://toml.io) and has 5 fields:
| Key   | Meaning   |
|--------------- | --------------- |
| `single_comments` | This value is what VexDoc looks for when starting a documentation block, reading the title of a documentation block, and ending a documentation block |
| `multi_comments` | This value(s) are used by VexDoc to determine where the description for a documentation block starts and ends, as well as containing said description |
| `ignored_dirs`   | These are directories that VexDoc ignores. They can be anywhere, although due to the newness of this project, only top level directories have been confirmed to work. |
| `file_extensions` | These are the extensions of the files VexDoc will target |
| `using_git` | A boolean to check if git VCS is being used |

Here is a sample config I used to document this project (using this project) in VexDoc:
```toml
single_comments = "#"
multi_comments = ['"""']
ignored_dirs = []
file_extensions = ['.py']
using_git = true
```

Once your config file has been created and modified to your liking you can begin documenting.

## Writing the Documentation

For this example, let's consider an imaginary file: `fizz.py`.
`fizz.py` contains the following:
```python
def foo():
  print("Foo!")

def bar():
  print("Bar!")
```

VexDoc extracts the documentation from a file in so-called "documentation blocks".
These blocks contain a title, a summary of the code (the actual documentation), and the code being documented.
To create a documentation block, write a single line comment at the start containing a space, and "STARTVEXDOC" (The space is important, as otherwise VexDoc will not work).
At the end of the area that you want to document this, do the same, except replacing "STARTVEXDOC" with end "ENDVEXDOC" (Once again, make sure there is a space)

This is what `fizz.py` looks like after doing this for the `foo` function:
```python
# STARTVEXDOC
def foo():
  print("Foo!")
# ENDVEXDOC

def bar():
  print("Bar!")
```

Next, beneath the start of the documentation block, create a new singe line comment that contains a space, and "TITLE" (Once more, the space is important).
After the word "TITLE", you can add the title of the documentation block.
`fizz.py` will now look like this:
```python
# STARTVEXDOC
# TITLE Documentation for the foo() function
def foo():
  print("Foo!")
# ENDVEXDOC

def bar():
  print("Bar!")
```

Finally, create a multiline comment starting with "startsummary" (no space this time) and ending with "endsummary". 
Within these 2 lines, you can write the actual documentation.
`fizz.py` will now look like this:
```python
# STARTVEXDOC
# TITLE Documentation for the foo() function
"""startsummary
The foo function prints Foo!
endsummary"""
def foo():
  print("Foo!")
# ENDVEXDOC

def bar():
  print("Bar!")
```

You can repeat this as many times as you want per file for as many files as needed.
Once you are done, simply rerun the script, and documentation will be generated in the `docs/` folder.

# License
Licensed GPL-3
