from bs4 import BeautifulSoup
import re
import platform
import os

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
        file = open(file_path, mode="r", encoding="utf8")
        # Read all lines at once
        contents = file.read()
        file.close()
        return contents

    def process_file(self):
        """
        Method process the contents of the txt or markdown file
        Paramerers
        ----------
        self : Object (class File)
            reference to the current instance of the class (TextFile)
        Returns
        -------
        processed_content : Dictionary
            Python dictionary containing the processed information:
            - title
            - number of paragraphs
            - paragraphs
        """
        processed_content = {}
        contents = self.read_file()
        if not contents:
            raise ValueError(
                f"Empty file - {self.file_path}. No information to process"
            )

        if self.file_path.endswith(".txt"):
            processed_content = self.process_txt_file(contents)
        elif self.file_path.endswith(".md"):
            processed_content = self.process_md_file(contents)
        else:
            raise Exception(
                f"File type - {self.file_path.split('.')[-1]} is not supported!"
            )
        return processed_content

    def process_txt_file(self, contents):
        """
        Method process the contents of the text (txt) files
        Parameters
        ----------
        self : Object (class File)
            reference to the current instance of the class (TextFile)
        contents : String
            contents of the file
        Returns
        -------
        processed_content : Dictionary
            Python dictionary containing the processed information:
            - title
            - number of paragraphs
            - paragraphs
        """

        html_content = []
        # Splitting the content of the file by new line \n\n
        splitted_content = contents.split("\n\n")
        # handle <h1> title with applied style: text-aligning to the center and margin bottom
        html_content.append(
            "<h1 style='text-align: center; margin-bottom: 15px'>{title}</h1>".format(
                title=splitted_content[0]
            )
        )
        # handle the rest of the content, wrapping it up in <p> tag
        for paragraph in splitted_content[1:]:
            html_content.append(
                "<p>{content}</p>".format(
                    content=paragraph.encode("utf8").decode("utf8")
                )
            )
        processed_content = {
            "title": splitted_content[0],
            "content": html_content,
            "num_paragraphs": len(splitted_content),
        }
        return processed_content

    def process_md_file(self, contents):
        """
        Method process the contents of the markdown files
        Parameters
        ----------
        self : Object (class File)
            reference to the current instance of the class (TextFile)
        contents : String
            contents of the file
        Returns
        -------
        processed_content : Dictionary
            Python dictionary containing the processed information:
            - title
            - number of paragraphs
            - paragraphs
        """
        content_title = ""
        html_content = []
        # Capturing Frontmatter
        frontmatter_content = re.findall("^---[\s\S]+?---", contents)
        # Removing Frontmatter from the content
        contents = re.sub("^---[\s\S]+?---\n", "", contents)
        # Splitting the content of the markdown file by a new line \n\n
        splitted_content = contents.split("\n\n")
        for content in splitted_content:
            # regex for .md syntax
            reg_h1 = re.compile("[^#]*# (.*$)")
            reg_h2 = "(^[^#])*## ([^#]+)*(.*$)"
            reg_h3 = "(^[^#])*### ([^#]+)*(.*$)"
            reg_italic = "[^\*]?\*([^\*]+)\*[^\*]?"
            reg_bold = "[^\*]?\*{2}([^\*]+)\*{2}[^\*]?"
            reg_link = "\[(.+)\]\((.+)\)"
            reg_p = "(^[^#]*$)"
            reg_newline = "\n"
            reg_code = "\`(.*)\`"
            reg_horizontal_rule = "^---$"
            # Handling newline
            content = re.sub(reg_newline, "<br>", content)
            # Handling horizontal rule
            content = re.sub(reg_horizontal_rule, "<hr>", content)
            # Handling italics and bold in italics
            content = re.sub(
                reg_italic, r"<i>\1</i>", re.sub(reg_bold, r"<b>\1</b>", content)
            )
            # Handling bold and italics in bold
            content = re.sub(
                reg_bold, r"<b>\1</b>", re.sub(reg_italic, r"<i>\1</i>", content)
            )
            # Handling code
            content = re.sub(reg_code, r"<code>\1</code>", content)
            # Handling Headers and paragraphs
            content = re.sub(reg_p, r"<p>\1</p>", content)
            content = re.sub(
                reg_h3,
                r"\1<h3 style='text-align: center; margin-bottom: 15px'>\2</h3>\3",
                content,
            )
            content = re.sub(
                reg_h2,
                r"\1<h2 style='text-align: center; margin-bottom: 15px'>\2</h2>\3",
                content,
            )
            # Handling links
            content = re.sub(reg_link, r'<a href="\2">\1</a>', content)
            if reg_h1.match(content):
                content_title = content[1:]
                html_content.append(
                    "<h1 style='text-align: center; margin-bottom: 15px'>{title}</h1>".format(
                        title=content_title
                    )
                )
            else:
                html_content.append(
                    "{content}".format(content=content.encode("utf8").decode("utf8"))
                )

        processed_content = {
            "title": content_title,
            "content": html_content,
            "num_paragraphs": len(splitted_content),
        }
        # Processing Markdown Formatter
        # Extracting title field
        if re.findall(r"title:\s*(.*)", frontmatter_content[0]):
            processed_content["title"] = re.findall(
                r"title:\s*(.*)", frontmatter_content[0]
            )[0]
        # Extracting description field
        if re.findall(r"description:\s*(.*)", frontmatter_content[0]):
            processed_content["description"] = re.findall(
                r"description:\s*(.*)", frontmatter_content[0]
            )[0]
        # Extracting upload date field
        if re.findall(r"upload_date:\s*(.*)", frontmatter_content[0]):
            processed_content["upload_date"] = re.findall(
                r"upload_date:\s*(.*)", frontmatter_content[0]
            )[0]
        # Extracting author field
        if re.findall(r"author:\s*(.*)", frontmatter_content[0]):
            processed_content["author"] = re.findall(
                r"author:\s*(.*)", frontmatter_content[0]
            )[0]
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
        path : Tuple
            String: path to the generated html file
            String: path to the link
        """

        template = """<!doctype html>
        <html lang="en">
        <head>
        <meta charset="utf-8">
        <title>{title}</title>
        <meta name="description" content={description}>
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
        description = ""
        if "description" in processed_content:
            description = processed_content["description"]
        template = template.format(
            title=processed_content["title"],
            style_sheet=stylesheet,
            content="".join(processed_content["content"]),
            description=description,
        )
        # Determine the path to the file or directory using (ternary operator)
        # Get the filename from filepath, convert it to lower case
        file_name = (
            "_".join(
                [
                    str.lower(name)
                    for name in self.file_path.split("/")[-1].split(".")[0].split(" ")
                ]
            )
            + ".html"
        )
        link_name = " ".join(
            [name for name in self.file_path.split("/")[-1].split(".")[0].split(" ")]
        )
        path = os.path.join(OUTPUT_DIR, file_name)
        html_file = open(path, "w", encoding="utf8")
        # Pretty HTML file
        soup = BeautifulSoup(template, "html.parser")
        html_file.write(soup.prettify())
        html_file.close()
        if platform.system() == "Windows":
            path = path.split("\\")[-1]
        else:
            path = path.split("/")[-1]
        return (path, link_name)
