from PIL import Image
import PIL
import sys
import PIL.Image
import PIL.ImageDraw
import pyocr
import pyocr.builders
import numpy as np
from matplotlib import pylab as plt

# OCR tool
tools = pyocr.get_available_tools()
if len(tools) == 0:
    print("No OCR tool found")
    sys.exit(1)

# The tools are returned in the recommended order of usage
tool = tools[0]
print("Will use tool '%s'" % (tool.get_name()))
# Ex: Will use tool 'libtesseract'

def scan_txt(img,lang):
    txt = tool.image_to_string(
        img,
        lang=lang,
        builder=pyocr.builders.TextBuilder(tesseract_layout=6)
    )
    return txt
