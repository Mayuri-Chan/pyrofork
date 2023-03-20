import datetime
import random
import re
import string

with open("pyrogram/__init__.py", "r") as f:
    pyro_version = re.findall(r"__version__ = \"(.+)\"", f.read())[0]
    date = datetime.datetime.now().strftime("%Y%m%d")
    dev_version = ''.join(random.choice(string.digits) for i in range(4))
    version = f"{pyro_version}.dev{date}{dev_version}"

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
        f.write(line)
