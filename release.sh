#!/bin/bash

set -e


function error() {
    >&2 echo "$1"
    exit 1
}

function confirm() {
    msg="$1"
    if [[ -z "$msg" ]]; then
        msg="Are you sure?"
    fi
    read -r -p "$msg [Y/n] " response
    case $response in
        [yY][eE][sS]|[yY]|"")
            return
            ;;
        *)
            error "Abort."
            ;;
    esac
}


function main() {
    arg="$1"

    if [[ $# -eq 0 ]]; then
        error "No command given."
    fi

    case $arg in
        tag)
            tag "$2"
            exit 0;
            ;;
        publish)
            publish
            exit 0;
            ;;
        _generate_readme)
            generate_readme
            exit 0;
            ;;
        *)
            error "Unrecognised argument: $arg. Choose from tag,publish"
            ;;
    esac
}


function _trim_from_upto() {
    fname="$1"
    from="$2"
    upto="$3"

    from_line="$(grep -n "$from" "$fname" | sed 's/\:.*//')"
    upto_line="$(grep -n "$upto" "$fname" | sed 's/\:.*//')"

    if [[ -z $from_line ]]; then error "Unable to find $from in $fname"; fi
    if [[ -z $upto_line ]]; then error "Unable to find $upto in $fname"; fi

    upto_line=$(($upto_line-1))

    sed -i "$from_line,${upto_line}d" "$fname"
}


function generate_readme() {
    pandoc --from=markdown --to=rst --output=README README.md || error "Unable to convert README.md"
    # Remove the Github status links
    sed -i '/Build Status.*Coverage Status.*PyPI/,+1d' README
    # And remove a big chunk of html that gets a bit exploded
    _trim_from_upto README "Or as HTML:" "Extra things:"
}


function tag() {
    up="${1:-patch}"
    
    [[ "$(git rev-parse --abbrev-ref HEAD)" == master ]] || error "Must be on master to tag."

    git diff-files --quiet || error "Working directory must be clean to tag"

    current="$(grep version setup.py | sed 's/^.*=//' | sed 's/,$//' | sed "s/['\"]//g")"
    re='\([0-9]\+\)\.\([0-9]\+\)\.\([0-9]\+\)'
    major="$(echo $current | sed "s/$re/\1/")"
    minor="$(echo $current | sed "s/$re/\2/")"
    patch="$(echo $current | sed "s/$re/\3/")"

    echo "Parsed current version as: $major.$minor.$patch"

    case $up in
        patch)
            patch=$(($patch+1))
            ;;
        minor)
            minor=$(($minor+1))
            patch=0
            ;;
        major)
            major=$(($major+1))
            minor=0
            patch=0
            ;;
        *)
            error "Unknown version section to increase: $up. Please select from: major,minor,patch."
            ;;
    esac

    new="$major.$minor.$patch"

    echo "Ready to tag new version $new."
    confirm

    sed -i "s/$current/$new/" setup.py

    underline="$(echo "$new" | sed 's/./-/g')"
    log="$(git log "$(git describe --tags --abbrev=0)..." --pretty=format:'%s' --reverse | while read line; do echo "- $line"; done)"
    changelog_entry="$new
$underline
$log
"

    touch CHANGELOG.md
    cat <(echo "$changelog_entry") CHANGELOG.md > CHANGELOG.md.new
    mv CHANGELOG.md.new CHANGELOG.md

    echo "CHANGES:"
    echo "$log"
    echo "/CHANGES"

    confirm "Written changes to CHANGELOG.md, but not yet added. Edit there and then continue."

    git add setup.py CHANGELOG.md
    git commit -m "Bump to version $new"
    git push origin master
    git tag -a "v$new" -m "Version $new"
    git push origin "v$new"
}

function publish() {
    generate_readme

    echo "Ready publish to PyPI."
    confirm
    rm -rf dist
    python setup.py sdist
    twine upload dist/Flask-Table-*.tar.gz
}

main $@
