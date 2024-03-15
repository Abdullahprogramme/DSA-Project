import numpy as np 
from PIL import Image, ImageDraw

MAX_DEPTH = 8
DETAIL_THRESHOLD = 5# 13
SIZE_MULTIPLIER = 1

def Get_Detail(histogram):
    '''
    Description: 
        This function calculates the detail intensity of the image by taking the weighted average of the histogram of the image.
    
    Args:
        histogram: list of pixel values.
    
    Returns:
        detail_intensity: float value of the detail intensity.
    '''
    red_detail = Weighted_Average(histogram[:256]) # taking values from 0 to 255 for red colour channel
    green_detail = Weighted_Average(histogram[256:512]) # taking values from 256 to 511 for green colour channel
    blue_detail = weighted_Average(histogram[512:768]) # taking values from 512 to 767 for blue colour channel

    detail_intensity = red_detail * 0.2989 + green_detail * 0.5870 + blue_detail * 0.1140  # weighted average of the three colour channels for eye sensitivity

    return detail_intensity

def Quadrant(image, bbox, depth):
    quadrant = {} # dictionary to store the details of the quadrant
    quadrant['bbox'] = bbox # bounding box of the quadrant
    quadrant['depth'] = depth # depth of the quadrant in the tree
    quadrant['children'] = None # children of the quadrant
    quadrant['leaf'] = False # flag to check if the quadrant is a leaf node

    # crop image to quadrant size
    image = image.crop(bbox) # cropping the image to the size of the quadrant using the bounding box
    hist = image.histogram() # getting the histogram of the image which contains the pixel values 

    quadrant['detail'] = Get_Detail(hist) # calculating the detail intensity of the quadrant
    quadrant['colour'] = Average_Colour(image) # calculating the average colour of the quadrant
