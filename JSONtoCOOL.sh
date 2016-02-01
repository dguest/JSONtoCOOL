#!/usr/bin/env bash

set -eu

ROOT_DB_FILE=BTagCalibRUN2-08-14_inclDL1.root
TAG_NAME=BTagCalibRUN2-08-14_inclDL1

# arg 1 is the calibration file, arg 2 is the json file

DIR=$(dirname $0)
if [[ $# == 2 ]]; then
    NEW_ROOT_FILE=${1%%.json}.root
    python $DIR/JSONtoCOOL_converter.py $2 2> /dev/null
    hadd $ROOT_DB_FILE $NEW_ROOT_FILE $1 2> /dev/null
elif [[ $# == 1 ]]; then
    cp $1 $ROOT_DB_FILE
else
    echo "usage $0 <base root file> [<json file to add>]"
    exit 1
fi

# Associate a GUID to this file
coolHist_setFileIdentifier.sh $ROOT_DB_FILE
# Insert the calibration ROOT file into a local COOL file catalogue:
coolHist_insertFileToCatalog.py $ROOT_DB_FILE

# Generate a local database
coolHist_setReference.py OFLP200 /GLOBAL/BTagCalib/RUN12 1 $TAG_NAME $ROOT_DB_FILE

# Open it to define it's channel
expect <<EOF
spawn AtlCoolConsole.py "sqlite://;schema=mycool.db;dbname=OFLP200"
expect ">>>"
send "setchan /GLOBAL/BTagCalib/RUN12 1 RUN12\n"
expect ">>>"
send "exit\n"
expect eof
EOF

