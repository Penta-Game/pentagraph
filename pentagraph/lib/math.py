from math import sqrt


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Math:
    k = 3
    l = 6
    PHI = (sqrt(5) + 1) / 2  # alias golden
    # Distances based on s
    j = (9 - (2 * sqrt(5))) / sqrt(5)
    s = 1
    c = sqrt(5)

    def __init__(self):
        """Math provides constants and relative values for a pentagame field"""
        self.L = self.c + 12 + self.j
        self.K = (2 * self.j) + 6
        self.d = 2 * (self.c + 12 + self.j) + (2 * self.j + 6)
        self.r = (2 / 5) * sqrt(1570 + (698 * sqrt(5)))
        self.R = self.r + self.c
        self.linewidth = 0.1 / self.R
        self.inner_r = ((self.k + self.j) * 2 * (1 + sqrt(5))) / sqrt(2 * (5 + sqrt(5)))
        return
