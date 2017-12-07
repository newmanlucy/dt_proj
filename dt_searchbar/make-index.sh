#!/bin/bash

echo "indexing files..."

printf -v FILES %s "$(./make-json.py $1)"

#echo $FILES

echo $FILES | node build-index.js > index.json

echo "index successfully created"
