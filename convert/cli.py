"""
convert-cli

Usage:
  convert-cli hello
  convert-cli audio
  convert-cli audio [-m | --multiple | --verbose]
  convert-cli video
  convert-cli video [-m | --multiple | --verbose]
  convert-cli -h | --help
  convert-cli -v | --version

Options:
  -h --help                         Show this screen.
  -v --version                      Show version.
  -m --multiple                     Convert all files within a given folder
  --verbose                         Redirect converting process to stdout

Examples:
  convert hello

Help:
  For help using this tool, please open an issue on the Github repository:
  https://github.com/patillacode/convert-cli
"""


from inspect import getmembers
from inspect import isclass

from docopt import docopt

from . import __version__ as VERSION


def main():
    """Main CLI entrypoint."""
    import convert.commands
    options = docopt(__doc__, version=VERSION)

    # Here we'll try to dynamically match the command the user is trying to run
    # with a pre-defined command class we've already created.
    for (k, v) in options.items():
        if hasattr(convert.commands, k) and v:
            module = getattr(convert.commands, k)
            convert.commands = getmembers(module, isclass)
            command = [command[1] for command
                       in convert.commands
                       if command[0] != 'Base'][0]
            command = command(options)
            command.run()
