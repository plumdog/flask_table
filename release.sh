#!/bin/bash

set -e


function error() {
    >&2 echo "$1"
    exit 1
}

function confirm() {
    read -r -p "Are you sure? [Y/n] " response
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
    sed -i '/Build Status.*Coverage Status/,+1d' README
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

    git add setup.py
    git commit -m "Bump to version $new"
    git push origin master
    git tag -a "v$new" -m "Version $new"
    git push origin "v$new"
}

function publish() {
    generate_readme

    echo "Ready publish to PyPI."
    confirm
    python setup.py sdist upload -r pypi
}

main $@
