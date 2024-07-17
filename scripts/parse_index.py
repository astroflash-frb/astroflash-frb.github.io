#! /usr/bin/env python3

import os
import sys
import argparse
import traceback
import logging
from pathlib import Path
import parse_article as particles
import parse_teams as pteams



def main(index_template='../templates/index_template.html', output_html='../index.html',
         verbose=False):
    logging.basicConfig(level=logging.INFO,
                        format="%(levelname)s : %(asctime)s - %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S")
    logger = logging.getLogger('main_M33_WR.py')
    logger.addHandler(logging.FileHandler(filename='log-python.log'))
    try:
        assert os.path.isfile(index_template), f"The file {index_template} is not found."
        # First gets the team information (short version of people to be shown in index.html)
        p = pteams.Researchers()
        if Path.cwd().name == 'scripts':
            p.get_researchers(verbose=True)
        else:
            p.get_researchers(path='team/', verbose=True)

        logger.info(f"There are {len(p)} researchers.")
        str_team = ''
        # Old code where they are shorted firt by role and then by surname
        # for a_role in p.roles:
        #     for person in p.with_role(a_role):
        #         str_team += person.format_short_person()

        # New code where, except Jason, now they are all shorted by surname
        str_team += p.pop(name='Jason Hessels').format_short_person()
        for person in p.researchers:
            if person.role != 'former':
                str_team += person.format_short_person()

        # Now it gets the same but for the latest 6 posts
        p = particles.Posts()
        if Path.cwd().name == 'scripts':
            p.get_posts(verbose=True)
        else:
            p.get_posts(path='posts/', verbose=True)

        p.sort(reverse=True)
        logger.info(f"There are {len(p)} posts.")

        str_posts = ''
        for post in p.sorted(reverse=True)[:6]:
            str_posts += post.format_short_post(fullpath='posts/')

        assert len(str_posts) > 0, "No info found to build up the posts."
        with open(index_template, 'r') as template:
            if verbose:
                print(f"Reading the html template file {index_template}")

            full_html = ''.join(template.readlines())
            full_html = full_html.replace('{{posts}}', str_posts)
            full_html = full_html.replace('{{team}}', str_team)

        with open(output_html, 'w') as outhtml:
            logger.info(f"Writting {output_html}.")
            if verbose:
                print(f"Writting the html template file {output_html}")

            outhtml.write(full_html)
            logger.info(f"Writted {output_html}.")

    except Exception:
        print('*** Error occurred while processing persons.')
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    usage = "%(prog)s [-h]  parse_index.py"
    description = "Creates the main index.html wiht the current information"
    parser = argparse.ArgumentParser(description=description, prog="", usage=usage)
    parser.add_argument('-t', '--template', type=str, default='../templates/index_template.html',
                        help='index.html template file.')
    parser.add_argument('-o', '--output', type=str, default='../index.html',
                        help='index.html file to be created.')
    parser.add_argument('-v', '--verbose', action='store_true', default=False)


    args = parser.parse_args()

    main(index_template=args.template, output_html=args.output, verbose=args.verbose)
