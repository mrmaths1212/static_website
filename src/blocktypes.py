from enum import Enum

class BlockType(Enum):
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    PARAGRAPH = "paragraph"

def markdown_to_blocks(markdown):
    # Split by double newlines (paragraph separator)
    raw_blocks = markdown.split('\n\n')
    
    # Strip whitespace and remove empty blocks
    blocks = [block.strip() for block in raw_blocks if block.strip() != '']
    
    return blocks

def block_to_block_type(block):
    lines = block.split('\n')

    # Heading (starts with 1–6 '#' followed by a space)
    if lines[0].startswith('#') and len(lines[0].split(' ')[0]) <= 6 and lines[0][len(lines[0].split(' ')[0])] == ' ':
        return BlockType.HEADING

    # Code block (starts and ends with ```)
    if block.startswith('```') and block.endswith('```'):
        return BlockType.CODE

    # Quote block (each line starts with '>')
    if all(line.startswith('>') for line in lines):
        return BlockType.QUOTE

    # Unordered list block (each line starts with '- ')
    if all(line.strip().startswith('- ') for line in lines):
        return BlockType.UNORDERED_LIST

    # Ordered list block (lines like 1. , 2. , 3. , ...)
    is_ordered = True
    for i, line in enumerate(lines, 1):
        if not line.strip().startswith(f"{i}. "):
            is_ordered = False
            break
    if is_ordered:
        return BlockType.ORDERED_LIST

    # Default to paragraph
    return BlockType.PARAGRAPH
