import datetime
import re
import string

with open("pyrogram/__init__.py", "r") as f:
    pyro_version = re.findall(r"__version__ = \"(.+)\"", f.read())[0]
    date = datetime.datetime.now().strftime("%Y%m%d%H%M")
    version = f"{pyro_version}.dev{date}"

with open("pyrogram/__init__.py", "r") as f:
    lines = f.readlines()

with open("pyrogram/__init__.py", "w") as f:
    for line in lines:
        line = re.sub(r'__fork_name__ = "PyroFork"', '__fork_name__ = "PyroFork-dev"', line)
        line = re.sub(r'^__version__ = "'+ pyro_version +'"', '__version__ = "'+ version +'"', line)
        f.write(line)

with open("setup.py", "r") as f:
    lines = f.readlines()

with open("setup.py", "w") as f:
    for line in lines:
        line = re.sub(r'    name="PyroFork"', '    name="PyroFork-dev"', line)
        line = re.sub(r'        "Development Status :: 5 - Production/Stable"', '        "Development Status :: 4 - Beta"', line)
        f.write(line)
