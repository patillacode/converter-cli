import os
import sys

import ffmpeg

from termcolor import colored


class Base(object):
    """A base command."""

    def __init__(self, options, *args, **kwargs):
        """"""
        self.options = options
        self.args = args
        self.kwargs = kwargs
        self.clear()

    def let_user_pick(self):
        """"""
        print("\nPlease choose an option:")
        for key, value in self.conversion_map.items():
            print(
                colored("\t{}) {}".format(key, value['option_text']), 'green'))
        i = input("Enter option number: ")

        try:
            try:
                if int(i) in self.conversion_map:
                    return int(i)
                else:
                    raise ValueError()

            except ValueError:
                print(colored('\nPlease enter a valid option', 'red'))
                sys.exit(2)

        except Exception as exc:
            print(
                colored('\nAn exception ocurred:', 'red'),
                '{}'.format(exc))
            sys.exit(1)

        return None

    def clear(self):
        # for windows
        if os.name == 'nt':
            command = 'cls'
        # for mac and linux(here, os.name is 'posix')
        else:
            command = 'clear'

        os.system(command)

    def confirm_multiple(self, ori_ext, ori_folder, out_ext, out_folder):
        print(
            '\nYou are about to convert all',
            colored('.{}'.format(ori_ext), 'yellow'),
            'files in folder',
            colored('{}'.format(ori_folder), 'yellow'),
            'into',
            colored('.{}'.format(out_ext), 'yellow'),
            'files to be saved in folder',
            colored('{}'.format(out_folder), 'yellow'))

        confirmation = input(
            colored('\nPlease confirm action above [y/n]: ', 'red'))

        if confirmation not in ('y', ''):
            return False

        return True

    def confirm_single(self, ori_path, out_ext, out_folder):
        print(
            '\nYou are about to convert file',
            colored('{}'.format(ori_path), 'yellow'),
            'into a',
            colored('.{}'.format(out_ext), 'yellow'),
            'file to be saved in folder',
            colored('{}'.format(out_folder), 'yellow'))

        confirmation = input(
            colored('\nPlease confirm action above [y/n]: ', 'red'))

        if confirmation not in ('y', ''):
            return False

        return True

    def print_warning(self):
        print(colored(
            '                                                     \n'
            '                      WARNING                        \n',
            'red',
            attrs=['bold', 'underline']))
        print(colored(
            ' Output file will be called the same as the original \n'
            ' with the proper extension (.mp4, .mp3, ...) which   \n'
            ' may cause an overwrite - YOU HAVE BEEN WARNED       \n',
            'red',
            attrs=['reverse', 'bold']))

    def validate_path(self, path, path_type):
        valid = True
        if path_type not in ('file', 'folder'):
            print(
                colored('Wrong path type', 'red'),
                colored('{}'.format(path_type), 'yellow'),
                colored('only valid values are', 'red'),
                colored('[file, folder]', 'yellow'))
            sys.exit(1)

        elif path_type == 'file':
            if not os.path.isfile(path):
                valid = False

        elif path_type == 'folder':
            if path[-1] != '/':
                path = path + '/'
            if not os.path.exists(path):
                valid = False

        if not valid:
            print(
                colored('\nGiven path is not valid, please confirm', 'red'),
                colored(path, 'yellow'),
                colored('has no typos.\n', 'red'))
            sys.exit(2)

        return path

    def convert(self, conversion_data):
        """"""
        if self.options['--multiple']:
            source_folder = input(
                colored("Enter path to source folder containing all files to "
                        "be converted: ", 'green'))
            source_folder = self.validate_path(source_folder, 'folder')
            source_extension = input(
                colored("Enter extension of source files to be converted "
                        "(mp4, mp3, ...): ", 'green'))
        else:
            source_path = input("Enter path to source file: ")
            source_path = self.validate_path(source_path, 'file')
            source_name = os.path.splitext(os.path.split(source_path)[1])[0]
            source_folder = os.path.splitext(os.path.split(source_path)[0])[0]

        default_folder = '{}'.format(source_folder)
        destination = input(colored(
            "Enter path to destination folder "
            "(Enter for same folder as source): ", 'green')) or default_folder
        destination = self.validate_path(destination, 'folder')

        # display warning
        self.print_warning()

        if self.options['--multiple']:

            if not self.confirm_multiple(source_extension,
                                         source_folder,
                                         conversion_data['extension'],
                                         destination):
                sys.exit(2)

            # clear screen
            self.clear()

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
            self.clear()

            self.run_ffmpeg(
                source_path, output_path, conversion_data['params'])

        print(
            colored('\n(っ◕‿◕)っ   ', 'magenta'),
            colored('Conversion completed',
                    'green',
                    attrs=['bold']),
            colored('   ⊂(´･◡･⊂ )∘˚\n', 'magenta'))

    def run_ffmpeg(self, source_path, output_path, params):
        """"""
        try:
            if not self.options['--verbose']:
                print(
                    'Converting source',
                    colored('{}'.format(source_path), 'yellow'),
                    'into output',
                    colored('{}'.format(output_path), 'yellow'),
                    '... ',
                    end='',
                    flush=True)
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

            print('Done!')
        except Exception as exc:
            print(
                colored('An exception ocurred:', 'red'),
                '{}'.format(exc))
            sys.exit(1)

    def run(self):
        raise NotImplementedError(
            'You must implement the run() method yourself!')
