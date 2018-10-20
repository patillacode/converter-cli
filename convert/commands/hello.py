"""The hello command."""


from json import dumps

from .base import Base


class Hello(Base):
    """Say hello, world!"""

    def run(self):
        print('Hello, world!')
