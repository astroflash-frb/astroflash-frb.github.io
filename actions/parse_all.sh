#! /usr/bin/env bash


if [ $(basename "$PWD") != "actions" ];then
    WD=..
    cd actions
else
    WD=.
fi

python3 parse_article.py
python3 parse_teams.py
python3 parse_index.py

cd $WD

