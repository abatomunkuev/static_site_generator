from ssg import determine_path
import pytest
import subprocess


class TestUtils:
    def test_determine_path_good_file(self):
        """
        Test function that checks the output of
        determine_path function by providing good
        input file path value
        """
        parsed_arg_obj = {"input": "./tests/test_files/test_file.md"}
        path_obj = determine_path(parsed_arg_obj)
        assert (
            path_obj["file_path"] is not None
        ), "Path object should contain a path to the file"
        assert (
            path_obj["dir_path"] is not None
        ), "Path object should contain a corresponding directory"

    def test_determine_path_invalid_file(self):
        """
        Test function that checks the output of
        determine_path function by providing invalid
        input value
        """
        parsed_arg_obj = {"input": "../../invalid_file_path"}
        # Should throw ValueError
        with pytest.raises(ValueError):
            determine_path(parsed_arg_obj)

    def test_determine_path_dir_file(self):
        """
        Test function that checks the output of
        determine_path function by providing good
        input directory path value
        """
        parsed_arg_obj = {"input": "./tests/test_files"}
        path_obj = determine_path(parsed_arg_obj)
        assert (
            path_obj["file_names"] is not None
        ), "Path object should contain file_names that are in directory"
        assert (
            path_obj["dir_path"] is not None
        ), "Path object should contain a corresponding directory"

    def test_cla_parser_version_arg(self):
        """
        Test function checks cla parser output by providing
        --version input argument
        """
        # Check short-cut -v
        shortcut_version_output = subprocess.check_output(
            "python3 -c 'from ssg import cla_parser; cla_parser()' -v", shell=True
        )
        assert (
            shortcut_version_output.decode("utf-8") == "Static Site Generator 0.1\n"
        ), 'Should output "Static Site Generator 0.1"'
        # Check full argument --version
        full_version_output = subprocess.check_output(
            "python3 -c 'from ssg import cla_parser; cla_parser()' --version",
            shell=True,
        )
        assert (
            full_version_output.decode("utf-8") == "Static Site Generator 0.1\n"
        ), 'Should output "Static Site Generator 0.1"'

    def test_cla_parser_invalid_input_arg(self):
        """
        Test case when we pass an invalid input argument value
        """
        # Should throw error
        with pytest.raises(Exception):
            subprocess.check_output("python3 ssg.py -i ../../invalid_path", shell=True)
