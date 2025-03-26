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
        case text_node.text_type.NORMAL:
            normal_leaf = LeafNode(None, text_node.text, None)
            return normal_leaf 
        case text_node.text_type.BOLD:
            bold_leaf = LeafNode("b", text_node.text, None)
            return bold_leaf
        case text_node.text_type.ITALIC:
            italic_leaf = LeafNode("i", text_node.text, None)
            return italic_leaf
        case text_node.text_type.CODE:
            code_leaf = LeafNode("code", text_node.text, None)
            return code_leaf
        case text_node.text_type.LINK:
            link_leaf = LeafNode("a", text_node.text, {"href": text_node.url})
            return link_leaf
        case text_node.text_type.IMAGE:
            image_leaf = LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
            return image_leaf
        case _:
            raise Exception("Invalid TextType")