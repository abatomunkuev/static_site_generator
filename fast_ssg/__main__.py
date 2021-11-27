#!/usr/bin/env python
import os
import shutil
from text import OUTPUT_DIR, TextFile
from utils import cla_parser, determine_path, generate_index_html


def main():
    args_obj = cla_parser()
    path = determine_path(args_obj)
    # Create Dir path
    dir_path = os.path.join(os.getcwd(), OUTPUT_DIR)
    if os.path.isdir(dir_path):
        shutil.rmtree(dir_path)
    os.mkdir(dir_path)
    if path["file_names"]:
        # Handle a folder
        # Create a list, which will hold the paths to all files,
        # to link them in index.html
        generated_files = []
        # Generate Index html containing links to the files.
        for file_name in path["file_names"]:
            file = TextFile(file_name, path["dir_path"], args_obj["stylesheet"])
            generated_files.append(file.generate_html())
        generate_index_html(args_obj["stylesheet"], generated_files)
    else:
        # Handle single file
        file = TextFile(path["file_path"], path["dir_path"], args_obj["stylesheet"])
        file.generate_html()


if __name__ == "__main__":
    main()
