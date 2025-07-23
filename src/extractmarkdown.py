import os


def extract_title(mardown):
    lines = mardown.splitlines()
    for line in lines:
        if line.startswith('# '):
            return line
    raise Exception("No title found in the markdown file.")

