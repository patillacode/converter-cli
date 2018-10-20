"""
converter-cli

Usage:
  converter-cli hello
  converter-cli audio
  converter-cli audio [-m | --multiple | --verbose]
  converter-cli video
  converter-cli video [-m | --multiple | --verbose]
  converter-cli -h | --help
  converter-cli -v | --version

Options:
  -h --help                         Show this screen.
  -v --version                      Show version.
  -m --multiple                     Convert all files within a given folder
  --verbose                         Redirect converting process to stdout

Examples:
  convert hello

Help:
  For help using this tool, please open an issue on the Github repository:
  https://github.com/patillacode/converter-cli
"""


from docopt import docopt
from inspect import getmembers
from inspect import isclass

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
