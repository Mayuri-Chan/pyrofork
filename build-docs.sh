#!/bin/bash
export DOCS_KEY
export VENV=$(pwd)/venv

make clean
make clean-docs
make venv
make api
"$VENV"/bin/pip install -e '.[docs]'
cd compiler/docs && "$VENV"/bin/python compiler.py
cd ../..
"$VENV"/bin/sphinx-build -b html "docs/source" "docs/build/html" -j auto
git clone https://wulan17:"$DOCS_KEY"@github.com/Mayuri-Chan/pyrofork-docs.git
cd pyrofork-docs
refs=$(echo "$GITHUB_REF" | cut -d '/' -f "1 2") 
if [[ "$refs" == "refs/tags" ]]; then
    mkdir -p main
    cd main
    rm -rf _includes api genindex.html intro py-modindex.html sitemap.xml support.html topics _static faq index.html objects.inv searchindex.js start telegram
    cp -r ../../docs/build/html/* .
else
    mkdir -p staging
    cd staging
    rm -rf _includes api genindex.html intro py-modindex.html sitemap.xml support.html topics _static faq index.html objects.inv searchindex.js start telegram
    cp -r ../../docs/build/html/* .
fi
git config --local user.name "Mayuri-Chan"
git config --local user.email "mayuri@mayuri.my.id"
git add --all
git commit -a -m "docs: $(echo $GITHUB_REF | cut -d '/' -f 3): Update docs $(date '+%Y-%m-%d | %H:%m:%S %p %Z')" --signoff
git push -u origin --all
