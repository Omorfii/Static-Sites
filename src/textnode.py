import re
from enum import Enum
from htmlnode import LeafNode


class TextType(Enum):
    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK =  "link"
    IMAGE =  "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return (
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url
        )
        
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.NORMAL:
            normal_leaf = LeafNode(None, text_node.text, None)
            return normal_leaf 
        case TextType.BOLD:
            bold_leaf = LeafNode("b", text_node.text, None)
            return bold_leaf
        case TextType.ITALIC:
            italic_leaf = LeafNode("i", text_node.text, None)
            return italic_leaf
        case TextType.CODE:
            code_leaf = LeafNode("code", text_node.text, None)
            return code_leaf
        case TextType.LINK:
            link_leaf = LeafNode("a", text_node.text, {"href": text_node.url})
            return link_leaf
        case TextType.IMAGE:
            image_leaf = LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
            return image_leaf
        case _:
            raise Exception("Invalid TextType")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    split_list = []
    for nodes in old_nodes:
        if nodes.text_type != TextType.NORMAL:
            split_list.append(nodes)
            continue
        split_delimiter = nodes.text.split(delimiter)
        if len(split_delimiter) % 2 == 0:  
            raise Exception(f"Unmatched delimiter '{delimiter}' in: {nodes.text}")
        for index, part in enumerate(split_delimiter):
            if index % 2 == 0:
                split_list.append(TextNode(part, TextType.NORMAL))
            else:
                split_list.append(TextNode(part, text_type))

    return split_list
    
def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    split_list = []
    for nodes in old_nodes:
        if nodes.text_type != TextType.NORMAL:
            split_list.append(nodes)
            continue
        extracted_image = extract_markdown_images(nodes.text)
        if not extracted_image:
            split_list.append(nodes)
            continue
        remaining_text = nodes.text
        if remaining_text != "":
            for alt, url in extracted_image:
                split = remaining_text.split(f"![{alt}]({url})", 1)
                if split[0] != "":
                    split_list.append(TextNode(split[0], TextType.NORMAL))
                split_list.append(TextNode(alt, TextType.IMAGE, url))
                if len(split) > 1:
                    remaining_text = split[1]
                else:
                    remaining_text = ""
        if remaining_text:
            split_list.append(TextNode(remaining_text, TextType.NORMAL))
    return split_list

def split_nodes_link(old_nodes):
    split_list = []
    for nodes in old_nodes:
        if nodes.text_type != TextType.NORMAL:
            split_list.append(nodes)
            continue
        extracted_link = extract_markdown_links(nodes.text)
        if not extracted_link:
            split_list.append(nodes)
            continue
        remaining_text = nodes.text
        if remaining_text != "":
            for text, url in extracted_link:
                split = remaining_text.split(f"[{text}]({url})", 1)
                if split[0] != "":
                    split_list.append(TextNode(split[0], TextType.NORMAL))
                split_list.append(TextNode(text, TextType.LINK, url))
                if len(split) > 1:
                    remaining_text = split[1]
                else:
                    remaining_text = ""
        if remaining_text:
            split_list.append(TextNode(remaining_text, TextType.NORMAL))
    return split_list

def text_to_textnodes(text):
    nodes = TextNode(text, TextType.NORMAL)
    nodes = split_nodes_delimiter([nodes], "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    return split_nodes_link(nodes)
