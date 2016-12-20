class GridSpec(object):
    def __init__(self, frame_shape, frame_strides, window_size, search_size, distance):
        self.frame_shape    = frame_shape
        self.frame_strides  = frame_strides
        self.window_size = window_size
        self.search_size = search_size
        self.distance = distance
        self.pad = max([0, (search_size - window_size)/2])

    def equal_to(self, grid_spec):
        cond1 = grid_spec.window_size  == self.window_size
        cond2 = grid_spec.search_size  == self.search_size
        cond3 = grid_spec.distance     == self.distance
        if cond1 & cond2 & cond3:
            return True
        else:
            return False

    def get_grid_shape(self):
        lx, ly = self.frame_shape
        return ((lx - self.window_size)//self.distance+1,
                (ly - self.window_size)//self.distance+1)

    def get_interogation_grid_shape(self):
        shape = self.get_grid_shape()
        return shape + 2*(self.window_size,)

    def get_search_grid_shape(self):
        shape = self.get_grid_shape()
        return shape + 2*(self.search_size,)

    def get_interogation_grid_strides(self):
        sx, sy = self.frame_strides
        return (sx*self.distance, sy*self.distance, sx, sy)

    def get_search_grid_strides(self):
        sx, sy = self.frame_strides
        sx = sx + 2*self.pad*sy
        return (sx*self.distance, sy*self.distance, sx, sy)

