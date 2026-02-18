# Темная тема Solarized для подсветки синтаксиса
from pygments.style import Style
from pygments.token import Keyword, Name, Comment, String, Error, \
    Number, Operator, Generic, Token, Punctuation


class SolarizedDarkStyle(Style):
    background_color = "#002b36"
    styles = {
        Token: '#839496',
        Comment: '#586e75',
        Comment.Preproc: '#cb4b16',
        Keyword: '#859900',
        Keyword.Type: '#b58900',
        Operator: '#839496',
        Punctuation: '#839496',
        Name: '#839496',
        Name.Function: '#268bd2',
        Name.Class: '#b58900',
        Name.Decorator: '#cb4b16',
        Name.Namespace: '#cb4b16',
        Name.Exception: '#cb4b16',
        Name.Variable: '#839496',
        Name.Constant: '#b58900',
        Name.Attribute: '#839496',
        Name.Tag: '#268bd2',
        String: '#2aa198',
        String.Char: '#2aa198',
        String.Doc: '#586e75',
        String.Double: '#2aa198',
        String.Escape: '#cb4b16',
        String.Interpol: '#cb4b16',
        String.Other: '#2aa198',
        String.Regex: '#dc322f',
        String.Single: '#2aa198',
        String.Symbol: '#2aa198',
        Number: '#d33682',
        Number.Float: '#d33682',
        Number.Hex: '#d33682',
        Number.Integer: '#d33682',
        Number.Oct: '#d33682',
        Generic: '#839496',
        Generic.Deleted: '#dc322f',
        Generic.Emph: '#839496',
        Generic.Error: '#dc322f',
        Generic.Heading: '#839496',
        Generic.Inserted: '#859900',
        Generic.Output: '#586e75',
        Generic.Prompt: '#839496',
        Generic.Strong: '#839496',
        Generic.Subheading: '#839496',
        Generic.Traceback: '#dc322f',
        Error: '#dc322f',
    }