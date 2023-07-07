#! /usr/bin/env bash
python3 $(dirname "$0")/parse_article.py
python3 $(dirname "$0")/parse_teams.py
python3 $(dirname "$0")/parse_index.py
