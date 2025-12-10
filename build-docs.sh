#!/bin/bash

# Check if config.sh exists
if [ -f config.sh ]; then
    source config.sh
fi

function parse_parameters() {
    while (($#)); do
        case $1 in
            all | configure | cleanup | virtualenv | build | clone | push ) action=$1 ;;
            *) exit 33 ;;
        esac
        shift
    done
}

function do_configure() {
    echo "#!/bin/bash" > config.sh
    echo "export VENV=\"$(pwd)/venv\"" >> config.sh

    if [[ "$(echo "$GITHUB_REF" | cut -d '/' -f "1 2")" == "refs/tags" ]]; then
        echo "export BRANCH=\"main\"" >> config.sh
    elif [[ "$GITHUB_REF" == "refs/heads/staging" ]]; then
        echo "export BRANCH=\"staging\"" >> config.sh
    else
        b="$(echo "$GITHUB_REF" | cut -d '/' -f '3 4')"
        if [[ $(echo "$b" | cut -d '/' -f 1 ) == "dev" ]]; then
            b="$(echo "$b" | cut -d '/' -f 2)"
            if [[ "$b" =~ ^[0-9]\.[0-9]\.x ]]; then
                echo "export BRANCH=\"$b\"" >> config.sh
            else
                exit 0
            fi
        else
            exit 0
        fi
    fi
    chmod +x config.sh
}

function do_cleanup() {
    make clean
    make clean-docs
}

function do_virtualenv() {
    make venv
    make api
    "$VENV"/bin/pip install -e '.[docs]'
}

function do_build() {
    cd compiler/docs || exit 1 && "$VENV"/bin/python compiler.py
    cd  ../.. || exit 1
    "$VENV"/bin/sphinx-build -b html "docs/source" "docs/build/html" -j auto
}

function do_clone() {
    git clone https://wulan17:"$DOCS_KEY"@github.com/Mayuri-Chan/pyrofork-docs.git
}

function do_push() {
    cd pyrofork-docs || exit 1
    mkdir -p "$BRANCH"
    cd "$BRANCH" || exit 1
    rm -rf _includes api genindex.html intro py-modindex.html sitemap.xml support.html topics _static faq index.html objects.inv searchindex.js start telegram
    cp -r ../../docs/build/html/* .
    git config --local user.name "Mayuri-Chan"
    git config --local user.email "mayuri@mayuri.my.id"
    git add --all
    git commit -a -m "docs: $BRANCH: Update docs $(date '+%Y-%m-%d | %H:%m:%S %p %Z')" --signoff
    git push -u origin --all
}

function do_all() {
    do_configure
    source config.sh
    do_cleanup
    do_virtualenv
    do_build
    do_clone
    do_push
}

parse_parameters "$@"
do_"${action:=all}"
