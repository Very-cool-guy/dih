from PyQt6.QtGui import QColor, QTextCharFormat, QTextCursor
from PyQt6.QtWidgets import QPlainTextEdit

import tree_sitter_dih as tsdih
from tree_sitter import Language, Parser, Query, QueryCursor, Point

from pathlib import Path


DIH_LANGUAGE = Language(tsdih.language())

parser = Parser(DIH_LANGUAGE)
query_file = Path(__file__).parent.parent.parent.parent / "tree-sitter-dih" / "queries" / "highlights.scm" # lord help me.
query = Query(DIH_LANGUAGE, query_file.read_text())
query_cursor = QueryCursor(query)


def _format(color: str) -> QTextCharFormat:
    """Helper to return Qt text format of given hex color"""
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


# hate text encodings btw when i say byte i mean utf8 and when i say unicode i mean utf16
def _bytes_to_point(source: bytes, pos: int) -> tuple[int, int]:
    """Convert position in text given by byte number to Point"""
    row = source.count(b"\n", 0, pos)
    column = pos - (source.rfind(b"\n", 0, pos) + 1)
    return row, column

def _point_to_bytes(source: bytes, point: Point) -> int:
    """Convert position in text given by Point to byte number"""
    lines = source.split(b"\n")
    row = point.row
    column = point.column
    return sum(len(line) + 1 for line in lines[:row]) + column

def _bytes_to_unicode(source: bytes, pos: int) -> int:
    """Convert position in text given by byte number to unicode number"""
    prefix = source[:pos]
    return len(prefix.decode("utf-8").encode("utf-16-le")) // 2

def _unicode_to_bytes(source: str, pos: int) -> int:
    """Convert position in text given by unicode number to byte number"""
    prefix = source.encode("utf-16-le")[:pos*2]
    return len(prefix.decode("utf-16-le").encode("utf-8"))


class DihEditor(QPlainTextEdit):
    def __init__(self) -> None:
        super().__init__()

        self.doc = self.document()
        self.text_cursor = QTextCursor(self.doc)
        self.tree = parser.parse(b"") # open file or string later

        self.doc.contentsChange.connect(self.on_contents_changed) # pyright: ignore

    def on_contents_changed(self, start, removed, added):
        text = self.doc.toPlainText() # pyright: ignore
        text_bytes = text.encode("utf-8")

        start_byte = _unicode_to_bytes(text, start)
        old_end_byte = _unicode_to_bytes(text, start+removed)
        new_end_byte = _unicode_to_bytes(text, start+added)
        self.tree.edit(
            start_byte=start_byte, old_end_byte=old_end_byte, new_end_byte=new_end_byte,
            start_point = _bytes_to_point(text_bytes, start_byte),
            old_end_point = _bytes_to_point(text_bytes, old_end_byte),
            new_end_point = _bytes_to_point(text_bytes, new_end_byte)
        )
        self.tree = parser.parse(text.encode("utf-8"), self.tree)

        captures = query_cursor.captures(self.tree.root_node)
        for capture in captures.keys():
            for node in captures[capture]:
                start_char = _bytes_to_unicode(text_bytes, node.start_byte)
                end_char = _bytes_to_unicode(text_bytes, node.end_byte)

                self.text_cursor.setPosition(start_char, QTextCursor.MoveMode.MoveAnchor)
                self.text_cursor.setPosition(end_char, QTextCursor.MoveMode.KeepAnchor)
                self.text_cursor.setCharFormat(STYLES[capture])
