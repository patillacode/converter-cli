converter-cli
=============

*A media converter command line program in Python.*


Purpose
-------

This is a custom Python CLI for converting media files

I've done this to make it easy to convert my media files into different
formats, bitrates and whatnot without having to remember the ffmpeg syntax for
each case.

It does NOT cover all ffmpeg options (I just wanted a few) but it is possible to add them.


Install & Run
-------------

Plug & Play:

    $ pip install converter-cli


If you want to play around with the code I'd recommend creating a virtual environment:

    $ mkvirtualenv --python=/usr/local/bin/python3 converter-cli


And then:

    $ git clone

    $ cd converter-cli

    $ python setup.py develop


Run:

    $ converter-cli


Dependencies
------------
- [ffmpeg-python](https://github.com/kkroening/ffmpeg-python)
- [docopt](https://github.com/docopt/docopt)
- [termcolor](https://pypi.org/project/termcolor/)


Contributing
------------

Feel free to report any bugs or submit feature requests.

Pull requests are welcome as well.


Special thanks
--------------

- [Michal Klich](https://github.com/inirudebwoy)