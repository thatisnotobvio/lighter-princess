import random
from math import sin, cos, pi, log
from tkinter import *

CANVAS_WIDTH = 640
CANVAS_HEIGHT = 480
CANVAS_CENTER_X = CANVAS_WIDTH / 2
CANVAS_CENTER_Y = CANVAS_HEIGHT / 2
IMAGE_ENLARGE = 11
HEART_COLOR = "#FF4D8D"

def heart_function( t, shrink_ratio: float = IMAGE_ENLARGE):
    """
    Heart function generator
    :param shrink_ratio: Magnification ratio
    :param t: Parameter
    :return: Coordinates
    """
    # Basic Function
    x = 16 * (sin(t) ** 3)
    y = -(16 * cos(t) - 4 * cos(2 * t) - 2 * cos(3 * t) - cos(3 * t)) #end wala cos is for V width

    # Zoom in
    x *= shrink_ratio
    y *= shrink_ratio

    # Shift to center
    x += CANVAS_CENTER_X
    y += CANVAS_CENTER_Y

    return int(x), int(y)

def scatter_inside(x, y, beta=2.2):
    """
    Randomly internal diffusion
    :param x: Original x
    :param y: Original y
    :param beta: Intensity
    :return: New coordinates
    """
    ratio_x = - beta * log(random.random())
    ratio_y = - beta * log(random.random())

    dx = ratio_x * (x - CANVAS_CENTER_X)
    dy = ratio_y * (y - CANVAS_CENTER_Y)

    return x - dx, y - dy

def shrink(x, y, ratio):
    """
    Shaking
    :param x: Original x
    :param y: Original y
    :param ratio: Ratio
    :return: New coordinates
    """
    force = -1 / (((x - CANVAS_CENTER_X) ** 2 + (y - CANVAS_CENTER_Y) ** 2) ** 0.6)
    dx = ratio * force * (x - CANVAS_CENTER_X)
    dy = ratio * force * (y - CANVAS_CENTER_Y)

    return x - dx, y - dy

def curve(p):
    """
    Custom curve function to adjust the jumping period
    :param p: Parameter
    :return: Sine
    """
    return 2 * (2 * sin(4 * p)) / (2 * pi)

class Heart:
    """
    Heart class
    """

    def __init__(self, generate_frame=20):
        self._points = set()  # original heart coordinate set
        self._edge_diffusion_points = set()  # Edge diffusion effect point coordinate set
        self._center_diffusion_points = set()  # Center diffusion effect point coordinate set
        self.all_points = {}  # dynamic point coordinates per frame
        self.build(2000)
        self.random_halo = 4000

        self.generate_frame = generate_frame
        for frame in range(generate_frame):
            self.calc(frame)

    def build(self, number):
        # Heart
        for _ in range(number):
            t = random.random() * 2 * pi  # Gap in heart caused by random selection
            x, y = heart_function(t)
            self._points.add((x, y))

        # Spreading within heart
        for _x, _y in list(self._points):
            for _ in range(3):
                x, y = scatter_inside(_x, _y, 0.10)
                self._edge_diffusion_points.add((x, y))

        # Spreading again within heart
        point_list = list(self._points)
        for _ in range(3000):
            x, y = random.choice(point_list)
            x, y = scatter_inside(x, y, 0.20)
            self._center_diffusion_points.add((x, y))

    def calc_position(self, x, y, ratio):
        # Adjust scaling ratio
        force = 1 / (((x - CANVAS_CENTER_X) ** 2 + (y - CANVAS_CENTER_Y) ** 2) ** 0.545)  # magic parameter

        dx = ratio * force * (x - CANVAS_CENTER_X) + random.randint(-1, 1)
        dy = ratio * force * (y - CANVAS_CENTER_Y) + random.randint(-1, 1)

        return x - dx, y - dy

    def calc(self, generate_frame):
        ratio = 20 * curve(generate_frame / 15 * pi)  # scaling ratio for a smooth period
        halo_radius = int(4 + 6 * (1 + curve(generate_frame / 15 * pi)))
        halo_number = int(4000 + 5000 * abs(curve(generate_frame / 15 * pi) ** 2))

        all_points = []

        # Halo
        heart_halo_point = set()  # set of coordinates of halo points
        for _ in range(halo_number):
            t = random.uniform(0, 2 * pi)  # Gap in heart caused by random non-randomization
            x, y = heart_function(t, shrink_ratio=11.5)  # Magic parameters
            x, y = shrink(x, y, halo_radius)
            if (x, y) not in heart_halo_point:
                # Process new points
                heart_halo_point.add((x, y))
                x += random.randint(-14, 14)
                y += random.randint(-14, 14)
                size = random.choice((1, 2, 2))
                all_points.append((x, y, size))

        # Outline
        for x, y in self._points:
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 2)
            all_points.append((x, y, size))

        for x, y in self._edge_diffusion_points:
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 2)
            all_points.append((x, y, size))

        for x, y in self._center_diffusion_points:
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 2)
            all_points.append((x, y, size))

        self.all_points[generate_frame] = all_points

    def render(self, render_canvas, render_frame):
        for x, y, size in self.all_points[render_frame % self.generate_frame]:
            render_canvas.create_rectangle(x, y, x + size, y + size, width=0, fill=HEART_COLOR)


def draw(main, render_canvas, render_heart, render_frame=0):
    render_canvas.delete('all')
    render_heart.render(render_canvas, render_frame)
    main.after(50, draw, main, render_canvas, render_heart, render_frame + 1)  # Changed from 160 to 50 for smoother animation


if __name__ == '__main__':
    main = Tk()
    canvas = Canvas(main, bg='#05070F', width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
    canvas.pack()
    heart = Heart()
    draw(main, canvas, heart)
    main.mainloop()
