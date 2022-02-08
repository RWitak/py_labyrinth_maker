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


class Scout:
    def __init__(self, pos: tuple[float, float], heading):
        t = trtl.Turtle(visible=False)
        speed_init = t.speed()
        t.speed(0)
        t.up()
        t.setpos(*pos)
        t.setheading(heading)
        t.speed(speed_init)
        t.color("grey")

        self.scout = t

    def way_free(self) -> bool:
        self.scout.forward(STEP)
        free = free_field(*self.scout.pos())
        self.scout.undo()
        return free

    def make_wall(self, return_home=True) -> None:
        # get into position
        self.scout.fd(STEP * .5)
        self.scout.right(90)
        self.scout.fd(STEP * .5)

        # draw wall
        self.scout.down()
        self.scout.bk(STEP)

        if return_home:
            # return to origin
            for _ in range(4):
                self.scout.undo()


def free_field(x: float, y: float) -> bool:
    x = round(x)
    y = round(y)
    if not (LEFT < x < RIGHT and TOP < y < BOTTOM):
        return False

    for p_x, p_y in waypoints:
        if x == p_x and y == p_y:
            return False
    return True


def move(t: trtl.Turtle) -> None:
    # TODO: Find better way to navigate with precision and awareness.

    t.fd(STEP)
    waypoints.add((round(t.xcor()), round(t.ycor())))

    turns = [-90, 0, 90]
    random.shuffle(turns)

    for turn in turns:
        t.right(turn)
        scout = Scout(t.pos(), t.heading())

        if scout.way_free():
            try:
                move(t)
            except RecursionError:
                if messagebox.askyesno("Recursion limit reached",
                                       f"Maximum recursion depth reached: {sys.getrecursionlimit()}. "
                                       f"Double limit to continue?"):
                    sys.setrecursionlimit(sys.getrecursionlimit() * 2)
                else:
                    trtl.done()

        else:
            scout.make_wall(return_home=False)
            del scout
            t.undo()

    # backtrack
    t.undo()
    t.undo()


if __name__ == '__main__':
    # FIXME: arbitrary limit
    sys.setrecursionlimit(10000)
    root = tkinter.Tk()
    root.withdraw()

    trtl.delay(0)
    trtl.listen()
    trtl.onkey(trtl.bye, "space")
    trtl.onkey(trtl.bye, "Escape")

    turtle = trtl.Turtle()
    turtle.speed(0)
    turtle.color("lightgrey")
    # turtle.shape("turtle")
    turtle.hideturtle()
    # turtle.up()
    turtle.setundobuffer(10000000)

    try:
        move(turtle)
        trtl.done()
    except trtl.Terminator:
        pass
