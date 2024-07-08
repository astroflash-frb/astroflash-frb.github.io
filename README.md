[![pages-build-deployment](https://github.com/astroflash-frb/astroflash-frb.github.io/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/astroflash-frb/astroflash-frb.github.io/actions/workflows/pages/pages-build-deployment)

# AstroFlash Website

This is the repository that holds the [website of the AstroFlash group](https://astroflash-frb.github.io).
The website has been built as plain HTML files


Two main areas can be updated without touching HTML code!

Anyone with access to the `Astroflash-frb` repository should be able to push updates to this repository. And thus keep the website up to date.
This website follows the same principles as [the Hugo framework](https://gohugo.io). However, to get the current static html template working properly in a fast timeline, I just replicated this approach via some ad-doc Python scripts to the parts we are interested.

That means that there are two sections (the _blog_ and the _Team_ page) where one only needs to write the information in a _yaml_ file, without code. For major changes in the template a direct editing of the HTML files would be required.

**Note that index.html, team.html and blog.html should never be edited manually**
Their corresponding files under `templates/` (`blog_template.html`, `index_template.html`, and `team_template.html`) should be the ones modified instead (only if you want to change the _style_ of the pages).

In the following you have the instructions to add a new post entry or a new member in the group. Once you add and edit the necessary files, you just need to run `snakemake` in the main directory to propagate and update all html files.



### Writing a new post entry

The [Latest Results blog section](https://astroflash-frb.github.io/blog.html) page is generated automatically after pushing new contents to the repository.

The contents of the entries are located in the `posts` directory.
To create a new post you would only need to create a single `yaml` file in there with the contents of the post (use the `template.yaml`, or any of the existing files, as a template). It is recommend to also include an image file in the same directory, linked in the post, to be used as header image for it.

The `template.yaml` explains to you the different fields that you need to include. To keep it sorted, please use the file name convention `YYYYMMDD_descriptive-word-author.yaml`.

Once pushed, the new post will be populated into both the `blog` section and the `index` page of the website.



### A new member in the group?

The people from the team follows a similar approach as the posts. Everything is self-contained inside the `team/` directory. In there, each person is defined with a yaml file (use `template.yaml` as a template) and a picture of themselves with `jpg` extension and same file name as the yaml file (use the surname as convention).

The `template.yaml` describes all required and optional fields.



## A more in-depth structure explanation

(for the nerds and future maintainers)

This is a fully-static website using a Bootstrap theme.
To simplify the standard operations (specially to make fast and easy the creation of new posts), the following contents are just stored under individual `yaml` files:
- Posts (under `posts/`) - a new entry will add a new post in the `blog.html` page, also in the `index.html` file.
- People (under `team/`) - a new person within the group, to be shown in the `team.html` and `index.html` pages.

These contents get populated to the html files via simple Python scripts located in the `actions/` directory. Their file names directly reflects what files they read and modify:
- `parse_article.py` takes all available posts and overwrites the `blog.html` file.
- `parse_teams.py` takes all available people from the team and overwrites the `team.html` file.
- `parse_index.py` takes all available posts and people and overwrites the `index.html` file.
- `parse_all.sh` shell script that can run all previous Python scripts.

All this is clustered in `Snakefile`, which is a Make-like file (Snakemake to be precise), which runs all these scripts when needed (only when files have been updated).

The scripts use the blog/team/index template files located in the `templates` directory. These html files are the same as the final ones but contain some keywords (i.e. `{{content}}`) to tell the script where to replace the text and introduce all the content.

Any additional modification of the website would need to be done through the HTML files. Note that some changes, as the menu bar, should be propagated across all the `.html` files.
This is the tree of all important files in the repository:

- `actions/` - the folder containing the Python scripts that populate the new content to the website.
- `posts/` - the folder containing all posts from the blog.
- `team/` - the folder containing all members of the AstroFlash team as individual files.
- `templates/` - the folder containing the `html` files of the pages that get modified automatically (`blog`, `team`, `index`).
- `contact.html` - page showing the institutes involved in the AstroFlash project and a contact.
- `images/` - the folder with standard images used in the website (e.g. the favicon and logo and header pictures).
- `404.html` - the standard Not Found page to show if the user goes to an invalid url.
- `README.md` - this file that you are reading right now.


The following files should only be read (never modified my hand), as they get replaced automatically on each push:
- `index.html` - gets generated from the `templates/index_template.html` file and the `actions/parse_index.py` script.
- `blog.html` - gets generated from the `templates/blog_template.html` file and the `actions/parse_article.py` script.
- `team.html` - gets generated from the `templates/team_template.html` file and the `actions/parse_teams.py` script.


In GitHub, there are two actions that run automatically after every pull request or repository push:
- `populate_templates.yml` (also editable under `.github/workflows/`) - checks for flake8 style in the Python scripts and executes the three of them (`cd actions;python3 parse_article.py`, `parse_teams.py`, `parse_index.py`).
- `pages-build-deployment.yml` - only visible in GitHub. This is the GitHub automatic action that populates the repository into the [visible website](https://astroflash-frb.github.io). If something fails or gets wrong, the website will kept the latest working version of the repository.

