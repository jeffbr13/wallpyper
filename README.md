wallpyper
=========

Python script to update your GNOME desktop background from an online source.


Usage
-----

You can just run `python wallpyper.py` and you'll get one of this week's
top-upvoted images from [/r/wallpaper(s)](http://www.reddit.com/r/wallpaper+wallpapers/top/?sort=top&t=week). Otherwise, if you run

    python wallpyper.py --colourlovers

you'll get a pattern from [COLOURlovers](http://www.colourlovers.com) to jazz
up your GNOME desktop!

If you need some help, just <strike>whistle</strike> use the `help` flag:

    python wallpyper.py --help


Who are you? What have done?
----------------------------

Well, my name is [Ben Jeffrey](http://benjeffrey.net). If you see any bugs or
poor form, perhaps you could fork me and send a pull request?
I'd really appreciate the feedback!

This has mostly been a project to brush up my Python skills (and familiarity
with libraries), so if you take a peek inside, you can see that `wallpyper`
(named no more tackily than any other Python program...) uses:

* command-line arguments
* API calls
* HTML scraping
* regular expressions
* external process calls
* oh my!

Next though, I want to add some tests, and then (one day) make it look like
something I could install with `pip`. Pip-pip-hooray!
