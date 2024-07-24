# This is the main (Snake)Make file to propagate updates of the AstroFlash Website

import os
import glob
import subprocess

# Get all YAML files in the posts directory
blog_entries = [p for p in Path().glob("posts/*.yaml") if "template" not in p.name]
team_entries = [p for p in Path().glob("team/*.yaml") if "template" not in p.name]
# team_existing = [surname for surname in [t.name.replace('.yaml', '') for t in team_entries] \
#                  if subprocess.run(["grep", surname, "team.html"], check=False, capture_output=True).returncode == 0]


rule all:
    input:
        expand("{yaml_file}", yaml_file=[str(afile) for afile in blog_entries]),
        expand("{person_entry}", person_entry=team_entries)
    output:
        "index.html",
        "team.html",
        "blog.html"
    shell:
        """
        python3 scripts/parse_article.py -t templates/blog_template.html -o blog.html -i templates/blog-item-template.html -d blog/ -p posts/ -v  |
        python3 scripts/parse_teams.py -t templates/team_template.html -o team.html -d team/ -v  |
        python3 scripts/parse_index.py -t templates/index_template.html -o index.html
        """
    # run:
        # """
        #
        # from scripts import parse_index as pindex
        # pindex.main(index_template='templates/index_template.html', output_html='index.html', verbose=True)
        # """

