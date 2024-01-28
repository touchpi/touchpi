from touchpi.appbase.app import App
from PySimpleGUI import (Canvas, VPush, Push, theme_background_color,
                         theme_button_color_background, theme_button_color_text)
from turtle import TurtleScreen, RawTurtle
from datetime import datetime


class AnalogClock(App):
    def __init__(self):
        super().__init__()
        self.turtle_screen = TurtleScreen(self.window['analogclock_canvas'].tk_canvas)
        self.turtle_screen.bgcolor(theme_background_color())
        self.turtle_screen.mode('logo')
        size = 140
        self.second_hand = self.def_hand_shape("second_hand", 2, size * 0.95)
        self.minute_hand = self.def_hand_shape("minute_hand", 4, size * 0.85)
        self.hour_hand = self.def_hand_shape("hour_hand", 8, size * 0.6)
        self.draw_clock_face(size)

    @staticmethod
    def layout():
        layout = [[VPush()]]
        canvas = Canvas(size=(App.get_app_width(), App.get_app_height()), pad=(0, 0), key='analogclock_canvas')
        layout += [[Push(), canvas, Push()]]
        layout += [[VPush()]]
        return layout

    def def_hand_shape(self, name, broad, size):
        self.turtle_screen.register_shape(name, ((0, 0), (broad, size * 0.8), (0, size), (-broad, size * 0.8)))
        a_turtle = RawTurtle(self.turtle_screen)
        a_turtle.color(theme_button_color_text())
        a_turtle.shape(name)
        return a_turtle

    def draw_clock_face(self, radius):
        self.turtle_screen.tracer(False)
        a_turtle = RawTurtle(self.turtle_screen)
        a_turtle.color(theme_button_color_text())
        a_turtle.hideturtle()
        a_turtle.pensize(7)
        for i in range(60):
            a_turtle.penup()
            a_turtle.forward(radius)
            a_turtle.pendown()
            if i % 5 == 0:
                a_turtle.forward(20)
                a_turtle.penup()
                a_turtle.forward(-radius - 20)
                a_turtle.pendown()
            else:
                a_turtle.dot(5)
                a_turtle.penup()
                a_turtle.forward(-radius)
                a_turtle.pendown()
            a_turtle.right(6)
        self.draw_hands()
        a_turtle.pensize(0)
        a_turtle.goto(radius - 2,0)
        a_turtle.begin_fill()
        a_turtle.fillcolor(theme_button_color_background())
        a_turtle.circle(radius - 2, 360)
        a_turtle.end_fill()
        self.turtle_screen.tracer(True)
        return a_turtle

    def draw_hands(self):
        now = datetime.today()
        second_angle = now.second * 6
        minute_angle = (now.minute + (now.second / 60)) * 6
        hour_angle = ((now.hour + (now.minute / 60)) % 12) * 30
        self.second_hand.setheading(second_angle)
        self.minute_hand.setheading(minute_angle)
        self.hour_hand.setheading(hour_angle)

    def update(self, event, values):
        if event == "_pulse_1":
            self.draw_hands()


if __name__ == '__main__':
    app = AnalogClock()
    app.window.write_event_value("_pulse_1", None)
    app.run()
