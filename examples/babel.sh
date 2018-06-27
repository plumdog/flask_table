#!/bin/bash

BABEL=pybabel
TEMPLATE_FILE=messages.pot
TRANSLATIONS_DIR=translations

if [[ "$1" = "lninit" ]]; then
	$BABEL init -i $TEMPLATE_FILE -d $TRANSLATIONS_DIR -l de -l en_GB
elif [[ "$1" = "lnupdate" ]]; then
	$BABEL extract -F babel.cfg -o $TEMPLATE_FILE
	$BABEL update -i $TEMPLATE_FILE -d $TRANSLATIONS_DIR
elif [[ "$1" = "lncompile" ]]; then
	$BABEL compile -f -d $TRANSLATIONS_DIR
fi
