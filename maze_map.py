LEFT = -200
TOP = -200
RIGHT = 200
BOTTOM = 200

STEP = 10


class MazeMap:
    waypoints: set[tuple[int, int]]

    def __init__(self):
        self.waypoints = set()

    def free_field(self, x: float, y: float) -> bool:
        x = round(x)
        y = round(y)
        if not (LEFT < x < RIGHT and TOP < y < BOTTOM):
            return False

        for p_x, p_y in self.waypoints:
            if x == p_x and y == p_y:
                return False
        return True

    def add(self, x: int, y: int):
        self.waypoints.add((x, y))
