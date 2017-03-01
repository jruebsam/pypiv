class GridSpec(object):
    """
    Class for grid specifications.

    This class saves and caluclates the grid specifications.
    """

    def __init__(self, frame_shape, frame_strides, window_size, search_size, distance):
        """
        Initialization of the shapes and strides.

        Setting the values according to parameters.
        If the window_size and search_size are not the same a padding for the smaler one is added.

        :param frame_shape: shape of the initial image
        :param frame_strides: strides of the initial image
        :param window_size: size of the interogation window
        :param search_size: size of the search window
        :param distance: distance between interogation window beginnings
        """
        self.frame_shape    = frame_shape
        self.frame_strides  = frame_strides
        self.window_size = window_size
        self.search_size = search_size
        self.distance = distance
        self.pad = max([0, (search_size - window_size)/2])

    def equal_to(self, grid_spec):
        """
        Comparrison operator for class.

        Two GridSpecs are equal if the window_size, the search_size and distance are equal.

        :param GridSpec grid_spec: grid spec to compare with
        :returns: True or False
        """
        cond1 = grid_spec.window_size  == self.window_size
        cond2 = grid_spec.search_size  == self.search_size
        cond3 = grid_spec.distance     == self.distance
        if cond1 & cond2 & cond3:
            return True
        else:
            return False

    def get_grid_shape(self):
        """
        Getter function for the shape of the grid.

        The returned value is the shape of the grid calculated from the arangement of the interogation windows.

        :returns: grid shape in x and y direction as tupel
        """
        lx, ly = self.frame_shape
        return ((lx - self.window_size)//self.distance+1,
                (ly - self.window_size)//self.distance+1)

    def get_interogation_grid_shape(self):
        """
        Getter function for the shape of the interogation window.

        :returns: shape of the interogation window
        """
        shape = self.get_grid_shape()
        return shape + 2*(self.window_size,)

    def get_search_grid_shape(self):
        """
        Getter function for the shape of the search window.

        :returns: shape of the search window
        """
        shape = self.get_grid_shape()
        return shape + 2*(self.search_size,)

    def get_interogation_grid_strides(self):
        """
        Getter function for the strides of the interogation window.

        :returns: strides of the interogation window
        """
        sx, sy = self.frame_strides
        return (sx*self.distance, sy*self.distance, sx, sy)

    def get_search_grid_strides(self):
        """
        Getter function for the strides of the search window.

        :returns: strides of the search window
        """
        sx, sy = self.frame_strides
        sx = sx + 2*self.pad*sy
        return (sx*self.distance, sy*self.distance, sx, sy)

