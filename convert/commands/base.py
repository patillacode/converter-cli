import os
import sys

import ffmpeg

from termcolor import colored

from .utils import clear
from .utils import multi_source
from .utils import print_message as prmsg
from .utils import single_source
from .utils import validate_path


class Base(object):
    """A base command."""

    def __init__(self, options, *args, **kwargs):
        """Creates the Base object (a command object).

        :param options: command options
        :type options: dict
        """

        self.options = options
        self.args = args
        self.kwargs = kwargs
        clear()

    def confirm_multiple(self, ori_ext, ori_folder, out_ext, out_folder):
        """"""
        prmsg('confirm_multi',
              **{
                'ori_ext': ori_ext,
                'ori_folder': ori_folder,
                'out_ext': out_ext,
                'out_folder': out_folder})

        confirmation = input(
            colored('\nPlease confirm action above [y/n]: ', 'red'))

        if confirmation not in ('y', ''):
            return False

        return True

    def confirm_single(self, ori_path, out_ext, out_folder):
        """"""
        prmsg('confirm_single',
              **{
                'ori_path': ori_path,
                'out_ext': out_ext,
                'out_folder': out_folder})

        confirmation = input(
            colored('\nPlease confirm action above [y/n]: ', 'red'))

        if confirmation not in ('y', ''):
            return False

        return True

    def convert(self, conversion_data):
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

        if self.options['--multiple']:

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

                    self.run_ffmpeg(
                        source_path, output_path, conversion_data['params'])

        else:

            if not self.confirm_single(source_path,
                                       conversion_data['extension'],
                                       destination):
                sys.exit(2)

            output_path = '{}{}.{}'.format(
                destination, source_name, conversion_data['extension'])

            # clear screen
            clear()

            self.run_ffmpeg(
                source_path, output_path, conversion_data['params'])

        prmsg('completed')

    def run_ffmpeg(self, source_path, output_path, params):
        """Trigger ffmpeg command via the ffmpeg-python lib and given params.

        :param source_path: source media file path
        :type source_path: string
        :param output_path: output media file path
        :type output_path: string
        :param params: ffmpeg command options
        :type params: dict
        """

        try:
            if not self.options['--verbose']:
                prmsg('converting',
                      **{
                        'source_path': source_path,
                        'output_path': output_path})
            (
                ffmpeg
                .input(source_path)
                .output(
                    output_path,
                    **params,
                )
                .overwrite_output()
                .run(quiet=not(self.options['--verbose']))
            )

        except Exception as exc:
            prmsg('exception', **{'exc': exc})
            sys.exit(1)

    def run(self):
        """All commands must implement this method."""
        raise NotImplementedError(
            'You must implement the run() method yourself!')
