import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_neq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_dtype(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        self.assertEqual(node.text_type, TextType.ITALIC)
    
    def test_url(self):
        node = TextNode("This is a link", TextType.LINK, "https://example.com")
        self.assertEqual(node.url, "https://example.com")

    def test_imurl(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://example.com/image.png")
        node2 = TextNode("This is a link", TextType.LINK, None)
        self.assertNotEqual(node, node2)
  

if __name__ == "__main__":
    unittest.main()