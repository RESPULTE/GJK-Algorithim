from typing import List, Tuple, Union, Optional
from vector2D import Vector2D as vec
from math import sqrt, acos, sin, cos, radians

Point = Tuple[int, int]


def get_circumcircle(triangle: List[Point], radius: bool = True) -> Union[Tuple[vec, float], vec]:
    point_a, point_b, point_c = triangle

    angle_a = sin(2 * get_angle(point_b, point_c, point_a))
    angle_b = sin(2 * get_angle(point_c, point_a, point_b))
    angle_c = sin(2 * get_angle(point_a, point_b, point_c))

    circumcenter_x = (point_a[0] * angle_a + point_b[0] * angle_b + point_c[0] * angle_c) / (angle_a + angle_b + angle_c)
    circumcenter_y = (point_a[1] * angle_a + point_b[1] * angle_b + point_c[1] * angle_c) / (angle_a + angle_b + angle_c)
    circumcenter   = (circumcenter_x, circumcenter_y)
    
    if radius:
        circumradius = get_length(point_a - point_b) / angle_c
        return circumcenter, circumradius

    return circumcenter

def get_bounding_box(polygon: List[Point]) -> Tuple[vec, vec]:
    x_coords   = [x for (x, y) in polygon]
    y_coords   = [y for (x, y) in polygon]
    topright   = vec(max(x_coords), max(y_coords))
    bottomleft = vec(min(x_coords), min(y_coords)) 
    return bottomleft, topright


def get_intersect(line1: List[vec], line2: List[vec]) -> Union[bool, vec]:
    line1, line2 = vec.convert(line1), vec.convert(line2)
    start = line2[0] - line1[0]
    end_1, end_2 = line1[1] - line1[0], line2[1] - line2[0]
    determinant = end_1.cross(end_2)
    if determinant == 0:
        return False
    check_1 = (start).cross(end_2) / determinant
    check_2 = (start).cross(end_1) / determinant
    if (0 <= check_1 <= 1) and (0 <= check_2 <= 1):
        return round(line1[0] + (line1[1] - line1[0]) * check_1, 2)

    return False


def get_corner(polygon: List[Point]) -> Tuple[vec, vec]:
    topright   = max(polygon, lambda point: point[0] + point[1])
    bottomleft = min(polygon, lambda point: point[0] + point[1])
    return bottomleft, topright       


def get_center(polygon: List[Point]) -> vec:
    bottomleft, topright = get_bounding_box(polygon)
    center_x = bottomleft.x + ((topright.x - bottomleft.x) / 2)
    center_y = bottomleft.y + ((topright.y - bottomleft.y) / 2)
    return vec(center_x, center_y)


def get_support(shape1: List[vec], shape2: List[vec], direction: vec) -> vec:
    s1_furthestpoint = max(shape1, key=lambda point: point.dot(direction))
    s2_furthestpoint = max(shape2, key=lambda point: point.dot(-direction))
    support_point = s1_furthestpoint - s2_furthestpoint
    return support_point 


def is_convex(polygon: List[vec]) -> bool:
    if len(polygon) == 3: 
        return True

    polygon = vec.convert(polygon)
    for ind, center_point in enumerate(polygon):
        center_to_right = polygon[(ind + 1) % len(polygon)] 
        center_to_left  = polygon[(ind - 1) % len(polygon)] 

        if center_to_left.cross(center_to_right, origin=center_point) < 0:
            return False 

    return True


def is_collinear(points: List[vec]) -> bool:
    return all([True if point.cross(points[(ind + 1) % len(points)]) == 0 else False for ind, point in enumerate(points)]) 
