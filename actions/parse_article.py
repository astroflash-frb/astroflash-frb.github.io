#! /usr/bin/env python3

"""This is a Hugo-like motivated script to parse the human-based files
containing the different articles.
"""

import os
import sys
import datetime as dt
import glob
import yaml
import traceback


categories = {'paper': 'Papers', 'atel': 'ATels', 'talk': 'Talks'}


class Post(object):

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, new_par):
        assert isinstance(new_par, str)
        self._title = new_par

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, new_par):
        assert isinstance(new_par, str)
        self._author = new_par

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, new_par):
        assert isinstance(new_par, dt.date), \
               f"The value {new_par} (from {self.title}) cannot be parsed into a datetime object."
        self._date = new_par

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, new_par):
        assert (new_par in categories) or (new_par is None), \
               f"{new_par} is not a valid category (accepted values: {categories.keys()})"
        self._category = new_par

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, new_par):
        assert isinstance(new_par, str)
        self._image = new_par

    @property
    def link(self):
        return self._link

    @link.setter
    def link(self, new_par):
        assert isinstance(new_par, str)
        self._link = new_par

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, new_par):
        assert isinstance(new_par, str)
        self._body = new_par

    @property
    def reference(self):
        return self._reference

    @reference.setter
    def reference(self, new_par):
        assert isinstance(new_par, str)
        if (len(new_par) > 0) and (new_par[-1] != '.'):
            self._reference = new_par + '.'
        else:
            self._reference = new_par

    def __init__(self, title=None, author=None, date=None, category=None, image=None, link=None,
                 body=None, reference=None):
        self._title = title
        self._author = author
        self._date = date
        self.category = category
        self._image = image
        self._link = link
        self._body = body
        self._reference = reference

    def format_post(self):
        def linktype(a_link):
            if 'adsabs' in a_link:
                return 'in SAO/NASA ADS'
            elif 'astronomerstelegram' in a_link:
                return "in The Astronomer's Telegram"
            elif 'gcn.gsfc' in a_link:
                return 'in GCN Circulars'
            else:
                return 'it online'

        return """<div class="col-lg-8 isotope-item {category}">
                <div class="post">
                    <div class="post-image-wrapper">
                        <img src="posts/{imgpath}" class="img-fluid" alt="" />
                        <span class="blog-date"> {date}</span>
                    </div>
                    <div class="post-header clearfix">
                        <h2 class="post-title">
                            <a href="blog-item.html">{title}</a>
                        </h2>
                        <div class="post-meta">
                            <span class="post-meta-author">Posted by <a href="team.html"> {author}</a></span>
                            <span class="post-meta-cats">in <a href="#"> {pubtype}</a></span>
                        </div>
                    </div>
                    <div class="post-body">
                        <p>{body}</p>
                        <p>{reference}</p>
                    </div>
                    <div class="post-footer">
                        <a href="{url}" class="btn btn btn-outline-primary">See {linktype}
                            <i class="fa fa-angle-double-right">&nbsp;</i>
                        </a>
                    </div>
                </div>
            </div>
            """.format(category=self.category, imgpath=self.image, date=self.date.strftime('%B %d, %Y'),
                       title=self.title, author=self.author, pubtype=categories[self.category],
                       body=self.body, reference=self.reference, url=self.link, linktype=linktype(self.link))

    def shorten_title(self, max_length_char=85):
        if len(self.title) <= max_length_char:
            return self.title

        return self.title[:self.title.rindex(' ', 0, max_length_char+1)] + '...'

    def format_short_post(self, fullpath='./'):
        image_path = f"{fullpath}{self.image}" if fullpath[-1] == '/' else f"{fullpath}/{self.image}"
        return """<div class="feature-box col-md-6 col-lg-6 wow fadeInDown" data-wow-delay=".5s">
                        <div class="posts-thumb float-left px-3">
                            <a href="blog-rightside.html#">
                                <img alt="img" width="150rem;" height="94rem;" src="{imgpath}">
                            </a>
                        </div>
                        <div class="post-content">
                            <h4 class="entry-title">{title}</h4>
                            <p class="post-meta">
                                <span class="post-meta-date"><i class="fa fa-clock-o"></i> {date}</span>
                            </p>
                        </div>
                    </div>
                    """.format(imgpath=image_path, date=self.date.strftime('%B %d, %Y'), title=self.shorten_title())


class Posts(object):
    """Posts
    """
    @property
    def posts(self):
        return self._posts

    @posts.setter
    def posts(self, posts):
        assert isinstance(posts, list), "posts must be a list."
        self._posts = posts

    def __init__(self, posts=None):
        if posts is None:
            self._posts = []
        else:
            self._posts = posts

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
        all_posts = glob.glob(path)
        all_posts.remove(all_posts[all_posts.index('../posts/template.yaml')])  # check if remove gets this input
        if verbose:
            print("Found the following blog posts:\n" + f"{all_posts}")
        for a_post in all_posts:
            with open(a_post, 'r') as postfile:
                data = yaml.load(postfile, Loader=yaml.loader.SafeLoader)
                if verbose:
                    print(data)
                post = Post()
                post.title = data['title']
                post.author = data['author']
                post.date = data['date']
                post.category = data['category']
                post.image = data['image']
                post.link = data['link']
                post.reference = data['reference']
                post.body = data['body']

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


def merge_posts_in_html(posts, html_template, output_html):
    assert os.path.isfile(html_template), f"The file {html_template} is not found."
    with open(html_template, 'r') as template:
        full_html = ''.join(template.readlines())
        full_html = full_html.replace('{{template}}', posts.format_posts())
        full_html = full_html.replace('{{menu}}', format_menu(posts))

    with open(output_html, 'w') as outhtml:
        outhtml.write(full_html)


def main():
    try:
        p = Posts()
        p.get_posts()
        p.sort(reverse=True)
    except Exception:
        print('*** Error occurred while processing posts.')
        traceback.print_exc()
        sys.exit(1)

    merge_posts_in_html(p, '../templates/blog_template.html', '../blog.html')


if __name__ == '__main__':
    main()
