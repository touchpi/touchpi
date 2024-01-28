from turtle import TurtleScreen, RawTurtle
from PySimpleGUI import Canvas, Window, WIN_CLOSED
# from time import sleep


if __name__ == '__main__':
    a_canvas = Canvas(size=(385, 385), key='canvas')
    layout = [[a_canvas]]
    window = Window('Turtle fun', layout, finalize=True)
    window.bind("<Escape>", "Quit")
    turtle_screen = TurtleScreen(a_canvas.tk_canvas)
    turtle_screen.bgcolor("#64778d")
    # turtle_screen.mode('logo')
    a_turtle = RawTurtle(turtle_screen)
    a_turtle.hideturtle()
    a_turtle.pensize(3)

    turtle_screen.tracer(False)
    a_turtle.up()
    a_turtle.goto(180, 10)  # center circle around origin
    a_turtle.down()
    a_turtle.color('black')
    a_turtle.begin_fill()
    a_turtle.fillcolor("grey")
    a_turtle.setheading(90)
    a_turtle.circle(180, 180)
    a_turtle.left(90)
    a_turtle.forward(360)
    a_turtle.end_fill()
    a_turtle.up()
    a_turtle.goto(0, 50)  # center circle around origin
    a_turtle.down()
    a_turtle.write("to Pasing", font=("Verdana", 14, "bold"), align='center')

    a_turtle.up()
    a_turtle.goto(180, -10)  # center circle around origin
    a_turtle.down()
    a_turtle.color('black')
    a_turtle.begin_fill()
    a_turtle.fillcolor("grey")
    a_turtle.setheading(90)
    a_turtle.circle(180, -180)
    a_turtle.left(90)
    a_turtle.forward(360)
    a_turtle.end_fill()
    a_turtle.up()
    a_turtle.goto(0, -64)  # center circle around origin
    a_turtle.down()
    a_turtle.write("to City", font=("Verdana", 14, "bold"), align='center')
    turtle_screen.tracer(True)

    a_turtle.up()
    a_turtle.goto(0, 10)  # center circle around origin
    a_turtle.down()
    a_turtle.setheading(170)
    a_turtle.up()
    a_turtle.forward(140)
    a_turtle.down()
    a_turtle.color('red')
    a_turtle.write("2", font=("Verdana", 14, "bold"), align='center')

    a_turtle.up()
    a_turtle.goto(0, 10)  # center circle around origin
    a_turtle.down()
    a_turtle.setheading(125)
    a_turtle.up()
    a_turtle.forward(140)
    a_turtle.down()
    a_turtle.color('darkgreen')
    a_turtle.write("9", font=("Verdana", 24, "bold"), align='center')

    a_turtle.up()
    a_turtle.goto(0, 10)  # center circle around origin
    a_turtle.down()
    a_turtle.setheading(60)
    a_turtle.up()
    a_turtle.forward(140)
    a_turtle.down()
    a_turtle.color('green')
    a_turtle.write("14", font=("Verdana", 14, "bold"), align='center')

    a_turtle.up()
    a_turtle.goto(0, 10)  # center circle around origin
    a_turtle.down()
    a_turtle.setheading(10)
    a_turtle.up()
    a_turtle.forward(140)
    a_turtle.down()
    a_turtle.color('green')
    a_turtle.write("19", font=("Verdana", 14, "bold"), align='center')

    a_turtle.up()
    a_turtle.goto(0, -10-14-10)  # center circle around origin
    a_turtle.down()
    a_turtle.setheading(190)
    a_turtle.up()
    a_turtle.forward(140)
    a_turtle.down()
    a_turtle.color('red')
    a_turtle.write("3", font=("Verdana", 14, "bold"), align='center')

    a_turtle.up()
    a_turtle.goto(0, -10-14-10)  # center circle around origin
    a_turtle.down()
    a_turtle.setheading(230)
    a_turtle.up()
    a_turtle.forward(140)
    a_turtle.down()
    a_turtle.color('red')
    a_turtle.write("9", font=("Verdana", 14, "bold"), align='center')

    a_turtle.up()
    a_turtle.goto(0, -10-24-10)  # center circle around origin
    a_turtle.down()
    a_turtle.setheading(300)
    a_turtle.up()
    a_turtle.forward(140)
    a_turtle.down()
    a_turtle.color('darkgreen')
    a_turtle.write("14", font=("Verdana", 24, "bold"), align='center')

    a_turtle.up()
    a_turtle.goto(0, -10-14-10)  # center circle around origin
    a_turtle.down()
    a_turtle.setheading(350)
    a_turtle.up()
    a_turtle.forward(140)
    a_turtle.down()
    a_turtle.color('green')
    a_turtle.write("21", font=("Verdana", 14, "bold"), align='center')

    while True:
        event, values = window.read(200)
        if event in (WIN_CLOSED, 'Quit'):
            break

    window.close()
