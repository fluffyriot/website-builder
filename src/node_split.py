from textnode import TextNode, TextType
import re

delimiters = {
    "`": TextType.CODE,
    "_": TextType.ITALIC,
    "**": TextType.BOLD
}

def extract_markdown_images(text):
    pattern = r'!\[([^\]]+)\]\((https?://[^\)]+)\)'
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    pattern = r'\[([^\]]+)\]\((https?://[^\)]+)\)'
    matches = re.findall(pattern, text)
    return matches

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

def split_nodes_image(old_nodes):
    
    return_list = []
    
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            return_list.append(node)
            continue
        original_text = node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            return_list.append(node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                return_list.append(TextNode(sections[0], TextType.TEXT))
            return_list.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            return_list.append(TextNode(original_text, TextType.TEXT))
    return return_list

def split_nodes_link(old_nodes):
    
    return_list = []
    
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            return_list.append(node)
            continue
        original_text = node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            return_list.append(node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                return_list.append(TextNode(sections[0], TextType.TEXT))
            return_list.append(
                TextNode(
                    link[0],
                    TextType.LINK,
                    link[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            return_list.append(TextNode(original_text, TextType.TEXT))
    return return_list

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
