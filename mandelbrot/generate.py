from PIL import Image
from colors import color_codes
from sys import exc_info
# TODO: Floor up for row length

points = []

def generate_image(width, height):
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
                    pic[x,y] = color_codes[int(point)]
                    x += 1
                except:
                    x += 1
            else:
                y += 1
                x = 0
                try:
                    pic[x,y] = color_codes[int(point)]
                    x += 1
                except:
                    x += 1
        img.save('mandelbrot.png')

if __name__ == "__main__":
    generate_image()