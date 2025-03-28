import unittest

from textnode import *
from htmlnode import LeafNode, HTMLNode, ParentNode
from block_types import *

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
    
    def test_delimiter(self):
        node_list = [
            TextNode("This is a test", TextType.NORMAL),
            TextNode("This is bold", TextType.BOLD),
            TextNode("This text has no delimiter",TextType.NORMAL),
            TextNode("This text **has bold** in it",TextType.NORMAL),
            TextNode("**everything is just bold**", TextType.NORMAL),
            TextNode("This **is a test** with multiple **bold place**", TextType.NORMAL),
            TextNode("Wow italic", TextType.ITALIC)
        ]
        wrong_list = [
            TextNode("this is wrong**", TextType.NORMAL),
            TextNode("this **shouldnt work", TextType.NORMAL)
        ]
        split_delimiter = split_nodes_delimiter(node_list, "**", TextType.BOLD)
        self.assertEqual(split_delimiter, [
            TextNode("This is a test", TextType.NORMAL),
            TextNode("This is bold", TextType.BOLD),
            TextNode("This text has no delimiter", TextType.NORMAL),
            TextNode("This text ", TextType.NORMAL),
            TextNode("has bold", TextType.BOLD),
            TextNode(" in it", TextType.NORMAL),
            TextNode("", TextType.NORMAL),
            TextNode("everything is just bold", TextType.BOLD),
            TextNode("", TextType.NORMAL),
            TextNode("This ", TextType.NORMAL),
            TextNode("is a test", TextType.BOLD),
            TextNode(" with multiple ", TextType.NORMAL),
            TextNode("bold place", TextType.BOLD),
            TextNode("", TextType.NORMAL),
            TextNode("Wow italic", TextType.ITALIC)
        ])
        self.assertRaises(Exception, split_nodes_delimiter, wrong_list, "**", TextType.BOLD)
    
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        nothing = extract_markdown_images(
            "there is nothing here"
        )
        self.assertListEqual([], nothing)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)
        nothing = extract_markdown_links(
            "there is nothing here"
        )
        self.assertListEqual([], nothing)
    
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        node2 = TextNode(
            "and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)",
            TextType.NORMAL
        )
        new_nodes = split_nodes_image([node])
        link_nodes = split_nodes_image([node2])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes
        )
        self.assertListEqual([
                TextNode("and an ", TextType.NORMAL),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a [link](https://boot.dev)", TextType.NORMAL)
        ], link_nodes
        )

    def test_text_to_textnodes(self):
        node = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(node)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.NORMAL),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.NORMAL),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.NORMAL),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.NORMAL),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.NORMAL),
                TextNode("link", TextType.LINK, "https://boot.dev")
            ], new_nodes
       )
        
    def test_markdown_to_blocks(self):
        md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_block_to_block_type(self):
        block_heading = "# This is a level 1 heading (biggest)\n## This is a level 2 heading\n### This is a level 3 heading\n#### This is a level 4 heading"
        block_code = "``` this is code blablabla ```"
        block_quote = ">haha quote\n>haha other quote\n>hahahahahha quoting"
        block_unordered = "- list not ordered\n- nooo not ordered\n- hahaha"
        block_ordered = "1. first\n2. second\n3. third\n4. fourth"
        block_paragraph = "so many thing\nto say\nbecause thers\nnothing special"

        self.assertEqual(BlockType.HEADING, block_to_block_type(block_heading))
        self.assertEqual(BlockType.CODE, block_to_block_type(block_code))
        self.assertEqual(BlockType.QUOTE, block_to_block_type(block_quote))
        self.assertEqual(BlockType.UNORDERED_LIST, block_to_block_type(block_unordered))
        self.assertEqual(BlockType.ORDERED_LIST, block_to_block_type(block_ordered))
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(block_paragraph))

if __name__ == "__main__":
    unittest.main()