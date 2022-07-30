import numpy as np
import utility
from typing import List

class Point:
    def __init__(self, x, y, z, id, normal=None):
        self.z = np.float32(z)
        self.y = np.float32(y)
        self.x = np.float32(x)
        self.cell_code = None
        self.normal = normal
        self.id = id
        self.is_used = False

    def __lt__(self, other):
        return self.z <= other.z

    @property
    def neighbor_nodes(self) -> List:
        """
        Get all the points neighbor points.

        :return: List of neighbor points.
        """
        neighbor_nodes = [self.cell_code]

        # Find the point's cell.
        x, y, z = utility.decode_cell(self.cell_code)

        # Check for each of the possible 8 neighbors if it exists.
        for i in range(-1, 2):
            for j in range(-1, 2):
                for k in range(-1, 2):
                    cell_corner = x + i, y + j, z + k

                    if cell_corner[0] < 0 or cell_corner[1] < 0 or cell_corner[2] < 0:
                        continue

                    cell_code = utility.encode_cell(cell_corner[0], cell_corner[1], cell_corner[2])
                    neighbor_nodes.append(cell_code)

        return neighbor_nodes


class Edge:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.num_triangles_this_edge_is_in = 0 


class Cell:
    def __init__(self, radius, points=None):
        self.all_points = points
        self.cells = {}
        self.radius = radius
        self.num_cells_per_axis = 0
        self.bounding_box_size = 0
        self.edges = []
        self.triangles = []
        self.cell_size = 0

        if points is not None:
            self.init_with_data(points)

    def init_with_data(self, list_of_points):
        min_x, max_x, min_y, max_y, min_z, max_z = 0, 0, 0, 0, 0, 0

        # Find boundaries for the bounding box of the entire data.
        for point in list_of_points:
            min_x = point.x if point.x < min_x else min_x
            max_x = point.x if point.x > max_x else max_x
            min_y = point.y if point.y < min_y else min_y
            max_y = point.y if point.y > max_y else max_y
            min_z = point.z if point.z < min_z else min_z
            max_z = point.z if point.z > max_z else max_z

        x = max_x - min_x
        y = max_y - min_y
        z = max_z - min_z

        self.bounding_box_size = max(x, y, z)

        # Calculate each cell edge size.
        self.num_cells_per_axis = self.bounding_box_size / (2 * self.radius)
        self.cell_size = self.bounding_box_size / self.num_cells_per_axis

        # Start appending the data points to their cells.
        for point in list_of_points:

            x_cell = int((point.x // self.cell_size) * self.cell_size)
            y_cell = int((point.y // self.cell_size) * self.cell_size)
            z_cell = int((point.z // self.cell_size) * self.cell_size)

            code = utility.encode_cell(x=x_cell, y=y_cell, z=z_cell)
            point.cell_code = code

            # Add the point to the cell in the hash table.
            if code not in self.cells.keys():
                self.cells[code] = []

            self.cells[code].append(point)

    def get_cell_points(self, cell_code):
        points = []

        if cell_code in self.cells.keys():
            p = self.cells[cell_code]
            points.extend(p)

        return points

    def add_edge(self, edge: Edge):
        self.edges.append(edge)

    def remove_edge(self, edge: Edge):
        self.edges.remove(edge)


class Triangle:
	def __init__(self, v1, v2, v3):
		self.v1 = v1
		self.v2 = v2
		self.v3 = v3
		self.vertices = [v1, v2, v3]

	def __eq__(self, other):
		vertices = [self.v1, self.v2, self.v3]
		return other.v1 in vertices and other.v2 in vertices and other.v3 in vertices
