# Fast Static Site Generator
Fast Static Site Generator (Fast SSG) - a tool for generating a complete HTML files from raw data like txt and md files. This tool was made with Python language.

## Prerequisites
- Python3
- BeautifulSoup4

## Tool installation
To install the tool run the following command
```
pip install fast-ssg==1.0.1
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
- \<code> block support for md files. Content surround by Markdown Syntax **\`code content\`** will be parsed to html `<code>...</code>`
- Horizontal rule support for md files. The Markdown `---` gets converted to an `<hr>` tag.
- If users specifies a folder for the input, automatically generates an `index.html`, which has relative links to each of the generated files.

## Usage with shorthand flags
| Description | Command |
| ------------ | -------- |
|Generate basic HTML file(s)|`fast_ssg --input "relative path or absolute path to the file or folder"`|
|Generate basic HTML file(s) with CSS stylesheet | `fast_ssg --input "relative path or absolute path to the file or folder" --stylesheet "URL to CSS stylesheet"`|
|New Feature: Support arguments passed with Config File | `fast_ssg -c ./ssg-config.json` |
|Help | `fast_ssg --help` |
|Get current version | `fast_ssg --version`|

## Shorthand flags
| Flag | Shorthand version |
| -----| ----------------- |
| `--input` | `--i` |
| `--help` | `--h` |
| `--version` | `--v` |
| `--stylesheet` | `--s`|
| `--config` | `--c`|


## Markdown
### Headers
```
# H1
## H2
## H3
```
### Links
```
[Inline-style link](https://github.com)
```
### Bold & Italic
```
**bold text**

**italic text**

***bold and italic text***
```

### Code block
```
`var x = y + z`
```

### Horizontal rule
```
---
```

| Markdown syntax | HTML equivalent |
| ------------ | -------- |
|Header 1|`<h1>Test</h1>`|
|Header 2| `<h2>Test</h2>`|
|Header 3| `<h3>Test</h3>`|
|Bold| `<b>Test</b>`|
|Italic| `<i>Test</i>`|
|Link | `<a href='URL'>Test</a>`|
|Code | `<code>Code</code>`|
|Horizontal rule | `<hr>`|

# Live version & Project-package website

https://abatomunkuev.github.io/static_site_generator/
