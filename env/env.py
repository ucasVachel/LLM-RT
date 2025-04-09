class Env:
    def __init__(self, x_range, y_range, cross_barriers, avoid_barriers):
        self.x_range = x_range  # size of background
        self.y_range = y_range
        self.cross_barriers = cross_barriers
        self.avoid_barriers = avoid_barriers

    def boundary_map(self):
        """
        Initialize obstacles' positions
        :return: map of obstacles
        """

        x = self.x_range
        y = self.y_range
        obs = set()

        for i in range(x):
            obs.add((i, 0))
        for i in range(x):
            obs.add((i, y - 1))

        for i in range(y):
            obs.add((0, i))
        for i in range(y):
            obs.add((x - 1, i))

        return obs