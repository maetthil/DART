#! /bin/bash

EXPORT_DIR='export/'
TAG=$1
DATA=$2

mkdir -p $EXPORT_DIR;
docker run -it --rm \
-v "/$(pwd)/$DATA:/usr/src/app/dart/data/" \
-v "$(pwd)/$EXPORT_DIR:/usr/src/app/dart/export" \
--rm $TAG
