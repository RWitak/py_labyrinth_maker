# La<sup>PY</sup>rinth (aka _py_labyrinth_maker_)
_Randomly create labyrinths by turtle._

Works by sending a [turtle](https://en.wikipedia.org/wiki/Turtle_graphics) (invisible) on its way around an open field. It takes single steps by randomly choosing between going forward, to the left, or to the right. 
The turtle remembers its path; whenever it tries to cross it, it builds a separating wall instead and tries a different direction. 
As soon as all directions from a single point have been walked to their end, the turtle backtracks in single steps until it finds an untaken path, on which it continues.

In this way, a whole labyrinth is built, making sure that every point inside it can be reached in exactly one (and only one!) way.
