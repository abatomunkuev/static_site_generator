from bs4 import BeautifulSoup
import json
from io import open
import argparse
import os
from ssg.text import OUTPUT_DIR


def generate_index_html(stylesheet, links):
    """
    Function generates index.html file, containing the links to the generated pages.
    Parameters
    ----------
    stylesheet : String
        URL string to CSS
    links : Tuple
        Tuple contains the absolute path of the generated file, and name of the generated file
    """
    template = """<!doctype html>
        <html lang="en">
        <head>
        <meta charset="utf-8">
        <title>{title}</title>
        <link rel="stylesheet" href={style_sheet}>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        </head>
        <body>
        <h1 style='text-align: center; margin-bottom: 15px'>Generated Pages</h1>
        {links}
        </body>
        </html>"""

    # Determining stylesheet
    stylesheet_index = stylesheet if stylesheet else ""
    # Creating a list of <a> tags, containing links to the generated files
    links_a = []
    for path, name in links:
        links_a.append("<a href='{path}'>{name}</a>".format(path=path, name=name))

    template = template.format(
        title="Static Site Generator",
        style_sheet=stylesheet_index,
        links="<br>".join(links_a),
    )
    path = os.path.join(OUTPUT_DIR, "index.html")
    html_file = open(path, "w")
    # Pretty HTML file
    soup = BeautifulSoup(template, "html.parser")
    html_file.write(soup.prettify())
    html_file.close()


def determine_path(parsed_args):
    """
    Function determines the path to the file or directory
    Parameters
    ----------
    parsed_args : ArgumentParser(obj)
        ArgumentParser object containing parsed arguments.
    Returns
    -------
    path_obj : Dictionary
        Python dictionary containing the file path and directory path
    """
    # Determine the path to the file or directory using (ternary operator)
    path = (
        parsed_args["input"]
        if os.path.isabs(parsed_args["input"])
        else os.path.join(os.getcwd(), parsed_args["input"])
    )
    # Creating an object, that will contain paths to the file or directory
    path_obj = {"file_path": None, "dir_path": None, "file_names": []}
    # Check if the path is a file
    if os.path.isfile(path):
        path_obj["file_path"] = path
        path_obj["dir_path"] = "/".join(path.split("/")[:-1])
    # Check if the path is a directory
    elif os.path.isdir(path):
        path_obj["dir_path"] = path
        filenames = []
        # Read only files which ends with .txt or .md
        for file in os.listdir(path):
            if file.endswith(".txt") or file.endswith(".md"):
                filenames.append(file)
        path_obj["file_names"] = filenames
    else:
        raise ValueError("Please, provide the correct path to the file or directory")

    return path_obj


def cla_parser():
    """
    Function parses command line arguments.
    Parameters
    ----------
    Returns
    ------
    Python dictionary containing all the necessary information (
        input - command line argument that has a path to the file or folder needs to be processed
        version - command line argument
    )
    """
    # Creating argparser object
    # https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser
    parser = argparse.ArgumentParser(
        description=(
            """Static Site Generator - is a tool to generate
        HTML files from raw data like txt files."""
        )
    )
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        metavar="",
        help="path to the file or folder that needs to be processed",
    )
    # --version -v argument
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="Static Site Generator 0.1",
        help="show program's version number and exit",
    )
    # --stylesheet -s argument
    parser.add_argument(
        "-s",
        "--stylesheet",
        metavar="",
        help="URL stylesheet to be used in generated HTML files",
    )
    # --config -c argument
    parser.add_argument(
        "-c",
        "--config",
        metavar="",
        help=(
            """Users want to be able to specify all of their SSG options
        in a JSON formatted configuration file instead of having to pass
        them all as command line arguments every time"""
        ),
    )
    # Parse the command line arguments
    args = parser.parse_args()
    # if argument passed is config
    if args.config:
        with open(args.config) as f:
            try:
                stored_data = json.load(f)
                # print(stored_data)
                if len(stored_data) == 0:
                    print("JSON file not found:(\n Please update!\n")
                    exit(1)
            except Exception:
                print("\nError in reading Config File")
                exit(1)
            for value in stored_data:
                if value == "input" or value == "i":
                    input = stored_data[value]
                elif value == "stylesheet" or value == "s":
                    stylesheet = stored_data[value]
                if input is None:
                    print("No input file specified")
                    exit(1)
                    # parsing the arguments from config JSON file
            parsed_args = {
                "input": input if input else None,
                "stylesheet": stylesheet if stylesheet else None,
                "config": args.config,
            }
    elif args.input:
        parsed_args = {
            "input": args.input,
            "stylesheet": args.stylesheet if args.stylesheet else None,
        }
    return parsed_args
