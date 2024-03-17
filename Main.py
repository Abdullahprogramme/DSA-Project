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

def Split_Quadrant(quadrant, image):
    '''
    description:
        This function splits the input quadrant into 4 new quadrants.
    Args:
        quadrant: dictionary to store the details of the quadrant
        image: input image
    '''
    left, top, right, bottom = quadrant['bbox'] # getting the bounding box of the quadrant
    middle_x = left + (right - left) / 2 # getting the middle x coordinate of the quadrant
    middle_y = top + (bottom - top) / 2 # getting the middle y coordinate of the quadrant

    # split root quadrant into 4 new quadrants
    upper_left = Quadrant(image, (left, top, middle_x, middle_y), quadrant['depth']+1) # creating the upper left quadrant
    upper_right = Quadrant(image, (middle_x, top, right, middle_y), quadrant['depth']+1) # creating the upper right quadrant
    lower_left = Quadrant(image, (left, middle_y, middle_x, bottom), quadrant['depth']+1) # creating the lower left quadrant
    lower_right = Quadrant(image, (middle_x, middle_y, right, bottom), quadrant['depth']+1) # creating the lower right quadrant

    quadrant['children'] = [upper_left, upper_right, lower_left, lower_right] # storing the children of the quadrant in the quadrant dictionary

def Quad_Tree(image):
    '''
    description:
        This function creates a quad tree of the input image.
    Args:
        image: input image
    '''
    quad_tree = {}
    quad_tree['width'], quad_tree['height'] = image.size # getting the width and height of the image
    quad_tree['max_depth'] = 0
    
    Start(quad_tree, image) # starting the compression of the image by creating a quad tree of the image

def Start(quad_tree, image):
    '''
    description:
        This function starts the compression of the image by creating a quad tree of the image.
    Args:
        image: input image
    '''
    root = Quadrant(image, image.getbbox(), 0) # creating the root quadrant of the image
    Build(quad_tree, root, image) # building the quad tree of the image

def Build(quad_tree, root, image):
    '''
    description:
        This function builds the quad tree of the input image.
    Args:
        quad_tree: dictionary to store the details of the quad tree
        root: dictionary to store the details of the root quadrant
        image: input image
    '''
    if root['depth'] > MAX_DEPTH or root['detail'] < DETAIL_THRESHOLD: # checking if the depth of the quadrant is greater than the maximum depth or the detail intensity of the quadrant is less than the detail threshold
        if root['depth'] > quad_tree['max_depth']: 
            quad_tree['max_depth'] = root['depth']

        root['leaf'] = True # assigning the quadrant to a leaf node and stopping the recursion
        return
    
    Split_Quadrant(root, image) # splitting the quadrant into 4 new quadrants

    for child in root['children']: # iterating through the children of the quadrant
        Build(quad_tree, child, image) # building the quad tree of the child
