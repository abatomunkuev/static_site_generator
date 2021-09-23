import argparse
import os
import shutil
import re
from bs4 import BeautifulSoup
from io import open
import platform

OUTPUT_DIR = "dist"

class TextFile:
    def __init__(self, file_path, dir_path, stylesheet=None):
        """
        Built-in method to initialize an instace of the TextFile class
        Parameters
        ----------
        self : Object (class File) 
            reference to the current instance of the class (TextFile)
        file_name : String 
            filename 
        dir_path : String
            path to the directory
        """
        self.file_path = file_path
        self.dir_path = dir_path
        self.stylesheet = stylesheet

    def get_path(self):
        """
        Method returns an absolute path to the file
        Parameters
        ----------
        self : Object (class File) 
            reference to the current instance of the class (TextFile)
        
        Returns
        -------
        path : String
            Absolute path to the file.
        """
        return os.path.join(self.dir_path, self.file_path)

    def read_file(self):
        """
        Method reads a file that needs to be processed to HTML page
        Parameters
        ----------
        self : Object (class File) 
            reference to the current instance of the class (TextFile)
        Returns
        ------- 
        content : Array(str)
            Content array 
        """
        # Get path
        file_path = self.get_path()
        # Open a file
        file = open(file_path, mode='r', encoding='utf8')
        # Read all lines at once 
        contents = file.read()
        file.close()
        return contents

    def process_file(self):
        """
        Method process the contents of the file
        Paramerers
        ----------
        self : Object (class File) 
            reference to the current instance of the class (TextFile)
        Returns
        -------
        processed_content : Dictionary
            Python dictionary containing the processed information: title, number of paragraphs, paragraphs
        """
        contents = self.read_file()
        if (self.file_path.endswith(".txt")):
            # Splitting the content of the file by new line \n\n
            splitted_content = contents.split("\n\n")
            html_p = []
            # handle <h1> title with applied style: text-aligning to the center and margin bottom
            html_p.append("<h1 style='text-align: center; margin-bottom: 15px'>{title}</h1>".format(title=splitted_content[0]))
            # handle the rest of the content, wrapping it up in <p> tag
            for paragraph in splitted_content[1:]:
                # Handle encoding for windows
                if platform.system() == "Windows":
                    html_p.append("<p>{content}</p>".format(content=paragraph.encode('utf8').decode('utf8')))
                # Handle encoding for Mac and other platforms
                else:
                    html_p.append("<p>{content}</p>".format(content=paragraph.encode('utf8')))
            processed_content = {
                "title": splitted_content[0],
                "content": html_p,
                "num_paragraphs": len(splitted_content)
            }
        elif (self.file_path.endswith(".md")): 
            splitted_content = contents.split("\n\n")
            html_p=[]
            content_title = ""
            for content in splitted_content:
                # regex for .md syntax
                reg_h1 = re.compile('^# .+')
                reg_h2 = re.compile('^## .+')
                reg_italic = re.compile('[^\*]\*[^\*]+\*[^\*]')
                reg_bold = re.compile('[^\*]?\*{2}[^\*]+\*{2}[^\*]?')

                # Handling italics
                result_italic = reg_italic.findall(content)
                if (result_italic):
                    for phrase in result_italic:
                        new_phrase = phrase.replace("*", "<i>", 1)
                        new_phrase = new_phrase.replace("*", "</i>")
                        content = content.replace(phrase, new_phrase, 1)

                # Handling bold
                result_bold = reg_bold.findall(content)
                if (result_bold):
                    for phrase in result_bold:
                        new_phrase = phrase.replace("**", "<b>", 1)
                        new_phrase = new_phrase.replace("**", "</b>")
                        content = content.replace(phrase, new_phrase, 1)

                # Handling Headers
                if (reg_h1.match(content)):
                    content_title = content[1:]
                    html_p.append("<h1 style='text-align: center; margin-bottom: 15px'>{title}</h1>".format(title=content_title))
                elif (reg_h2.match(content)):
                    html_p.append("<h2 style='text-align: center; margin-bottom: 15px'>{subtitle}</h2>".format(subtitle=content[2:]))
                else:
                    # Handle encoding for windows
                    if platform.system() == "Windows":
                        html_p.append("<p>{content}</p>".format(content=content.encode('utf8').decode('utf8')))
                    # Handle encoding for Mac and other platforms
                    else:
                        html_p.append("<p>{content}</p>".format(content=content.encode('utf8')))
            processed_content = {
                "title": content_title,
                "content": html_p,
                "num_paragraphs": len(splitted_content)
            }
        return processed_content

    def generate_html(self):
        """
        Method generates an HTML file from the processed content
        Paramerers
        ----------
        self : Object (class File) 
            reference to the current instance of the class (TextFile)
        Returns
        -------
        path : String 
            path to the generated html file
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
        {content}
        </body>
        </html>"""
        # Determining stylesheet
        stylesheet = self.stylesheet if self.stylesheet else ""
        processed_content = self.process_file()
        template = template.format(title=processed_content['title'], style_sheet=stylesheet, content="".join(processed_content['content']))
        # Determine the path to the file or directory using (ternary operator)
        # Get the filename from filepath, convert it to lower case
        file_name = "_".join([str.lower(name) for name in self.file_path.split("/")[-1].split(".")[0].split(" ")]) + ".html"
        link_name = " ".join([name for name in self.file_path.split("/")[-1].split(".")[0].split(" ")])
        path = os.path.join(OUTPUT_DIR,file_name)
        html_file = open(path, 'w', encoding='utf8')
        # Pretty HTML file 
        soup = BeautifulSoup(template, 'html.parser')
        html_file.write(soup.prettify())
        html_file.close()
        if platform.system() == "Windows":
            path = path.split("\\")[-1]
        else:
            path = path.split("/")[-1]
        return (path,link_name)
        



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
    for path,name in links:
        links_a.append("<a href='{path}'>{name}</a>".format(path=path, name=name))
    
    template = template.format(title="Static Site Generator", style_sheet=stylesheet_index, links="<br>".join(links_a))
    path = os.path.join(OUTPUT_DIR,"index.html")
    html_file = open(path, 'w')
    # Pretty HTML file 
    soup = BeautifulSoup(template, 'html.parser')
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
    path = parsed_args['input'] if os.path.isabs(parsed_args['input']) else os.path.join(os.getcwd(), parsed_args['input'])
    # Creating an object, that will contain paths to the file or directory
    path_obj = {
        "file_path": None,
        "dir_path": None,
        "file_names": []
    }
    # Check if the path is a file
    if (os.path.isfile(path)):
        path_obj['file_path'] = path
        path_obj['dir_path'] = "/".join(path.split("/")[:-1])
    # Check if the path is a directory   
    elif (os.path.isdir(path)):
        path_obj['dir_path'] = path
        filenames = []
        # Read only files which ends with .txt or .md
        for file in os.listdir(path):
            if (file.endswith(".txt") or file.endswith(".md")):
                filenames.append(file)
        path_obj['file_names'] = filenames
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
        input - command line argument that has a path to the file or folder that needs to be processed
        version - command line argument 
    ) 
    """
    # Creating argparser object
    # https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser
    parser = argparse.ArgumentParser(description="Static Site Generator - is a tool to generate HTML files from raw data like txt files.")
    parser.add_argument('-i','--input', type=str,required=True,metavar='',help='path to the file or folder that needs to be processed')
    # --version -v argument
    parser.add_argument("-v", "--version", action="version", version="Static Site Generator 0.1", help="show program's version number and exit")
    # --stylesheet -s argument 
    parser.add_argument("-s", "--stylesheet", metavar='',help="URL stylesheet to be used in generated HTML files")
    # Parse the command line arguments
    args = parser.parse_args()
    parsed_args = {
        'input': args.input,
        'stylesheet': args.stylesheet if args.stylesheet else None
    }
    return parsed_args


if __name__ == "__main__":
    args_obj = cla_parser()
    path = determine_path(args_obj)
    # Create Dir path
    dir_path = os.path.join(os.getcwd(), OUTPUT_DIR)
    if (os.path.isdir(dir_path)):
        shutil.rmtree(dir_path)
    os.mkdir(dir_path)
    if path['file_names']:
        # Handle a folder 
        # Create a list, which will hold the paths to all files, to link them in index.html
        generated_files = []
        # Generate Index html containing links to the files.
        for file_name in path['file_names']:
            file = TextFile(file_name,path['dir_path'],args_obj['stylesheet'])
            generated_files.append(file.generate_html())
        generate_index_html(args_obj['stylesheet'], generated_files)
    else:
        # Handle single file 
        file = TextFile(path['file_path'],path['dir_path'],args_obj['stylesheet'])
        file.generate_html()