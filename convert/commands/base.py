import os

from termcolor import colored

from ..converter_utils import (clear, confirmator, multi_source, single_source,
                               validate_path)


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

    def get_user_input(self, conversion_data):
        """Set all needed variables via user input for the conversion.

        :param conversion_data: command based data (see command init)
        :type conversion_data: dict
        :returns: source_paths
                  output_paths
                  conversion_data_params
        :rtype: string
                list
                list
        """

        if self.options['--multiple']:
            source_folder, source_extension = multi_source()
        else:
            source_path, source_name, source_folder = single_source()

        default_folder = '{}'.format(source_folder)
        destination = (
            input(
                colored(
                    "Enter path to destination folder "
                    "(Enter for same folder as source): ",
                    'green',
                )
            )
            or default_folder
        )
        destination = validate_path(destination, 'folder')

        source_paths = []
        output_paths = []

        # multiple files flow
        if self.options['--multiple']:
            confirmator(
                self.options,
                **{
                    'ori_ext': source_extension,
                    'ori_folder': source_folder,
                    'out_ext': conversion_data['extension'],
                    'out_folder': destination,
                },
            )

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
                    source_paths.append(source_path)
                    output_path = '{}{}.{}'.format(
                        destination, source_name, conversion_data['extension']
                    )
                    output_paths.append(output_path)

        # single file flow
        else:
            # do not show confirmation message if the option is enabled
            confirmator(
                self.options,
                **{
                    'ori_path': source_path,
                    'out_ext': conversion_data['extension'],
                    'out_folder': destination,
                },
            )

            source_paths = [source_path]
            output_paths = [
                '{}{}.{}'.format(destination, source_name, conversion_data['extension'])
            ]

        return source_paths, output_paths, conversion_data['params']

    def run(self):
        """All commands must implement this method."""
        raise NotImplementedError('You must implement the run() method yourself!')
