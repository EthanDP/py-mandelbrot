#!/usr/bin/python3
import tkinter as tk
import pygame as pg
import sys
import calculate

def get_settings():
    """
    Generates a GUI to collect basic generation settings.
    Sets default values for any entries that are not filled.
    """

    menu = tk.Tk()
    tk_rgb = "#%02x%02x%02x" % (128, 192, 200)
    menu.title('Mandelbrot Settings')
    menu.configure(background=tk_rgb)

    def start_gen(gen_settings, status_label):
        arguments = [] # Argument Order: width, height, minx, maxx, miny, maxy
        defaults = (500, 500, -2.0, 1.0, -1.5, 1.5)
        for i, setting in enumerate(gen_settings):
            value = setting.get()
            try:
                value = float(setting.get())
                print(value)
                arguments.append(value)
            except ValueError:
                print("Invalid input, must be a number.  Supplying default value.")
                arguments.append(defaults[i])
        status_label.configure(text='Calculating...')
        menu.update_idletasks()
        calculate.find_points(*arguments)
        menu.destroy()
        pg_window(int(arguments[0]), int(arguments[1]))

    width_label = tk.Label(menu, text='Window Width', background=tk_rgb)
    width_field = tk.Entry(menu)
    height_label = tk.Label(menu, text='Window Height', background=tk_rgb)
    height_field = tk.Entry(menu)
    minx_label = tk.Label(menu, text='Min X', background=tk_rgb)
    minx_field = tk.Entry(menu)
    maxx_label = tk.Label(menu, text='Max X', background=tk_rgb)
    maxx_field = tk.Entry(menu)
    miny_label = tk.Label(menu, text='Min Y', background=tk_rgb)
    miny_field = tk.Entry(menu)
    maxy_label = tk.Label(menu, text='Max Y', background=tk_rgb)
    maxy_field = tk.Entry(menu)

    entries = [width_field, height_field, minx_field, maxx_field,
        miny_field, maxy_field]

    generate_status = tk.Label(menu, text='Waiting...', background=tk_rgb)
    generate_button = tk.Button(menu, text='Generate Set', 
                                command=lambda: start_gen(entries, generate_status))

    # TODO: Find less stupid way to do this
    width_label.grid(row=1, column=0)
    width_field.grid(row=1, column=1, columnspan=2)
    height_label.grid(row=2, column=0)
    height_field.grid(row=2, column=1, columnspan=2)
    minx_label.grid(row=3, column=0)
    minx_field.grid(row=3, column=1, columnspan=2)
    maxx_label.grid(row=4, column=0)
    maxx_field.grid(row=4, column=1, columnspan=2)
    miny_label.grid(row=5, column=0)
    miny_field.grid(row=5, column=1, columnspan=2)
    maxy_label.grid(row=6, column=0)
    maxy_field.grid(row=6, column=1, columnspan=2)
    generate_status.grid(row=7, column=0)
    generate_button.grid(row=7, column=1)

    menu.mainloop()

def zoom(mouse_x, mouse_y, width, height, zoom_x, zoom_y):
    # TODO: FIX ZOOM WHEN RECT OFF-SCREEN
    start_x = mouse_x - zoom_x
    end_x = mouse_x + zoom_x
    start_y = mouse_y - zoom_y
    end_y = mouse_y + zoom_y
    x = 0
    y = 0

    min_x = 0
    max_x = 0
    min_y = 0
    max_y = 0

    with open('results.txt', 'r') as f:
        for line in f:
            if x % width == 0:
                x = 0
                y += 1

            if x == start_x and y == start_y:
                point = line.split(',') 
                print(point)
                min_x = float(point[1]) # TODO: Something is sketchy here
                min_y = float(point[2])
            elif x == end_x and y == end_y:
                point = line.split(',')
                max_x = float(point[1])
                max_y = float(point[2])

            x += 1

    calculate.find_points(width, height, min_x, max_x, min_y, max_y)

def pg_window(width, height):
    pg.init()
    
    fill_color = 255, 255, 255 # White
    window = pg.display.set_mode((width, height))

    set_img = pg.image.load('mandelbrot.png')
    zoom_x = int(width * .15)
    zoom_y = int(height * .15)

    while True:
        window.fill(fill_color)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                zoom(*pg.mouse.get_pos(), width, height, zoom_x, zoom_y)
                pg.quit()
                pg_window(width, height)
                
        zoom_rect = pg.Rect((0,0), (zoom_x * 2 + 1, zoom_y * 2 + 1))
        # zoom variables are the distance from mouse position to edge of rect
        # Multiplying each variable by 2 and adding 1 gives the rect its size
        zoom_rect.center = pg.mouse.get_pos()
        
        window.fill(fill_color)
        window.blit(set_img, (0, 0))
        pg.draw.rect(window, (30, 30, 30), zoom_rect, 5)
        pg.display.flip()


if __name__ == "__main__":
    get_settings()