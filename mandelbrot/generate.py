from PIL import Image
import colors
import user_schemes
import sys

points = []
color_code = "Random"
color_scheme = None # The actual dict or dict reference with RGB color codes

def generate_image(width, height):
    """
    Generates an image using the points stored in results.txt and
    color codes it based on the iteration value of each point.

    Parameters:
    width, height: The requested width and height of the image
    """

    global color_code
    global color_scheme
    if color_code == "True Random":
        color_scheme = colors.random_colors()
    elif not color_scheme:
        if color_code == "Random":
            color_scheme = colors.random_colors()
        elif color_code == "Purple Pop":
            color_scheme = colors.purple_rainbow
        elif color_code == "Fractal Flames":
            color_scheme = colors.fractal_flames
        else:
            for var in dir(user_schemes): #TODO: Fix
                if color_code == var:
                    dict_access = f'global color_scheme; color_scheme = user_schemes.{var}'
                    exec(dict_access)
                    break
            else:
                print("Invalid color code entry, closing program.")
                sys.exit()


    with open('results.txt', 'r') as f:
        img = Image.new('RGB', (width, height), color='white')
        pic = img.load()
        points = []
        for line in f:
            iterations = line.split(',')
            points.append(iterations[0])
        x = 0
        y = 0
        for point in points:
            if x < width:
                try:
                    pic[x,y] = color_scheme[int(point)]
                    # Assigns each point to a color value stored in the colors.py 
                    x += 1
                except:
                    x += 1
            else:
                y += 1
                x = 0
                try:
                    pic[x,y] = color_scheme[int(point)]
                    x += 1
                except:
                    x += 1

        img.resize((int(width/2), int(height/2)), resample=Image.ANTIALIAS)
        
        img.save('mandelbrot.png')