import math

def __write_heading(file, text, block_width, comment_type, filler):
    heading_spacing = (block_width - 2) - len(text)
    if heading_spacing % 2 != 0:
        heading_spacing_r = math.ceil(heading_spacing / 2)
        heading_spacing_l = math.floor(heading_spacing / 2)
    else:
        heading_spacing_r = heading_spacing / 2
        heading_spacing_l = heading_spacing / 2

    file.write(f"{comment_type}#" + filler * int(heading_spacing_l) + text + filler * int(heading_spacing_r) + "#\n")

def __write_empty_line(file, block_width, comment_type, filler):
    file.write(f"{comment_type}#" + filler * int(block_width - 2) + "#" + "\n")

def __write_full_line(file, block_width, comment_type):
    file.write(f"{comment_type}" + "#" * int(block_width) + "\n")

def write_comment_block(file, text, block_width, block_height, comment_type, filled = False, no_extra_return = False):
    """
    Write a code block to a file with certain text.
    """

    text = " " + text + " "

    if block_width < len(text):
        return
    
    if block_height < 1:
        return

    filler = " " if not filled else "#"

    if block_height == 1:
        __write_heading(file, text, block_width, comment_type, filler)

    elif block_height > 2 and block_height % 2 == 1:
        empty_lines = int((block_height - 3) / 2)

        __write_full_line(file, block_width, comment_type)

        for i in range(empty_lines):
            __write_empty_line(file, block_width, comment_type, filler)
        
        __write_heading(file, text, block_width, comment_type, filler)

        for i in range(empty_lines):
            __write_empty_line(file, block_width, comment_type, filler)

        __write_full_line(file, block_width, comment_type)

    elif block_height > 2 and block_height % 2 == 0:
        empty_lines = (block_height - 3) / 2

        top_empty_lines = math.floor(empty_lines)
        bottom_empty_lines = math.ceil(empty_lines)

        __write_full_line(file, block_width, comment_type)

        for i in range(top_empty_lines):
            __write_empty_line(file, block_width, comment_type, filler)
        
        __write_heading(file, text, block_width, comment_type, filler)

        for i in range(bottom_empty_lines):
            __write_empty_line(file, block_width, comment_type, filler)

        __write_full_line(file, block_width, comment_type)

    if not no_extra_return:
        file.write("\n")
