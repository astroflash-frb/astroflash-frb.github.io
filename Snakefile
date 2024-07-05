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
        expand("blog/{yaml_file}", yaml_file=[afile.name.replace('.yaml', '.html') for afile in blog_entries]),
        expand("{person_entry}", person_entry=team_entries)
    output:
        "index.html"
    shell:
        "python3 scripts/parse_index.py -t templates/index_template.html -o index.html"
    # run:
        # """
        #
        # from scripts import parse_index as pindex
        # pindex.main(index_template='templates/index_template.html', output_html='index.html', verbose=True)
        # """


rule blog_entries:
    input: "posts/{entry}.yaml"
    output: blog_entries="blog/{entry}.html"
    run:
        """
        from scripts import parse_article as pblog
        try:
            p = pblog.Posts()
            p.get_posts(verbose=True)
            p.sort(reverse=True)
        except Exception:
            print('*** Error occurred while processing posts.')
            sys.exit(1)

        pblog.merge_posts_in_html(p, 'templates/blog_template.html', 'blog.html',
                        'templates/blog-item-template.html', 'blog/', True)
        """


rule team_entries:
    input: "team/{entry}.yaml"
    run:
        """
        from scripts import parse_team as pteam
        try:
            p = pteam.Researchers()
            p.get_researchers(verbose=verbose)
            p.merge_people_in_html('templates/team_template.html', 'team.html', True)
        except Exception:
            print('*** Error occurred while processing persons.')
            sys.exit(1)
        """




