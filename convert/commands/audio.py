from .base import Base

from .utils import let_user_pick


class Audio(Base):
    """Get user input to execute different video conversions"""

    def __init__(self, options, *args, **kwargs):
        super(Audio, self).__init__(options, *args, **kwargs)
        self.conversion_map = {
            1: {
                'option_text': 'Convert to .mp3 (320k)',
                'extension': 'mp3',
                'params': {
                    'ar': 44100,
                    'ac': 2,
                    'ab': '320k ',
                    'f': 'mp3'
                }
            },
            2: {
                'option_text': 'Convert to .wav',
                'extension': 'wav',
                'params': {}
            }
        }

    def run(self):
        """Run the Audio command."""
        self.convert(self.conversion_map[let_user_pick(self.conversion_map)])
