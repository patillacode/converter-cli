import os
import sys

from termcolor import colored

from ..converter_utils import clear
from ..converter_utils import multi_source
from ..converter_utils import print_message as prmsg
from ..converter_utils import single_source
from ..converter_utils import validate_path
from ..converter_utils import user_confirmed


class Base(object):
    """A base command."""

    def __init__(self, options, *args, **kwargs):
        """Create the Base object (a command object).

        :param options: command options
        :type options: dict
        """

        self.options = options
        self.args = args
        self.kwargs = kwargs
        clear()

    def confirm_multiple(self, ori_ext, ori_folder, out_ext, out_folder):
        """Confirm conversion menu"""
        prmsg('confirm_multi',
              **{
                'ori_ext': ori_ext,
                'ori_folder': ori_folder,
                'out_ext': out_ext,
                'out_folder': out_folder})

        confirmation = input(
            colored('\nPlease confirm action above [y/n]: ', 'red'))

        return user_confirmed(confirmation)

    def confirm_single(self, ori_path, out_ext, out_folder):
        """"""
        prmsg('confirm_single',
              **{
                'ori_path': ori_path,
                'out_ext': out_ext,
                'out_folder': out_folder})

        confirmation = input(
            colored('\nPlease confirm action above [y/n]: ', 'red'))

        return user_confirmed(confirmation)

    def get_user_input(self, conversion_data):
        """Set all needed variables via user input for the conversion.

        :param conversion_data: command based data (see command init)
        :type source_path: dict
        """

        if self.options['--multiple']:
            source_folder, source_extension = multi_source()
        else:
            source_path, source_name, source_folder = single_source()

        default_folder = '{}'.format(source_folder)
        destination = input(colored(
            "Enter path to destination folder "
            "(Enter for same folder as source): ", 'green')) or default_folder
        destination = validate_path(destination, 'folder')

        # display warning
        prmsg('warning')

        # multiple files flow
        if self.options['--multiple']:
            # do not show confirmation message if the option is enabled
            if not self.options['--no-confirm']:
                if not self.confirm_multiple(source_extension,
                                             source_folder,
                                             conversion_data['extension'],
                                             destination):
                    sys.exit(2)

                # clear screen
                clear()

            folder = os.fsencode(source_folder)
            for file in os.listdir(folder):
                # get source filename
                filename = os.fsdecode(file)
                # set needed vars based on filename
                source_path = os.path.join(source_folder, filename)
                source_name = os.path.splitext(os.path.split(filename)[1])[0]
                source_ext = os.path.splitext(os.path.split(filename)[1])[1]

                # check extension fits
                if source_ext == '.{}'.format(source_extension):
                    output_path = '{}{}.{}'.format(
                        destination, source_name, conversion_data['extension'])

                    return source_path, output_path, conversion_data['params']

        # single file flow
        else:
            # do not show confirmation message if the option is enabled
            if not self.options['--no-confirm']:
                if not self.confirm_single(source_path,
                                           conversion_data['extension'],
                                           destination):
                    sys.exit(2)

                # clear screen
                clear()
            output_path = '{}{}.{}'.format(
                destination, source_name, conversion_data['extension'])

            return source_path, output_path, conversion_data['params']

    def run(self):
        """All commands must implement this method."""
        raise NotImplementedError(
            'You must implement the run() method yourself!')
