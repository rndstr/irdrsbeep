#!/bin/sh
set -e
[[ $# -ne 1 ]] && { echo "missing version"; exit 1; }

NAME="irdrsbeep"
ZIP="$NAME-v$1-bin.zip"

# clean
rm -rf $NAME $ZIP
mkdir $NAME
pyinstaller --onefile irdrsbeep.py --distpath .
cp irdrsbeep.exe irdrsbeep.ini README.md $NAME
zip $ZIP $NAME/*

