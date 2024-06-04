from touchpi.appbase.app import log, settings
from PySimpleGUI import theme_background_color
from turtle import TurtleScreen, RawTurtle


class MvgDraw:
    def __init__(self, app_canvas):
        self.turtle_screen = TurtleScreen(app_canvas)
        self.main_turtle = self.create_turtle()
        self.radius = (min(self.turtle_screen.canvwidth, self.turtle_screen.canvheight) - 30) / 2
        self.center_distance = 10

    def init_screen(self, message="loading...", color='black'):
        self.turtle_screen.clearscreen()
        self.turtle_screen.bgcolor(theme_background_color())
        self.turtle_screen.tracer(False)
        self.main_turtle = self.create_turtle(color=color)
        self.main_turtle.goto(20, 40)
        self.main_turtle.write(message, font=("Verdana", 14, "bold"), align='center')

    def create_turtle(self, color=None, shape_name=None):
        a_turtle = RawTurtle(self.turtle_screen)
        a_turtle.hideturtle()
        if color is None:
            a_turtle.color(theme_background_color())
        else:
            a_turtle.color(color)
        if shape_name is not None:
            a_turtle.shape(shape_name)
        a_turtle.up()
        return a_turtle

    def def_semicircle_shape(self, radius):
        # Just want to try stamping shapes, there are more easy ways to draw the two semicircles. ;-)
        shape_name = 'semicircle'
        turtle_semicircle_shape = self.create_turtle()
        turtle_semicircle_shape.begin_poly()
        turtle_semicircle_shape.circle(radius, 180)
        turtle_semicircle_shape.end_poly()
        poly = turtle_semicircle_shape.get_poly()
        self.turtle_screen.register_shape(shape_name, poly)
        return shape_name

    def draw_semicircle_shapes(self):
        # Just want to try stamping shapes, there are more easy ways to draw the two semicircles. ;-)
        self.main_turtle.shape('semicircle')
        self.main_turtle.color(settings.mvg_inner_circle_color)
        self.main_turtle.goto(-self.radius, -self.center_distance)
        self.main_turtle.stamp()
        self.main_turtle.setheading(180)
        self.main_turtle.goto(self.radius, self.center_distance)
        self.main_turtle.stamp()

    def draw_departure_times(self, departures):
        # departures = [[ 3, 7 , 15 , 21], [12, 17 , 32, 49]]  # sample data
        self.main_turtle.shape('classic')
        self.main_turtle.goto(0, self.center_distance * 2)
        self.main_turtle.color(theme_background_color())
        self.main_turtle.write(settings.mvg_direction_label1, font=("Verdana", 14, "bold"), align='center')
        n_min = min(departures[0])
        n_max = max(departures[0])
        self.main_turtle.color(settings.mvg_upper_text_color)
        for index, n in enumerate(departures[0]):
            heading = 180 - round(((n - n_min) / (n_max - n_min) * 160) + 10)
            self.main_turtle.goto(0, self.center_distance)
            self.main_turtle.setheading(heading)
            self.main_turtle.forward(self.radius - 40)
            self.main_turtle.write(str(n), font=("Verdana", 24 - (index * 3), "bold"), align='center')

        self.main_turtle.goto(0, -self.center_distance * 4)
        self.main_turtle.color(theme_background_color())
        self.main_turtle.write(settings.mvg_direction_label2, font=("Verdana", 14, "bold"), align='center')
        n_min = min(departures[1])
        n_max = max(departures[1])
        self.main_turtle.color(settings.mvg_lower_text_color)
        for index, n in enumerate(departures[1]):
            heading = 180 + round(((n - n_min) / (n_max - n_min) * 160) + 10)
            self.main_turtle.goto(0, -(self.center_distance + 40))
            self.main_turtle.setheading(heading)
            self.main_turtle.forward(self.radius - 40)
            self.main_turtle.write(str(n), font=("Verdana", 24 - (index * 3), "bold"), align='center')

    def draw(self, departures):
        log.debug("Drawing departure times.")
        self.main_turtle.clear()
        self.main_turtle = self.create_turtle(shape_name=self.def_semicircle_shape(self.radius))
        self.draw_semicircle_shapes()
        self.draw_departure_times(departures)
