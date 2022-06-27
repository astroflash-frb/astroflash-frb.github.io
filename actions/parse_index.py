#! /usr/bin/env python3

import os
import sys
import traceback
import parse_article as particles
import parse_teams as pteams


def main(index_template='../templates/index_template.html', output_html='../index.html'):
    try:
        assert os.path.isfile(index_template), f"The file {index_template} is not found."
        # First gets the team information (short version of people to be shown in index.html)
        p = pteams.Researchers()
        p.get_researchers()

        str_team = ''
        for a_role in p.roles:
            for person in p.with_role(a_role):
                str_team += person.format_short_person()

        # Now it gets the same but for the latest 6 posts
        p = particles.Posts()
        p.get_posts()
        p.sort(reverse=True)

        str_posts = ''
        for post in p.sorted(reverse=True)[:6]:
            str_posts += post.format_short_post(fullpath='posts/')

        with open(index_template, 'r') as template:
            full_html = ''.join(template.readlines())
            full_html = full_html.replace('{{posts}}', str_posts)
            full_html = full_html.replace('{{team}}', str_team)

        with open(output_html, 'w') as outhtml:
            outhtml.write(full_html)

    except Exception:
        print('*** Error occurred while processing persons.')
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
