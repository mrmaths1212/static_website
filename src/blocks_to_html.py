from HTMLNode import *
from textnode import *
from blocktypes import *
from markdown_to_node import *


def text_to_children(text):
    t=[]
    for text_node in text_to_textnodes(text):
        t.append(text_node_to_html_node(text_node))
    return t

def OL_to_node(ol):
    li_nodes = []
    lines = ol.splitlines()
    for line in lines:
        line = line.strip()
        match = re.match(r"^\s*\d+\.\s+(.*)", line)
        if not match:
            raise ValueError(f"Invalid ordered list format at line: '{line}'")
        

        # Enlève "1. ", "2. ", etc.
        item_text = match.group(1).strip()
        li_nodes.append(ParentNode(tag="li", children=text_to_children(item_text)))
    return ParentNode(tag="ol", children=li_nodes)

def UL_to_node(ul):
    li_nodes = []
    lines = ul.splitlines()
    for line in lines:
        line = line.strip()
        match = re.match(r"^\s*\-\s+(.*)", line)
        if not match:
            raise ValueError(f"Invalid ordered list format at line: '{line}'")
        

        # Enlève "1. ", "2. ", etc.
        item_text = match.group(1).strip()
        li_nodes.append(ParentNode(tag="li", children=text_to_children(item_text)))
    return ParentNode(tag="ul", children=li_nodes)

def quote_to_node(quote):
    lines = quote.splitlines()
    quote_lines = [line.lstrip('> ') for line in lines]
    quote_text = '\n'.join(quote_lines)
    return ParentNode(tag="blockquote", children=text_to_children(quote_text))

def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.HEADING:
            level = len(block.split(' ')[0])
            text = block[level+1:]
            children.append(ParentNode(tag=f'h{level}', children=text_to_children(text)))

        elif block_type == BlockType.PARAGRAPH:
            cleaned_block = block.replace("\n", " ")
            cleaned_block = re.sub(r"\s+", " ", cleaned_block).strip()
            children.append(ParentNode(tag="p", children=text_to_children(cleaned_block)))

        elif block_type == BlockType.CODE:
            code_content = block.strip("```").strip(" ")
            code_node = text_node_to_html_node(TextNode(code_content, TextType.CODE))
            children.append(ParentNode(tag="pre", children=[code_node]))

        elif block_type == BlockType.QUOTE:
            quote_lines = [line.lstrip('> ') for line in block.splitlines()]
            quote_text = '\n'.join(quote_lines)
            children.append(ParentNode(tag="blockquote", children=text_to_children(quote_text)))

        elif block_type == BlockType.UNORDERED_LIST:
            children.append(UL_to_node(block))

        elif block_type == BlockType.ORDERED_LIST:
            children.append(OL_to_node(block))

    return ParentNode(tag="div", children=children)
