from PyQt6.QtGui import QColor, QTextCharFormat
from PyQt6.QtWidgets import QPlainTextEdit

import tree_sitter_dih as tsdih
from tree_sitter import Language, Parser, Query, QueryCursor, Point

from pathlib import Path


DIH_LANGUAGE = Language(tsdih.language())

parser = Parser(DIH_LANGUAGE)
query_file = Path(__file__).parent.parent.parent / "tree-sitter-dih" / "queries" / "highlights.scm" # lord help me.
query = Query(DIH_LANGUAGE, query_file.read_text())
query_cursor = QueryCursor(query)


def _format(color):
    _color = QColor()
    _color.setNamedColor(color)

    _qt_format = QTextCharFormat()
    _qt_format.setForeground(_color)
    return _qt_format

STYLES = {
    'keyword': _format('#e66159'),
    'string': _format('#92a132'),
    'number': _format('#d070b6')
} # from everforest


def _qt_to_ts(source, offset):
    row = source.count(b"\n", 0, offset)
    column = offset - (source.rfind(b"\n", 0, offset) + 1)
    return Point(row, column)
def _ts_to_qt(): ...


class DihEditor(QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.doc = self.document()
        self.doc.contentsChange.connect(self.on_contents_changed)

    def on_contents_changed(self, start, removed, added):
        ...
