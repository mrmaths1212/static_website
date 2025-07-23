
import unittest
from markdown_to_node import *
from blocktypes import *
from textnode import TextNode, TextType
from blocks_to_html import *
from extractmarkdown import *
import os

class TestInlineMarkdown(unittest.TestCase):

    def test_CODEtype(self):
        md = """```This is some `inline code` in a paragraph.```"""
        type = block_to_block_type(md)
        self.assertEqual(
            type,
            BlockType.CODE,
        )

    def test_CODE(self):
        md = """```This is some `inline code` in a paragraph.```"""
        html = markdown_to_html_node(md)
        html = html.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is some `inline code` in a paragraph.</code></pre></div>",
        )
    def test_HEADINGtype(self):
        md = """# This is a heading"""
        type = block_to_block_type(md)
        self.assertEqual(
            type,
            BlockType.HEADING,
        )
    
    def test_HEADING1(self):
        md = """# This is a heading"""
        html = markdown_to_html_node(md)
        html = html.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a heading</h1></div>",
        )
    
    def test_HEADING3(self):
        md = """### This is a heading"""
        html = markdown_to_html_node(md)
        html = html.to_html()
        self.assertEqual(
            html,
            "<div><h3>This is a heading</h3></div>",
        )

    def test_QUOTEtype(self):
        md = """> This is a quote"""
        type = block_to_block_type(md)
        self.assertEqual(
            type,
            BlockType.QUOTE,
        )

    def test_QUOTE(self):
        md = """> This is a quote"""
        html = markdown_to_html_node(md)
        html = html.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote</blockquote></div>",
        )

    def test_ULtype(self):
        md = """- Item 1
    - Item 2
    - Item 3"""

        type = block_to_block_type(md)
    
        self.assertEqual(
            type,
            BlockType.UNORDERED_LIST,
        )

    def test_OLtype(self):
        md = """1. Item 1
    2. Item 2
    3. Item 3"""
        type = block_to_block_type(md)
        self.assertEqual(
            type,
            BlockType.ORDERED_LIST,
        )

    def test_OL(self):
        md = """1. Item 1
    2. Item 2
    3. Item 3
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>Item 1</li><li>Item 2</li><li>Item 3</li></ol></div>",
        )
    def test_UL(self):
        md = """- Item 1
    - Item 2
    - Item 3
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul></div>",
        )
    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


    def test_markdown_title(self):
        title = """# This is a title

This is a paragraph with some **bold** text and an _italic_ word."""
        title = extract_title(title)
        self.assertEqual(title, "# This is a title")
    
    