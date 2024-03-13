import numpy as np 
from PIL import Image, ImageDraw

MAX_DEPTH = 8
DETAIL_THRESHOLD = 5# 13
SIZE_MULT = 1

def Quadrant(image, bbox, depth):
    quadrant = {}
    quadrant['bbox'] = bbox
    quadrant['depth'] = depth
    quadrant['children'] = None
    quadrant['leaf'] = False

    # crop image to quadrant size
    image = image.crop(bbox)
    hist = image.histogram()

    quadrant['detail'] = Get_Detail(hist)
    quadrant['colour'] = Average_Colour(image)
