import math

class Vector1d:
    def __init__(self, x=0.0):
        self.x = float(x)

    def add(self, other):
        return Vector1d(self.x + other.x)

    def subtract(self, other):
        return Vector1d(self.x - other.x)

    def multiply(self, other):
        return Vector1d(self.x * other.x)

    def divide(self, other):
        if other.x == 0:
            raise ValueError("Vector cannot be zero.")
        return Vector1d(self.x / other.x)

    def get_magnitude(self):
        return abs(self.x)

    def dot(self, other):
        return self.x * other.x

    def clone(self):
        return Vector1d(self.x)

    def __str__(self):
        return f"({self.x})"

    def __eq__(self, other):
        if not isinstance(other, Vector1d):
            return NotImplemented
        return self.x == other.x

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return f"Vector1d(x={self.x})"

class Vector2d:
    def __init__(self, x=0.0, y=0.0):
        self.x = float(x)
        self.y = float(y)

    def add(self, other):
        return Vector2d(self.x + other.x, self.y + other.y)

    def subtract(self, other):
        return Vector2d(self.x - other.x, self.y - other.y)

    def multiply(self, other):
        return Vector2d(self.x * other.x, self.y * other.y)

    def divide(self, other):
        if other.x == 0 or other.y == 0:
            raise ValueError("Vector cannot be zero.")
        return Vector2d(self.x / other.x, self.y / other.y)

    def get_magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def clone(self):
        return Vector2d(self.x, self.y)

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, other):
        if not isinstance(other, Vector2d):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return f"Vector2d(x={self.x}, y={self.y})"

class Vector3d:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def add(self, other):
        return Vector3d(self.x + other.x, self.y + other.y, self.z + other.z)

    def subtract(self, other):
        return Vector3d(self.x - other.x, self.y - other.y, self.z - other.z)

    def multiply(self, other):
        return Vector3d(self.x * other.x, self.y * other.y, self.z * other.z)

    def divide(self, other):
        if other.x == 0 or other.y == 0 or other.z == 0:
            raise ValueError("Vector cannot be zero.")
        return Vector3d(self.x / other.x, self.y / other.y, self.z / other.z)

    def get_magnitude(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        """Computes the cross product of this vector with another vector."""
        cx = self.y * other.z - self.z * other.y
        cy = self.z * other.x - self.x * other.z
        cz = self.x * other.y - self.y * other.x
        return Vector3d(cx, cy, cz)

    def clone(self):
        return Vector3d(self.x, self.y, self.z)

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"

    def __eq__(self, other):
        if not isinstance(other, Vector3d):
            return NotImplemented
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return f"Vector3d(x={self.x}, y={self.y}, z={self.z})"

class Vector4d:
    def __init__(self, x=0.0, y=0.0, z=0.0, w=0.0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.w = float(w)

    def add(self, other):
        return Vector4d(self.x + other.x, self.y + other.y, self.z + other.z, self.w + other.w)

    def subtract(self, other):
        return Vector4d(self.x - other.x, self.y - other.y, self.z - other.z, self.w - other.w)

    def multiply(self, other):
        return Vector4d(self.x * other.x, self.y * other.y, self.z * other.z, self.w * other.w)

    def divide(self, other):
        if other.x == 0 or other.y == 0 or other.z == 0 or other.w == 0:
            raise ValueError("Vector cannot be zero.")
        return Vector4d(self.x / other.x, self.y / other.y, self.z / other.z, self.w / other.w)

    def get_magnitude(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2 + self.w**2)

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z + self.w * other.w

    def clone(self):
        return Vector4d(self.x, self.y, self.z, self.w)

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z}, {self.w})"

    def __eq__(self, other):
        if not isinstance(other, Vector4d):
            return NotImplemented
        return self.x == other.x and self.y == other.y and self.z == other.z and self.w == other.w

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return f"Vector4d(x={self.x}, y={self.y}, z={self.z}, w={self.w})"

class Vector2dBoxArea:
    def __init__(self, x1=0.0, y1=0.0, x2=0.0, y2=0.0):
        self.x1 = float(x1)
        self.y1 = float(y1)
        self.x2 = float(x2)
        self.y2 = float(y2)

    def width(self):
        return abs(self.x2 - self.x1)

    def height(self):
        return abs(self.y2 - self.y1)

    def area(self):
        return self.width() * self.height()

    def contains_point(self, point):
        return (min(self.x1, self.x2) <= point.x <= max(self.x1, self.x2) and
                min(self.y1, self.y2) <= point.y <= max(self.y1, self.y2))

    def intersects(self, other):
        return not (self.x2 < other.x1 or self.x1 > other.x2 or
                    self.y2 < other.y1 or self.y1 > other.y2)

    def move(self, vector):
        return Vector2dBoxArea(
            self.x1 + vector.x, self.y1 + vector.y,
            self.x2 + vector.x, self.y2 + vector.y
        )

    def clone(self):
        return Vector2dBoxArea(self.x1, self.y1, self.x2, self.y2)

    def __str__(self):
        return f"(({self.x1}, {self.y1}) -> ({self.x2}, {self.y2}))"

    def __eq__(self, other):
        if not isinstance(other, Vector2dBoxArea):
            return NotImplemented
        return (self.x1 == other.x1 and self.y1 == other.y1 and
                self.x2 == other.x2 and self.y2 == other.y2)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return f"Vector2dBoxArea(x1={self.x1}, y1={self.y1}, x2={self.x2}, y2={self.y2})"

class Vector2dPolygon:
    def __init__(self, points=None):
        self.points = [p.clone() for p in points] if points else []

    def add_point(self, point):
        self.points.append(point.clone())

    def move(self, vector):
        return Vector2dPolygon([p.add(vector) for p in self.points])

    def clone(self):
        return Vector2dPolygon(self.points)

    def area(self):
        n = len(self.points)
        if n < 3:
            return 0.0
        area = 0.0
        for i in range(n):
            j = (i + 1) % n
            area += self.points[i].x * self.points[j].y
            area -= self.points[j].x * self.points[i].y
        return abs(area) / 2.0

    def contains_point(self, point):
        n = len(self.points)
        inside = False
        x, y = point.x, point.y
        for i in range(n):
            j = (i + 1) % n
            xi, yi = self.points[i].x, self.points[i].y
            xj, yj = self.points[j].x, self.points[j].y
            intersect = ((yi > y) != (yj > y)) and \
                        (x < (xj - xi) * (y - yi) / (yj - yi + 1e-12) + xi)
            if intersect:
                inside = not inside
        return inside

    def get_bounding_box(self):
        if not self.points:
            return Vector2dBoxArea(0, 0, 0, 0)
        min_x = min(p.x for p in self.points)
        max_x = max(p.x for p in self.points)
        min_y = min(p.y for p in self.points)
        max_y = max(p.y for p in self.points)
        return Vector2dBoxArea(min_x, min_y, max_x, max_y)

    def intersects(self, other):
        # Uses Separating Axis Theorem
        def get_axes(polygon):
            axes = []
            for i in range(len(polygon)):
                p1 = polygon[i]
                p2 = polygon[(i + 1) % len(polygon)]
                edge = p2.subtract(p1)
                normal = Vector2d(-edge.y, edge.x)
                mag = normal.get_magnitude()
                if mag != 0:
                    normal = normal.divide(mag)
                axes.append(normal)
            return axes

        def project(polygon, axis):
            dots = [p.dot(axis) for p in polygon]
            return min(dots), max(dots)

        poly1 = self.points
        poly2 = other.points
        for axis in get_axes(poly1) + get_axes(poly2):
            min_a, max_a = project(poly1, axis)
            min_b, max_b = project(poly2, axis)
            if max_a < min_b or max_b < min_a:
                return False
        return True

    def __str__(self):
        return f"Polygon({', '.join(str(p) for p in self.points)})"

    def __eq__(self, other):
        if not isinstance(other, Vector2dPolygon):
            return NotImplemented
        if len(self.points) != len(other.points):
            return False
        for i in range(len(self.points)):
            if self.points[i] != other.points[i]:
                return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return f"Vector2dPolygon(points=[{', '.join(repr(p) for p in self.points)}])"