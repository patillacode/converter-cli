from .base import Base

from .utils import let_user_pick


class Video(Base):
    """Get user input to execute different video conversions"""

    def __init__(self, options, *args, **kwargs):
        super(Video, self).__init__(options, *args, **kwargs)
        self.conversion_map = {
            1: {
                'option_text': 'Convert to .mp4',
                'extension': 'mp4',
                'params': {
                    'vcodec': 'libx264',
                    'crf': 20,
                    'acodec': 'aac',
                    'strict': 'experimental'
                }
            },
            2: {
                'option_text': 'Convert to .mov',
                'extension': 'mov',
                'params': {
                    'vcodec': 'libx264',
                    'crf': 20,
                    'acodec': 'aac',
                    'f': 'mov',
                }
            },
            3: {
                'option_text': 'Convert to .flv',
                'extension': 'flv',
                'params': {
                    'vcodec': 'flv1',
                    'acodec': 'aac',
                    'strict': 'experimental'
                }
            },
            4: {
                'option_text': 'Convert to .mkv',
                'extension': 'mkv',
                'params': {
                    'vcodec': 'copy',
                    'acodec': 'copy',
                }
            },
            5: {
                'option_text': 'Extract audio (output in .mp3)',
                'extension': 'mp3',
                'params': {
                    'ar': '44100',
                    'ac': '2',
                    'ab': '320k',
                    'f': 'mp3',
                }
            }
        }

    def run(self):
        """Run the Video command."""
        self.convert(self.conversion_map[let_user_pick(self.conversion_map)])
