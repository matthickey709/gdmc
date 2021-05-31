class Structure:
    def __init__(self, minx, minz, xlength, zlength, direction):
        self.r = [minx, minz, xlength, zlength]
        # self.name = name
        self.direction = direction

    def overlap(self, otherStruct, buffer):

        extendedStruct = Structure(self.r[0] -  buffer, self.r[1] - buffer, self.r[2] + 2*buffer, self.r[3] + 2*buffer, self.direction)
        if (extendedStruct.r[0] >= otherStruct.r[0] + otherStruct.r[2]) or (extendedStruct.r[0] + extendedStruct.r[2] <= otherStruct.r[0]) or (
                extendedStruct.r[1] + extendedStruct.r[3] <= otherStruct.r[1]) or (extendedStruct.r[1] >= otherStruct.r[1] + otherStruct.r[3]):
            return False
        else:
            return True

    def isInBuildArea(self, build_area):
        # FIXME: With the latest changes to north/south facing buildings this check isn't adequate. Need to get genx/z
        # Quick length check
        if self.r[2] >= build_area[2] or self.r[3] >= build_area[3]:
            # plot is too long/wide
            return False
        bottom_left_in = build_area[0] <= self.r[0] < build_area[0] + build_area[2] and build_area[1] <= self.r[1] < build_area[1] + build_area[3]
        top_right = self.r[0] + self.r[2], self.r[1] + self.r[3]
        top_right_in = build_area[0] <= top_right[0] < build_area[0] + build_area[2] and build_area[1] <= top_right[1] < build_area[1] + build_area[3]

        return bottom_left_in and top_right_in
