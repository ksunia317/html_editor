# Темная тема Dracula для подсветки синтаксиса
from pygments.style import Style
from pygments.token import Keyword, Name, Comment, String, Error, \
    Number, Operator, Generic, Token, Punctuation


class DraculaDarkStyle(Style):
    background_color = "#282a36"
    styles = {
        Token: '#f8f8f2',
        Comment: '#6272a4',
        Comment.Preproc: '#ff79c6',
        Keyword: '#ff79c6',
        Keyword.Type: '#8be9fd',
        Operator: '#ff79c6',
        Punctuation: '#f8f8f2',
        Name: '#f8f8f2',
        Name.Function: '#50fa7b',
        Name.Class: '#8be9fd',
        Name.Decorator: '#ff79c6',
        Name.Namespace: '#ff79c6',
        Name.Exception: '#ff79c6',
        Name.Variable: '#f8f8f2',
        Name.Constant: '#bd93f9',
        Name.Attribute: '#50fa7b',
        Name.Tag: '#ff79c6',
        String: '#f1fa8c',
        String.Char: '#f1fa8c',
        String.Doc: '#6272a4',
        String.Double: '#f1fa8c',
        String.Escape: '#ff79c6',
        String.Interpol: '#ff79c6',
        String.Other: '#f1fa8c',
        String.Regex: '#f1fa8c',
        String.Single: '#f1fa8c',
        String.Symbol: '#f1fa8c',
        Number: '#bd93f9',
        Number.Float: '#bd93f9',
        Number.Hex: '#bd93f9',
        Number.Integer: '#bd93f9',
        Number.Oct: '#bd93f9',
        Generic: '#f8f8f2',
        Generic.Deleted: '#ff5555',
        Generic.Emph: '#f8f8f2',
        Generic.Error: '#ff5555',
        Generic.Heading: '#f8f8f2',
        Generic.Inserted: '#50fa7b',
        Generic.Output: '#6272a4',
        Generic.Prompt: '#f8f8f2',
        Generic.Strong: '#f8f8f2',
        Generic.Subheading: '#f8f8f2',
        Generic.Traceback: '#ff5555',
        Error: '#ff5555',
    }