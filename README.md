# Static Site Generator SSG
Static Site Generator (SSG) - a tool for generating a complete HTML files from raw data like txt and md files. This tool was made with Python language. 

## Prerequisites
- Python3
- BeautifulSoup4

## Beautiful Soup installation
```
pip install beautifulsoup4
```

## Tool features 
- CSS stylesheet support by specifying `--stylesheet` or `s`
- Title parsing support for txt files. First line, indicates title followed by two blank lines. This will populate the `<title>...</title>` and add `<h1>...</h1>` to the top of the `<body>...</body>`.
- Title parsing support for md files. Line starting with the Markdown syntax \# indicates the title. This will populate the `<title>...</title>` and add `<h1>...</h1>` to the top of the `<body>...</body>`.
- Header parsing support for md files. Lines starting with the Markdown syntax \#\# or \#\#\# will be parsed with `<h2>...</h2>` and `<h3>...</h3>` tags respectively.
- Italic syntax support for md files. Contents surrounded by Markdown Syntax *\*italics\** will be parsed to html `<i>...</i>` tags.
- Bold syntax support for md files. Contents surrounded by Markdown Syntax **\*\*Bold\*\*** will be parsed to html `<b>...</b>` tags.
- Bold and Italic syntax support for md files. Contents surrounded by Markdown Syntax ***\*\*\*Bold Italcs \*\*\**** will be parsed with both italic and bold html tags.
- Link syntax support for md files. Contents in Markdown Syntax \[Link\]\(url\) will be parsed to html link tags with working links.
- If users specifies a folder for the input, automatically generates an `index.html`, which has relative links to each of the generated files.

## Usage with shorthand flags
| Description | Command |
| ------------ | -------- |
|Generate basic HTML file(s)|`python3 ssg.py --input "relative path or absolute path to the file or folder"`| 
|Generate basic HTML file(s) with CSS stylesheet | `python3 ssg.py --input "relative path or absolute path to the file or folder" --stylesheet "URL to CSS stylesheet"`|
|Help | `python3 ssg.py --help` |
|Get current version | `python3 ssg.py --version`|

## Shorthand flags
| Flag | Shorthand version | 
| -----| ----------------- |
| `--input` | `--i` | 
| `--help` | `--h` |
| `--version` | `--v` | 
| `--stylesheet` | `--s`| 

# Live version

https://abatomunkuev.github.io/static_site_generator/
