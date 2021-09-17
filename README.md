# Static Site Generator SSG
Static Site Generator (SSG) - a tool for generating a complete HTML files from raw data like txt files. This tool was made with Python language. 

## Prerequisites
- Python3
- BeautifulSoup4

## Beautiful Soup installation
```
pip install beautifulsoup4
```

## Tool features 
- CSS stylesheet support by specifying `--stylesheet` or `s`
- Title parsing support. First line, indicates title followed by two blank lines. This will populate the `<title>...</title>` and add `<h1>...</h1>` to the top of the `<body>...</body>`.
- If users specifies a folder for the input, automatically generates an `index.html`, which has relative links to each of the generated files.

## Usage with shorthand flags
| Description | Command |
| ------------ | -------- |
|Generate basic HTML file(s)|`python ssg.py --input "relative path or absolute path to the file or folder"`| 
|Generate basic HTML file(s) with CSS stylesheet | `python ssg.py --input "relative path or absolute path to the file or folder" --stylesheet "URL to CSS stylesheet"`|
|Help | `python ssg.py --help` |
|Get current version | `python ssg.py --version`|

## Shorthand flags
| Flag | Shorthand version | 
| -----| ----------------- |
| `--input` | `--i` | 
| `--help` | `--h` |
| `--version` | `--v` | 
| `--stylesheet` | `--s`| 

# Live version 

https://abatomunkuev.github.io/static_site_generator/
