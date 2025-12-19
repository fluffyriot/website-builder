from textnode import TextNode

def markdown_to_blocks(markdown):
    return_list = []
    for line in markdown.split("\n\n"):
        line = line.strip()
        if line != "":
            return_list.append(line)
    return return_list