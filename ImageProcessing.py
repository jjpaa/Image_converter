from PIL import Image
import glob
import os

# Color filtter function
def filtterFunc(r, g, b):

    # List of colors (16)
    color_list = [
    [255, 255, 255],
    [255, 255, 0],
    [255, 102, 0],
    [221, 0, 0],
    [255, 0, 153],
    [51, 0, 153],
    [0, 0, 204],
    [0, 153, 255],
    [0, 170, 0],
    [0, 102, 0],
    [102, 51, 0],
    [153, 102, 51],
    [187, 187, 187],
    [136, 136, 136],
    [68, 68, 68],
    [0, 0, 0]
    ]

    ######### Color transformation. Finds closest color from the list by using following calculation.

    # Color difference "color_diff" is calculated for each color of the list
    # color_diff is calculated by using sum of r g b difference between orginal picture color and current color from the list
    # If color_diff between current color of the list is smaller than any color before, current color becomes new most closest color.
    # Chancing colors won't work with color green properly using this solution
        # Probably because green is one of the primary colors and our color palette includes a lot of grey colors which reach small color difference.
        # A slight increase to any ( just one) primary color (r,g,b) makes picture turn from grey to colorfull for naked eye, but for this algorithm change is very subtle
    # For this reason green color is handled before other colors.

    color_diff = 1000 # Color difference # "1000" is just initial value that will be overwriten

    if g > r * 1.2  and g > b * 1.2: # check if green is dominant color in pixel                            # Special handling for green color
        if g > 100: # Check if color is bright green, or dark green
            new_r, new_g, new_b = color_list[8][0], color_list[8][1], color_list[8][2]
        else:
            new_r, new_g, new_b = color_list[9][0], color_list[9][1], color_list[9][2]
    else:                                                                                                   # Rest of the colors
        for i, item in enumerate(color_list):
            if color_diff > abs(color_list[i][0] - r) + abs(color_list[i][1] - g) + abs(color_list[i][2] - b):
                color_diff = abs(color_list[i][0] - r) + abs(color_list[i][1] - g) + abs(color_list[i][2] - b)
                new_r, new_g, new_b = color_list[i][0], color_list[i][1], color_list[i][2]

    return new_r, new_g, new_b
# End of color filter

cwd = os.getcwd() # get current path
temp = 0

for filepath in glob.iglob(cwd + "\\dataset" + "\\*.jpg"):
    temp = temp + 1
    # Loading the image and processing
    image = Image.open(filepath)
    Image2 = image.resize((128,128))
    newImage = Image2.convert('RGB') # Caused errors without converting to RGB
    pixels = newImage.load()
    # Program repeats this process for each pixel in the picture
    for i in range(newImage.size[0]):    # for every col:
        for j in range(newImage.size[1]):    # For every row
            r, g, b = newImage.getpixel((i,j))       
            r, g, b = filtterFunc(r, g, b)  # call for color filtter
            pixels[i,j] = (r, g, b) # insert new colors
            
        save_path = str(cwd) + "\\processed"
        fileName = str(temp) + ".png"
        completeName = os.path.join(save_path, fileName) # os.path.join removes errors while saving into folder
        newImage.save(completeName)