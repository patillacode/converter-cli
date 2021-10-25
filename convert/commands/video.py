from ..converter_utils import let_user_pick
from ..converter_utils import print_message as prmsg
from ..converter_utils import run_ffmpeg
from .base import Base


class Video(Base):
    """Get user input to execute different video conversions"""

    def __init__(self, options, *args, **kwargs):
        super().__init__(options, *args, **kwargs)
        self.conversion_map = {
            1: {
                'option_text': 'Convert to .mp4',
                'extension': 'mp4',
                'params': {
                    'vcodec': 'libx264',
                    'crf': 20,
                    'acodec': 'aac',
                    'strict': 'experimental',
                },
            },
            2: {
                'option_text': 'Convert to .mov',
                'extension': 'mov',
                'params': {
                    'vcodec': 'libx264',
                    'crf': 20,
                    'acodec': 'aac',
                    'f': 'mov',
                },
            },
            3: {
                'option_text': 'Convert to .flv',
                'extension': 'flv',
                'params': {'vcodec': 'flv1', 'acodec': 'aac', 'strict': 'experimental'},
            },
            4: {
                'option_text': 'Convert to .mkv',
                'extension': 'mkv',
                'params': {
                    'vcodec': 'copy',
                    'acodec': 'copy',
                },
            },
            5: {
                'option_text': 'Extract audio (output in .mp3)',
                'extension': 'mp3',
                'params': {
                    'ar': '44100',
                    'ac': '2',
                    'ab': '320k',
                    'f': 'mp3',
                },
            },
        }

    def run(self):
        """Run the Video command."""
        chosen_option = let_user_pick(self.conversion_map)
        source_paths, output_paths, params = self.get_user_input(
            self.conversion_map[chosen_option]
        )
        for (source_path, output_path) in list(zip(source_paths, output_paths)):
            run_ffmpeg(source_path, output_path, params, self.options)
        prmsg('completed')
