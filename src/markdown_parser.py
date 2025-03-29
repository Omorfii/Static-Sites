import re
from textnode import text_node_to_html_node, text_to_textnodes, TextNode, TextType
from htmlnode import HTMLNode, ParentNode, LeafNode
from block_types import BlockType, block_to_block_type, markdown_to_blocks

def text_to_children(text):
    text = text.replace("\n", " ")
    text_nodes = text_to_textnodes(text)
    html_node = []
    for text_node in text_nodes:
        html_node.append(text_node_to_html_node(text_node))
    return html_node

def count_heading_level(text):
    header = text.strip() 
    level = 0
    for char in header:
        if char == "#":
            level += 1
        else:
            break
    return min(level, 6)

def removing_header_mark(text):
    index = 0
    while index < len(text) and text[index] == "#":
        index += 1
    while index < len(text) and text[index].isspace():
        index += 1
    result = "" 
    return text[index:]
    
def removing_code_mark(text): 
    lines = text.split("\n")
    if len(lines) == 1:
        return text.strip("```").strip()
    
    first_line = lines[0]
    if first_line.startswith("```"):
        first_line = first_line[3:].strip()  

    last_line = lines[-1]
    if last_line.endswith("```"):
        last_line = last_line[:-3].strip()
    elif last_line.strip() == "```":
        last_line = "" 

    result_lines = [first_line] + lines[1:-1] + ([last_line] if last_line else [])
    return "\n".join(result_lines)

def is_ordered_list(line):
    return bool(re.match(r'^\s*\d+\.\s', line))

def is_unordered_list(line):
    return line.startswith("- ")

def making_line_list(text):
    split_text = text.split("\n")
    result = []
    for line in split_text:
        stripped_line = line.strip()
        if is_ordered_list(stripped_line) or is_unordered_list(stripped_line):
            # Extract the content after the marker
            content = re.sub(r'^\s*(?:\d+\.|\-)\s+', '', stripped_line)
            # Create a proper list item with children
            li_node = ParentNode("li", text_to_children(content))
            result.append(li_node)
    return result
            
def deleting_markdown_quote(text):
    split_text = text.split("\n")
    result = []
    for line in split_text:
        stripped_line = line.strip()
        content = re.sub(r'^\s*>\s?', '', stripped_line)
        result.append(content)
    return "\n".join(result)

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_node = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                node = ParentNode("p", text_to_children(block))
            case BlockType.HEADING:
                level = count_heading_level(block)
                node = ParentNode(f"h{level}", text_to_children(removing_header_mark(block)))
            case BlockType.CODE:
                code_content = removing_code_mark(block)
                if code_content.startswith("\n"):
                   code_content = code_content[1:]
                if not code_content.endswith("\n"):
                    code_content += "\n"
                code_node = text_node_to_html_node(TextNode(code_content, TextType.CODE))
                node = ParentNode("pre", [code_node])
            case BlockType.UNORDERED_LIST:
                unordered_line = making_line_list(block)
                node = ParentNode("ul", unordered_line)
            case BlockType.ORDERED_LIST:
                ordered_line = making_line_list(block)
                node = ParentNode("ol", ordered_line)
            case BlockType.QUOTE:
                quote_content = deleting_markdown_quote(block)
                node = ParentNode("blockquote", text_to_children(quote_content))
                
        html_node.append(node)
    
    parent_node = ParentNode("div", html_node)
    return parent_node
