import random
import sys
import tkinter.simpledialog
from tkinter import messagebox
import turtle as trtl

waypoints = set()

LEFT = -200
TOP = -200
RIGHT = 200
BOTTOM = 200

STEP = 10


def within_bounds(x, y):
    return (LEFT <= x <= RIGHT
            and TOP <= y <= BOTTOM)


def free_field(x: float, y: float) -> bool:
    # FIXME: allows to cross outer bounds by 1 step

    x = round(x)
    y = round(y)
    if not (LEFT <= x <= RIGHT and TOP <= y <= BOTTOM):
        return False

    for p_x, p_y in waypoints:
        if x == p_x and y == p_y:
            return False
    return True


def spawn_turtle(x, y, heading=0):
    t = trtl.Turtle(visible=False)
    speed_init = t.speed()
    t.speed(0)
    t.up()
    t.setpos(x, y)
    t.setheading(heading)
    t.speed(speed_init)
    t.down()
    return t


def move(t: trtl.Turtle):
    # TODO: Find better way to navigate with precision and awareness.
    turns = [-90, 0, 90]
    random.shuffle(turns)

    for turn in turns:
        waypoints.add((round(t.xcor()), round(t.ycor())))
        t.right(turn)
        t.forward(STEP)

        if free_field(*t.pos()):
            try:
                move(t)
            except RecursionError:
                if messagebox.askyesno("Recursion limit reached",
                                       f"Maximum recursion depth reached: {sys.getrecursionlimit()}. "
                                       f"Double limit to continue?"):
                    sys.setrecursionlimit(sys.getrecursionlimit() * 2)
                else:
                    trtl.done()

        elif t.pos()[0] >= (LEFT * STEP):
            wall = spawn_turtle(*t.pos(), t.heading())
            wall.hideturtle()
            wall.speed(0)
            wall.color("gray")
            wall.up()
            wall.bk(STEP * .5)
            wall.down()
            wall.right(90)
            wall.fd(STEP * .5)
            wall.bk(STEP)
            t.undo()
            t.undo()
    t.undo()
    t.undo()


class WallException(Exception):
    pass


def increase_recursion_limit():
    old = sys.getrecursionlimit()
    sys.setrecursionlimit(old * 2)


if __name__ == '__main__':
    # FIXME: arbitrary limit
    sys.setrecursionlimit(10000)
    root = tkinter.Tk()
    root.withdraw()

    trtl.delay(0)
    turtle = trtl.Turtle()
    turtle.speed(3)
    turtle.shape("turtle")
    turtle.hideturtle()
    turtle.up()
    turtle.setundobuffer(10000000)
    move(turtle)
    trtl.done()
