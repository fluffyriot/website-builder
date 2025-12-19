from textnode import TextNode, TextType
import re

delimiters = {
    "`": TextType.CODE,
    "_": TextType.ITALIC,
    "**": TextType.BOLD
}

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    return_list = []

    if delimiter not in delimiters:
        raise ValueError(f"Delimiter {delimiter} not supported.")
    
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            return_list.append(node)
            continue
        split_nodes = []
        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(parts)):
            if parts[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(parts[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(parts[i], delimiters[delimiter]))
        return_list.extend(split_nodes)
    
    return return_list

def extract_markdown_images(text):
    pattern = r'!\[([^\]]+)\]\((https?://[^\)]+)\)'
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    pattern = r'\[([^\]]+)\]\((https?://[^\)]+)\)'
    matches = re.findall(pattern, text)
    return matches