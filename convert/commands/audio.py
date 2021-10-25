from ..converter_utils import let_user_pick
from ..converter_utils import print_message as prmsg
from ..converter_utils import run_ffmpeg
from .base import Base


class Audio(Base):
    """Get user input to execute different video conversions"""

    def __init__(self, options, *args, **kwargs):
        super().__init__(options, *args, **kwargs)
        self.conversion_map = {
            1: {
                'option_text': 'Convert to .mp3 (320k)',
                'extension': 'mp3',
                'params': {'ar': 44100, 'ac': 2, 'ab': '320k ', 'f': 'mp3'},
            },
            2: {'option_text': 'Convert to .wav', 'extension': 'wav', 'params': {}},
        }

    def run(self):
        """Run the Audio command."""
        chosen_option = let_user_pick(self.conversion_map)
        source_paths, output_paths, params = self.get_user_input(
            self.conversion_map[chosen_option]
        )
        for (source_path, output_path) in list(zip(source_paths, output_paths)):
            run_ffmpeg(source_path, output_path, params, self.options)
        prmsg('completed')
