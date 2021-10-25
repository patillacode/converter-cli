import builtins
import os

import mock
import pytest
from converter_utils import (let_user_pick, multi_source, single_source,
                             user_confirmed, validate_path)


class TestUserInput(object):
    def setup(self):
        self.conversion_map = {1: {'option_text': 'bar'}, 2: {'option_text': 'foo'}}
        self.file_path = os.path.abspath(__file__)
        self.folder_path = os.path.dirname(self.file_path)

    def test_let_user_pick_success(self):
        """ """
        for option in self.conversion_map.keys():
            with mock.patch.object(builtins, 'input', lambda _: option):
                assert let_user_pick(self.conversion_map) == option

    def test_let_user_pick_fail(self):
        """ """
        with mock.patch.object(builtins, 'input', lambda _: 'f'):
            with pytest.raises(SystemExit) as pytest_wrapped_e:
                let_user_pick(self.conversion_map)
            assert pytest_wrapped_e.type == SystemExit
            assert pytest_wrapped_e.value.code == 2

    def test_single_source(self):
        """ """
        with mock.patch.object(builtins, 'input', lambda _: self.file_path):
            source_path, source_name, source_folder = single_source()
            assert source_path == self.file_path
            assert source_name == 'test_utils'
            assert source_folder == self.folder_path

    def test_multi_source(self):
        """ """
        with mock.patch.object(builtins, 'input', side_effect=[self.folder_path, 'mp4']):
            source_folder, source_extension = multi_source()
            assert source_folder == self.folder_path + '/'
            assert source_extension == 'mp4'

    def test_user_confirmed(self):
        options = {
            'True': ['y', 'yes', 'Y', ''],
            'False': ['n', 'no', 'N', 'random', 3, '#'],
        }
        for key, val in options.items():
            for input_value in val:
                assert user_confirmed(input_value) is eval(key)


class TestPathValidation(object):
    def setup(self):
        self.file_path = os.path.abspath(__file__)
        self.folder_path = os.path.dirname(self.file_path)

    def test_validate_path_success(self):
        """ """
        assert validate_path(self.file_path, 'file') == self.file_path
        assert validate_path(self.folder_path, 'folder') == self.folder_path + '/'

    def test_validate_path_fail(self):
        """ """
        paths = [
            {'path': '/random/path/', 'sys': 1, 'type': 'foo'},
            {'path': '/random/path/to/file.ext', 'sys': 2, 'type': 'file'},
            {'path': '/random/path/to/folder', 'sys': 2, 'type': 'folder'},
        ]

        for path in paths:
            with pytest.raises(SystemExit) as pytest_wrapped_e:
                validate_path(path['path'], path['type'])
            assert pytest_wrapped_e.type == SystemExit
            assert pytest_wrapped_e.value.code == path['sys']
