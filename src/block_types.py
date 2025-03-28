from enum import Enum

def markdown_to_blocks(markdown):
    split_markdown = markdown.strip().split("\n\n")
    strip_markdown = []
    for split in split_markdown:
        block_line = split.split("\n")
        strip_block = [line.strip() for line in block_line]
        clean_block = "\n".join(strip_block)
        if clean_block:
            strip_markdown.append(clean_block)
    return strip_markdown


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def is_ordered_list_line(line, expected_number):
    parts = line.split(' ', 1)
    return len(parts) > 1 and parts[0] == f"{expected_number}."

def block_to_block_type(block):
    split_block = block.split("\n")
    if split_block[0].startswith("#") and " " in split_block[0] and split_block[0].index(" ") <= 6:
        return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
         return BlockType.CODE
    if all(line.startswith(">") for line in split_block):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in split_block):
        return BlockType.UNORDERED_LIST
    is_ordered_list = True
    for i, line in enumerate(split_block, 1):
        if not line.startswith(f"{i}. "):
            is_ordered_list = False
            break
    if is_ordered_list:
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH