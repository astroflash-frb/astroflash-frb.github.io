#! /usr/bin/env python3

"""This is a Hugo-like motivated script to parse the human-based files
containing the different articles.
"""

import os
import sys
from pathlib import Path
from rich import print as rprint
import datetime as dt
import glob
from typing import Optional #, Union
import yaml
import traceback



categories: dict[str, str] = {'paper': 'Papers', 'atel': 'ATels', 'talk': 'Talks', 'other': 'Other'}


class Post(object):
    """Defines an article (post) for the blog part of the website.
    """
    @property
    def yaml_file(self) -> str:
        return self._yaml

    @yaml_file.setter
    def yaml_file(self, new_file: str):
        assert isinstance(new_file, str)
        self._yaml = new_file

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, new_par: str):
        assert isinstance(new_par, str)
        self._title = new_par

    @property
    def author(self) -> str:
        return self._author

    @author.setter
    def author(self, new_par: str):
        assert isinstance(new_par, str)
        self._author = new_par

    @property
    def date(self) -> dt.date:
        return self._date

    @date.setter
    def date(self, new_par: dt.date):
        assert isinstance(new_par, dt.date), \
               f"The value {new_par} (from {self.title}) cannot be parsed into a datetime object."
        self._date = new_par

    @property
    def category(self) -> str:
        return self._category

    @category.setter
    def category(self, new_par: str):
        assert (new_par in categories) or (new_par is None), \
               f"{new_par} is not a valid category (accepted values: {categories.keys()})"
        self._category = new_par

    @property
    def image(self) -> str:
        return self._image

    @image.setter
    def image(self, new_par: str):
        assert isinstance(new_par, str)
        self._image = new_par

    @property
    def image_caption(self) -> Optional[str]:
        return self._caption

    @image_caption.setter
    def image_caption(self, new_caption: Optional[str]):
        assert isinstance(new_caption, str) or (new_caption is None)
        self._caption = new_caption

    @property
    def link(self) -> Optional[str]:
        return self._link

    @link.setter
    def link(self, new_par: Optional[str]):
        assert isinstance(new_par, str) or (new_par is None)
        self._link = new_par

    @property
    def body(self) -> str:
        return self._body

    @body.setter
    def body(self, new_par: str):
        assert isinstance(new_par, str)
        self._body = new_par

    @property
    def reference(self) -> Optional[str]:
        return self._reference

    @reference.setter
    def reference(self, new_par: Optional[str]):
        assert isinstance(new_par, str) or (new_par is None)
        if new_par is None:
            self._reference = None
        elif (len(new_par) > 0) and (new_par[-1] != '.'):
            self._reference = new_par + '.'
        else:
            self._reference = new_par

    def __init__(self, yaml, title, author, date, category, body, image,
                 link=None, reference=None, caption=None):
        self.yaml_file = yaml
        self.title = title
        self.author = author
        self.date = date
        self.category = category
        self.image = image
        self.image_caption = caption
        self.link = link
        self.body = body
        self.reference = reference

    def format_post(self, topdir='.') -> str:
        def linktype(a_link: Optional[str]) -> Optional[str]:
            if a_link is None:
                return None
            elif 'adsabs' in a_link:
                return 'in SAO/NASA ADS'
            elif 'astronomerstelegram' in a_link:
                return "in The Astronomer's Telegram"
            elif 'gcn.gsfc' in a_link:
                return 'in GCN Circulars'
            else:
                return 'it online'

        if linktype(self.link) is None:
            link_button = ""
        else:
            link_button = """<a href="{url}" class="btn btn btn-outline-primary">See {linktype}
                            <i class="fa fa-angle-double-right">&nbsp;</i>
                          </a>""".format(url=self.link, linktype=linktype(self.link))

        topdir = topdir[:-1] if topdir[-1] == '/' else topdir
        return """<div class="col-lg-8 isotope-item {category}">
                <div class="post">
                    <div class="post-image-wrapper">
                        <img src="{imgpath}" class="img-fluid" alt="" />
                        <span class="blog-date"> {date}</span>
                        <label>{imgcaption}</label>
                    </div>
                    <div class="post-header clearfix">
                        <h2 class="post-title">
                            <a href="{blog_url}">{title}</a>
                        </h2>
                        <div class="post-meta">
                            <span class="post-meta-author">Posted by
                            <a href="team.html"> {author}</a></span>
                            <span class="post-meta-cats">in <a href="#"> {pubtype}</a></span>
                        </div>
                    </div>
                    <div class="post-body">
                        <p>{body}</p>
                        <p>{reference}</p>
                    </div>
                    <div class="post-footer">
                        {link}
                    </div>
                </div>
            </div>
            """.format(category=self.category, imgpath=topdir + '/posts/' + self.image,
                       blog_url=topdir + "/blog/" + self.yaml_file.replace('.yaml', '.html'),
                       date=self.date.strftime('%B %d, %Y'), title=self.title, author=self.author,
                       pubtype=categories[self.category], body=self.body, reference=self.reference,
                       link=link_button, imgcaption='' if self.image_caption is None else self.image_caption)

    def shorten_title(self, max_length_char: int = 85) -> str:
        if len(self.title) <= max_length_char:
            return self.title

        return self.title[:self.title.rindex(' ', 0, max_length_char+1)] + '...'

    def format_short_post(self, fullpath: str = './') -> str:
        img_path = f"{fullpath}{self.image}" if fullpath[-1] == '/' else f"{fullpath}/{self.image}"
        return """<div class="feature-box col-md-6 col-lg-6 wow fadeInDown" data-wow-delay=".5s">
                        <div class="posts-thumb float-left px-3">
                            <a href="{urlpost}">
                                <img alt="img" width="150rem;" height="94rem;" src="{imgpath}">
                            </a>
                        </div>
                        <div class="post-content">
                            <h4 class="entry-title">{title}</h4>
                            <p class="post-meta">
                                <span class="post-meta-date"><i class="fa fa-clock-o"></i> {date}
                                </span>
                            </p>
                        </div>
                    </div>
                    """.format(imgpath=img_path,
                               urlpost=f"blog/{self.yaml_file.replace('.yaml', '.html')}",
                               date=self.date.strftime('%B %d, %Y'), title=self.shorten_title())


class Posts(object):
    """A list of Posts.
    """
    @property
    def posts(self) -> list[Post]:
        return self._posts

    @posts.setter
    def posts(self, posts: list[Post]):
        assert isinstance(posts, list), "posts must be a list."
        self._posts: list[Post] = posts

    def __init__(self, posts: Optional[list[Post]] = None):
        if posts is None:
            self._posts = []
        else:
            self._posts = posts

    def __len__(self):
        return len(self._posts)

    def sorted(self, reverse=False):
        if reverse:
            return sorted(self._posts, key=lambda t: t.date)[::-1]
        else:
            return sorted(self._posts, key=lambda t: t.date)

    def sort(self, reverse=False):
        if reverse:
            self._posts = sorted(self._posts, key=lambda t: t.date)[::-1]
        else:
            self._posts = sorted(self._posts, key=lambda t: t.date)

    def append(self, a_post):
        self._posts.append(a_post)

    def categories(self):
        cats = set()
        for a_post in self.posts:
            cats.add(a_post.category)

        return cats

    def get_posts(self, path='../posts/*.yaml', verbose=False):
        all_posts = [p for p in glob.glob(path) if "template" not in p]
        if verbose:
            print("Found the following blog posts:")

        for a_post in all_posts:
            print(f"I am here!!!!      {a_post=}")
            with open(a_post, 'r') as postfile:
                data = yaml.load(postfile, Loader=yaml.loader.SafeLoader)
                post: Post = Post(yaml=a_post[a_post.rindex('/')+1:], title=data['title'],
                                        author=data['author'], date=data['date'], category=data['category'],
                                        caption=data['caption'] if 'caption' in data else None,
                                        image=data['image'], link=data['link'], reference=data['reference'],
                                        body=data['body'])

            if not (Path(a_post[:a_post.rindex('/')]) / post.image).exists():
                rprint(f"\n[red bold]The image associated to the post '{post.yaml_file}' " \
                       "cannot be found[/red bold]\n")
            if verbose:
                print(f"{post.date}: {post.title} (by {post.author})")

            self.append(post)

    def format_posts(self):
        s = ""
        for a_post in self.posts:
            s += a_post.format_post()

        return s


def format_menu(posts):
    cats = posts.categories()
    s = '<ul>\n<li><a href="portfolio-classic.html#" class="active" data-filter="*">All</a></li>'
    for cat in cats:
        s += f'<li><a href="portfolio-classic.html#" data-filter=".{cat}">{categories[cat]}</a></li>'

    s += '</ul>'
    return s


def merge_posts_in_html(posts, html_template, output_html, post_template, posts_dir, verbose=False):
    assert os.path.isfile(html_template), f"The file {html_template} was not found."
    assert os.path.isfile(post_template), f"The file {post_template} was not found."
    with open(html_template, 'r') as template:
        if verbose:
            print(f"Reading html information from {html_template}")

        full_html = ''.join(template.readlines())
        full_html = full_html.replace('{{template}}', posts.format_posts())
        full_html = full_html.replace('{{menu}}', format_menu(posts))

    with open(post_template, 'r') as template:
        if verbose:
            print(f"Reading html information from {post_template}")

        full_post_html = ''.join(template.readlines())

    for a_post in posts.posts:
        with open(f"{posts_dir}{'/' if posts_dir[-1] != '/' else ''}" \
                  f"{a_post.yaml_file.replace('.yaml', '.html')}", 'w') as post_template:
            if verbose:
                print(f"Generating html for post {a_post.yaml_file.replace('.yaml', '')}.")

            post_template.write(full_post_html.replace('{{template}}', a_post.format_post(topdir='..')))

    if verbose:
        print(f"Writting html information to {output_html} "
              f"({'exists' if os.path.isfile(output_html) else 'does not exist'})")

    with open(output_html, 'w') as outhtml:
        outhtml.write(full_html)


def main():
    try:
        p = Posts()
        p.get_posts(verbose=True)
        p.sort(reverse=True)
    except Exception:
        print('*** Error occurred while processing posts.')
        traceback.print_exc()
        sys.exit(1)

    merge_posts_in_html(p, '../templates/blog_template.html', '../blog.html',
                        '../templates/blog-item-template.html', '../blog/', True)


if __name__ == '__main__':
    main()
