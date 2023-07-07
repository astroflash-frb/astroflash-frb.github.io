#! /usr/bin/env python3

"""This is a Hugo-like motivated script to parse the human-based files
containing the different articles.
"""

import os
import sys
import glob
import yaml
import traceback
from pathlib import Path

_ROLES = {'leader': 'Group Leader', 'staff': 'Staff', 'postdoc': 'PostDoc',
          'phd': 'PhD students', 'master': 'Master Students',
          'affiliated': 'Affiliated', 'former': 'Previous  Members'}

class Researcher(object):
    @property
    def roles(self):
        return _ROLES

    @property
    def social_media(self):
        return {'github': {'a_class': 'github', 'i_class': 'fa fa-github'},
                'gitlab': {'a_class': 'twt', 'i_class': 'fa fa-twitter'},
                'facebook': {'a_class': 'fb', 'i_class': 'fa fa-facebook'},
                'twitter': {'a_class': 'twt', 'i_class': 'fa fa-twitter'},
                'linkedin': {'a_class': 'linkdin', 'i_class': 'fa fa-linkedin'},
                'webpage': {'a_class': 'dribble', 'i_class': 'fa fa-dribbble'}}

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name: str):
        assert isinstance(new_name, str), f"The new name needs to be a str, instead of {new_name}."
        self._name = new_name

    @property
    def filename(self):
        """This is just the preffix used in all files relative to this researcher.
        Likely just the surname, with no spaces (converted to underscore)
        """
        return self._filename

    @filename.setter
    def filename(self, new_filename):
        self._filename = new_filename

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, new_role: str):
        assert new_role in self.roles, \
               f"The new role {new_role} is not accepted. Possible values: {self.roles.keys()}"
        self._role = new_role

    @property
    def institute(self):
        return self._institute

    @institute.setter
    def institute(self, new_institute: str):
        assert isinstance(new_institute, str), f"The new institute needs to be a str, instead of {new_institute}."
        self._institute = new_institute

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, a_description: str):
        assert isinstance(a_description, str) or a_description is None, "The description needs to be a str."
        if a_description is None:
            self._description = ''
        else:
            self._description = a_description

    @property
    def links(self):
        """dict containing the different social media links.
        The keys would be the different platforms, and the value the url to the personal account
        """
        return self._links

    @links.setter
    def links(self, links_dict):
        assert isinstance(links_dict, dict), "Researcher.links needs to be a dict."
        for a_key in links_dict:
            assert a_key in self.social_media, \
                   f"Only the following platforms are available for social media: {self.social_media.keys()}"
        self._links = links_dict

    def add_link(self, platform, url):
        """Adds a link to a social media platform.
        The platform needs to be one of the accepted ones.
        """
        assert platform in self.social_media
        self._links[platform] = url

    def __init__(self, name=None, filename=None, role=None, institute=None, description=None, links=None):
        self._name = name
        self._filename = filename
        self._role = role
        self._institute = institute
        self._description = description
        if links is None:
            self.links = dict()
        else:
            self.links = links

    def format_social(self):
        s = ''
        s_template = '<a class="{a_class}" href="{url}"><i class="{i_class}"></i></a>\n'
        for a_link in self.links:
            s += s_template.format(a_class=self.social_media[a_link]['a_class'],
                                   i_class=self.social_media[a_link]['i_class'], url=self.links[a_link])

        return s

    def format_person(self):
        return """<div class="col-md-6">
                <div class="team team-list wow slideInRight">
                    <div class="img-hexagon">
                        <img src="team/{filename}.jpg" alt="">
                        <span class="img-top"></span>
                        <span class="img-bottom"></span>
                    </div>
                    <div class="team-content">
                        <h3>{fullname}</h3>
                        <p>{institute}</p>
                        <p class="desc">{description}</p>
                        <div class="team-social">
                            {social}
                        </div>
                    </div>
                </div>
            </div>\n
            """.format(filename=self.filename, fullname=self.name, institute=self.institute,
                       description=self.description, social=self.format_social())

    def format_short_person(self):
        return """<div class="col-md-6 col-lg-3">
                <div class="team wow slideInRight">
                    <div class="img-hexagon">
                        <img src="team/{filename}.jpg" alt="">
                        <span class="img-top"></span>
                        <span class="img-bottom"></span>
                    </div>
                    <div class="team-content">
                        <h3>{fullname}</h3>
                        <p>{institute}</p>
                    </div>
                </div>
            </div>\n""".format(filename=self.filename, fullname=self.name, institute=self.institute)


class Researchers(object):
    """A list of researchers
    """
    @property
    def roles(self):
        return _ROLES

    @property
    def researchers(self):
        return sorted(self._researchers, key=lambda t: t.filename)

    @researchers.setter
    def researchers(self, list_of_researchers):
        assert isinstance(list_of_researchers, list)
        for a_researcher in list_of_researchers:
            assert isinstance(a_researcher, Researcher)

        self._researchers = list_of_researchers

    def __init__(self, researchers=None):
        if researchers is None:
            self._researchers = []
        else:
            self._researchers = researchers

    def pop(self, filename=None, name=None):
        """Pops the given researcher from the list of researchers.
        Either the 'filename' or 'name' attributes must be provided to localize the researcher.
        """
        assert (filename is not None) or (name is not None), \
               "One, either 'filename' or 'name', must be provided."
        assert not ((filename is not None) and (name is not None)), \
               "Only one, either 'filename' or 'name', must be provided."
        if filename is not None:
            index = [r.filename for r in self._researchers].index(filename)
        elif name is not None:
            index = [r.filename for r in self._researchers].index(filename)
        return self._researchers.pop(index)

    def with_role(self, role):
        """Returns a list with the researchers within the specified role
        """
        assert role in self.roles, "Specified role not expected."
        return [person for person in self.researchers if person.role == role]

    def add_researcher(self, new_researcher):
        assert isinstance(new_researcher, Researcher)
        self._researchers.append(new_researcher)

    def get_researchers(self, path='../team/*.yaml', verbose=False):
        all_people = glob.glob(path)
        all_people.remove(all_people[all_people.index('../team/template.yaml')])
        if verbose:
            print("People found in the team:")

        for one_person in all_people:
            with open(one_person, 'r') as personfile:
                data = yaml.load(personfile, Loader=yaml.loader.SafeLoader)
                person = Researcher()
                person.name = data['name']
                person.filename = Path(one_person).stem
                person.role = data['role']
                person.institute = data['institute']
                person.description = data['description']
                for socialmedia in person.social_media:
                    if socialmedia in data:
                        person.add_link(socialmedia, data[socialmedia])
            if verbose:
                print(f"{person.role}: {person.name} ({person.institute})")

            self.add_researcher(person)

    def format_group(self, a_group):
        assert a_group in self.roles
        return f"""<div class="row">
            <div class="col-md-12 heading">
                <span class="title-icon classic float-left"><i class="fa fa-users"></i></span>
                <h2 class="title classic">{self.roles[a_group]}</h2>
            </div>
        </div>\n"""

    def merge_people_in_html(self, html_template, output_html, verbose=False):
        assert os.path.isfile(html_template), f"The file {html_template} is not found."
        s = ''
        for a_role in self.roles:
            s += '<div class="gap-60"></div>'
            s += self.format_group(a_role)
            s += '<div class="row">'
            for person in self.with_role(a_role):
                s += person.format_person()

            s += '</div>\n<div class="gap-60"></div>'

        with open(html_template, 'r') as template:
            if verbose:
                print(f"Reading html template file {html_template}")

            full_html = ''.join(template.readlines())
            full_html = full_html.replace('{{content}}', s)

        if verbose:
            print(f"Writting html information to {output_html} "
                  f"({'exists' if os.path.isfile(output_html) else 'does not exist'})")

        with open(output_html, 'w') as outhtml:
            outhtml.write(full_html)


def main(verbose=False):
    try:
        p = Researchers()
        p.get_researchers(verbose=verbose)
        p.merge_people_in_html('../templates/team_template.html', '../team.html', verbose)
    except Exception:
        print('*** Error occurred while processing persons.')
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main(verbose=True)
