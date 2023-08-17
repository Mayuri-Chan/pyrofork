#!/bin/bash
export DOCS_KEY
export VENV=$(pwd)/venv

make clean
make clean-docs
make venv
make api
"$VENV"/bin/pip install -r docs/requirements.txt
cd compiler/docs && "$VENV"/bin/python compiler.py
cd ../..
"$VENV"/bin/sphinx-build -b html "docs/source" "docs/build/html" -j auto
git clone https://wulan17:"$DOCS_KEY"@github.com/Mayuri-Chan/pyrofork-docs.git
cp -r docs/build/html/* pyrofork-docs
cd pyrofork-docs
git config --local user.name "Mayuri-Chan"
git config --local user.email "mayuri@mayuri.my.id"
git add --all
git commit -a -m "docs: Update docs $(date '+%Y-%m-%d | %H:%m:%S %p %Z')" --signoff
git push -u origin --all
