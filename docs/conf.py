# from recommonmark.parser import CommonMarkParser
extensions = ['recommonmark']
source_parsers = {
    '.md': CommonMarkParser,
    '.workbook': CommonMarkParser
}

source_suffix = ['.workbook', '.md']
