import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from markdown_parser import markdown_to_html_node


class TestTextNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://google.com" target="_blank"')

        node_no_props = HTMLNode(props=None)
        self.assertEqual(node_no_props.props_to_html(), "")

    def test_node_initialization(self):
        node1 = HTMLNode(tag="p", value="Hello", props={"class": "greeting"})
        self.assertEqual(node1.tag, "p")
        self.assertEqual(node1.value, "Hello")
        self.assertEqual(node1.props, {"class": "greeting"})

        node_empty = HTMLNode()
        self.assertIsNone(node_empty.tag)
        self.assertIsNone(node_empty.value)
        self.assertIsNone(node_empty.children)
        self.assertIsNone(node_empty.props)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        
        node2 = LeafNode("a", "test links", {"href": "https://www.google.com"})
        self.assertEqual(node2.to_html(), '<a href="https://www.google.com">test links</a>')

        node3 = LeafNode("a", None)
        with self.assertRaises(ValueError): 
            node3.to_html()

        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        child_node2 = LeafNode("spa", "chil")
        child_node3 = LeafNode("sp", "chi")
        child_node4 = LeafNode("s", "ch")
        child_node5 = LeafNode("a", "linktest", {"href": "https://biglink.com"})
        parent_node = ParentNode("div", [child_node])
        parent_node2 = ParentNode("hehe", [child_node, child_node2, child_node3, child_node4])
        parent_node3 = ParentNode("haha", [child_node5])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
        self.assertEqual(parent_node2.to_html(), "<hehe><span>child</span><spa>chil</spa><sp>chi</sp><s>ch</s></hehe>")
        self.assertEqual(parent_node3.to_html(), '<haha><a href="https://biglink.com">linktest</a></haha>')

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
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
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )