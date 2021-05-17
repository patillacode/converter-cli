[![Downloads](https://pepy.tech/badge/converter-cli)](https://pepy.tech/project/converter-cli)

converter-cli         
=============

*A media converter command line program in Python.*


Purpose
-------

This is a custom Python (3) CLI for converting media files

I've done this to make it easy to convert my media files into different
formats, bitrates and whatnot without having to remember the ffmpeg syntax for
each case.

It does NOT cover all ffmpeg options (I just wanted a few) but it is possible to add them.


Install
-------

Plug & Play:

    $ pip3 install converter-cli


If you want to play around with the code I'd recommend creating a virtual environment first (with python3):

    $ mkvirtualenv --python=/usr/local/bin/python3 converter-cli


And then:

    $ git clone https://github.com/patillacode/converter-cli.git

    $ cd converter-cli

    $ pip install -r requirements-dev.txt

    $ python setup.py develop


Unit Tests
----------

    $ py.test tests

Usage
-----

The idea is for the CLI to ask you for the necessary information in order to work,
the only thing you should know is that if what you are interested in is converting audio
you should use the `audio` command:

    $ converter-cli audio

If you are interested in converting video files then
use command `video`:

    $ converter-cli video


Full command list follows:

    Usage:
        converter-cli hello
        converter-cli audio
        converter-cli audio [-m | --multiple] [--verbose] [-n | --no-confirm]
        converter-cli video
        converter-cli video [-m | --multiple] [--verbose] [-n | --no-confirm]
        converter-cli -h | --help
        converter-cli -v | --version

    Options:
        -h --help                         Show this screen.
        -v --version                      Show version.
        -m --multiple                     Convert all files within a given folder
        -n --no-confirm                   Avoid user confirmation before converting
        --verbose                         Redirect converting process to stdout


By default the CLI will be used to convert one file, but the `-m`/`--multiple` option will allow you to do multiple files at once:

    $ converter-cli video -m

Also by default, the CLi will hide the output of the ffmpeg command in favor of a more readable custom line,
unless the `--verbose` option is specified:

    $ converter-cli audio --verbose


Examples
--------

Convert a .wav audio file into a .mp3 file:

    $ converter-cli audio

You will be presented with the following:

    Please choose an option:
        1) Convert to .mp3 (320k)
        2) Convert to .wav
    Enter option number:

Insert the option number in this case `1` and this will show up:

    Enter path to source file:

Here we will enter something like `/path/to/file/music.wav` and hit enter.

    Enter path to destination folder (Enter for same folder as source):

Notice if your click enter without specifying any path then the output file will
be in the same directory as the source file `/path/to/file/`

Next thing to happen will be (unless the `--no-confirm option` was given):


                      WARNING

    Output file will be called the same as the original
    with the proper extension (.mp4, .mp3, ...) which
    may cause an overwrite - YOU HAVE BEEN WARNED


    You are about to convert file /path/to/file/music.wav into a .mp3 file to be saved in folder /path/to/file/

    Please confirm action above [y/n]:

I have added the confirmation process with the warning message to give the user the option to review what is going to happen,
I might add the option in the future to bypass this.

You can just hit enter, or type `y` and hit enter, anything else will stop the process.

Once you accept, this will show up:

    Converting source /path/to/file/music.wav into output /path/to/file/music.mp3 ...

    (っ◕‿◕)っ    Conversion completed    ⊂(´･◡･⊂ )∘˚


As you can see the CLI asks the user for all needed data and provides the user with explicit messages of what is happening.
The rest of the commands have the same flow, just read what it asks for :)


Demo
----

[![asciicast](https://asciinema.org/a/210664.svg)](https://asciinema.org/a/210664)


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
