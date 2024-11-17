#!/bin/bash
path=$1

cd $path
rm -rf "enterprise-attack"

git init
git remote add origin https://github.com/mitre/cti.git
git sparse-checkout init --cone
git sparse-checkout set enterprise-attack

git pull origin master

if [ $? -ne 0 ]; then
    git pull origin main
fi

rm -rf ".git"
rm -rf "CHANGELOG.md"
rm ".gitignore"
rm "LICENSE.txt"
rm "README.md"
rm "USAGE-CAPEC.md"
rm "USAGE.md"
