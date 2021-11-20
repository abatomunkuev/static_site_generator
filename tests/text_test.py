import os
import shutil
import pytest
from fast_ssg.utils import determine_path
from fast_ssg.text import OUTPUT_DIR, TextFile


class TestText:
    def test_get_fullpath(self):
        parsed_arg_obj = {"input": "./tests/test_files/test_file.md"}
        path_obj = determine_path(parsed_arg_obj)
        full_path = TextFile(path_obj["file_path"], path_obj["dir_path"]).get_path()
        assert full_path == os.path.join(path_obj["dir_path"], path_obj["file_path"])

    def test_read_file(self):
        parsed_arg_obj = {"input": "./tests/test_files/test_file.md"}
        path_obj = determine_path(parsed_arg_obj)
        text_obj = TextFile(path_obj["file_path"], path_obj["dir_path"])

        # Open file
        file = open(text_obj.get_path(), mode="r", encoding="utf8")
        # Read the contents
        content = file.read()
        assert (
            content == text_obj.read_file()
        ), "Content from read_file() func should be the same as reading file directly"

    def test_genetate_html(self):
        # Create Dir path
        dir_path = os.path.join(os.getcwd(), OUTPUT_DIR)
        if os.path.isdir(dir_path):
            shutil.rmtree(dir_path)
        os.mkdir(dir_path)
        # Create Text obj
        parsed_arg_obj = {"input": "./tests/test_files/test_file.md"}
        path_obj = determine_path(parsed_arg_obj)
        text_obj = TextFile(path_obj["file_path"], path_obj["dir_path"])
        text_obj.generate_html()
        assert os.path.isfile(
            dir_path + "/test_file.html"
        ), "HTML file should exist in OUTPUT directory"

    def test_process_file_invalid_file(self):
        parsed_arg_obj = {"input": "./tests/test_files/test_unsupported_type.epub"}
        path_obj = determine_path(parsed_arg_obj)
        text_obj = TextFile(path_obj["file_path"], path_obj["dir_path"])
        # Should throw error
        with pytest.raises(Exception):
            text_obj.process_file()

    def test_process_empty_file(self):
        parsed_arg_obj = {"input": "./tests/test_files/test_empty_file.txt"}
        path_obj = determine_path(parsed_arg_obj)
        text_obj = TextFile(path_obj["file_path"], path_obj["dir_path"])
        # Should throw error
        with pytest.raises(Exception):
            text_obj.process_file()
