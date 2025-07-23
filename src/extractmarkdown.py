import os


def extract_title(mardown):
    lines = mardown.splitlines()
    for line in lines:
        if line.startswith('# '):
            return line
    return ""

