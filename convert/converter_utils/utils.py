import os
import sys

import ffmpeg
from termcolor import colored


def print_message(msg_type, **kwargs):
    """"""
    if msg_type == 'options':
        print(colored("\t{}) {}".format(kwargs['key'], kwargs['value']), 'green'))

    elif msg_type == 'choose':
        print(colored('\nPlease choose an option:', 'magenta'))

    elif msg_type == 'valid_option':
        print(colored('\n  Please enter a valid option\n', 'red'))

    elif msg_type == 'exception':
        print(colored('\nAn exception ocurred:', 'red'), '{}'.format(kwargs['exc']))

    elif msg_type == 'confirm_multi':
        print(
            '\nYou are about to convert all',
            colored('.{}'.format(kwargs['ori_ext']), 'yellow'),
            'files in folder',
            colored('{}'.format(kwargs['ori_folder']), 'yellow'),
            'into',
            colored('.{}'.format(kwargs['out_ext']), 'yellow'),
            'files to be saved in folder',
            colored('{}'.format(kwargs['out_folder']), 'yellow'),
        )

    elif msg_type == 'confirm_single':
        print(
            '\nYou are about to convert file',
            colored('{}'.format(kwargs['ori_path']), 'yellow'),
            'into a',
            colored('.{}'.format(kwargs['out_ext']), 'yellow'),
            'file to be saved in folder',
            colored('{}'.format(kwargs['out_folder']), 'yellow'),
        )

    elif msg_type == 'warning':
        print(
            colored(
                '                                                     \n'
                '                      WARNING                        \n',
                'red',
                attrs=['bold', 'underline'],
            )
        )
        print(
            colored(
                ' Output file will be called the same as the original \n'
                ' with the proper extension (.mp4, .mp3, ...) which   \n'
                ' may cause an overwrite - YOU HAVE BEEN WARNED       \n',
                'red',
                attrs=['reverse', 'bold'],
            )
        )

    elif msg_type == 'wrong_path_option':
        print(
            colored('Wrong path type', 'red'),
            colored('{}'.format(kwargs['path_type']), 'yellow'),
            colored('only valid values are', 'red'),
            colored('[file, folder]', 'yellow'),
        )

    elif msg_type == 'invalid_path':
        print(
            colored('\nGiven path is not valid, please confirm', 'red'),
            colored(kwargs['path'], 'yellow'),
            colored('has no typos.\n', 'red'),
        )

    elif msg_type == 'completed':
        print(
            colored('\n(っ◕‿◕)っ   ', 'magenta'),
            colored('Conversion completed', 'green', attrs=['bold']),
            colored('   ⊂(´･◡･⊂ )∘˚\n', 'magenta'),
        )

    elif msg_type == 'converting':
        print(
            'Converting source',
            colored('{}'.format(kwargs['source_path']), 'yellow'),
            'into output',
            colored('{}'.format(kwargs['output_path']), 'yellow'),
            '... ',
        )


def let_user_pick(conversion_map):
    """Gather initial user input to set conversion.

    :returns: selected option
    :rtype: int
    """

    print_message('choose')

    for key, value in conversion_map.items():
        print_message('options', **{'key': key, 'value': value['option_text']})

    i = input(colored("Enter option number: ", 'magenta'))

    try:
        try:
            if int(i) in conversion_map:
                return int(i)
            else:
                raise ValueError()

        except ValueError:
            print_message('valid_option')
            sys.exit(2)

    except Exception as exc:
        print_message('exception', **{'exc': exc})
        sys.exit(1)


def validate_path(path, path_type):
    valid = True
    if path_type not in ('file', 'folder'):
        print_message('wrong_path_option', **{'path_type': path_type})
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
        print_message('invalid_path', **{'path': path})
        sys.exit(2)

    return path


def single_source():
    source_path = input(colored("Enter path to source file: ", 'magenta'))
    source_path = validate_path(source_path, 'file')
    source_name = os.path.splitext(os.path.split(source_path)[1])[0]
    source_folder = os.path.splitext(os.path.split(source_path)[0])[0]

    return source_path, source_name, source_folder


def multi_source():
    source_folder = input(
        colored(
            "Enter path to source folder containing all files to " "be converted: ",
            'green',
        )
    )
    source_folder = validate_path(source_folder, 'folder')
    source_extension = input(
        colored(
            "Enter extension of source files to be converted " "(mp4, mp3, ...): ",
            'green',
        )
    )

    return source_folder, source_extension


def clear():
    # for windows
    if os.name == 'nt':
        command = 'cls'
    # for mac and linux(here, os.name is 'posix')
    else:
        command = 'clear'

    os.system(command)


def user_confirmed(confirmation):
    if confirmation in ('y', 'yes', 'Y', ''):
        return True

    return False


def confirmator(options, **kwargs):
    """"""
    # Show confirmation message when the --no-confirm option is missing
    if not options['--no-confirm']:
        # display warning
        print_message('warning')

        if options['--multiple']:
            print_message(
                'confirm_multi',
                **{
                    'ori_ext': kwargs['ori_ext'],
                    'ori_folder': kwargs['ori_folder'],
                    'out_ext': kwargs['out_ext'],
                    'out_folder': kwargs['out_folder'],
                },
            )

        else:
            print_message(
                'confirm_single',
                **{
                    'ori_path': kwargs['ori_path'],
                    'out_ext': kwargs['out_ext'],
                    'out_folder': kwargs['out_folder'],
                },
            )

        confirmation = input(colored('\nPlease confirm action above [y/n]: ', 'red'))

        if not user_confirmed(confirmation):
            sys.exit(2)
        else:
            # clear screen
            clear()


def run_ffmpeg(source_path, output_path, ffmpeg_params, options):
    """Trigger ffmpeg command via the ffmpeg-python lib and given params.

    :param source_path: source media file path
    :type source_path: string
    :param output_path: output media file path
    :type output_path: string
    :param ffmpeg_params: ffmpeg command options
    :type ffmpeg_params: dict
    :param options: command options
    :type options: dict
    """

    try:
        # present user with information of happening conversion
        if not options['--verbose']:
            print_message(
                'converting', **{'source_path': source_path, 'output_path': output_path}
            )

        # run the actual ffmpeg command
        (
            ffmpeg.input(source_path)
            .output(
                output_path,
                **ffmpeg_params,
            )
            .overwrite_output()
            .run(quiet=not (options['--verbose']))
        )

    except Exception as exc:
        print_message('exception', **{'exc': exc})
        sys.exit(1)
