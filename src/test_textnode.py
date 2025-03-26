import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import LeafNode, HTMLNode, ParentNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("Diferent text node", TextType.NORMAL)
        node4 = TextNode("this is a none url", TextType.LINK, None)
        self.assertEqual(node, node2)
        self.assertNotEqual(node2, node3)

    def test_text(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")


if __name__ == "__main__":
    unittest.main()