from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])

def angular_coefficient(point_a, point_b):
  delt_x = point_b.x - point_a.x
  delt_y = point_b.y - point_a.y

  return delt_y / delt_x

def linear_coefficient(point):
  pass

def reduced_line_equation():
  pass

def geral_line_equation(point, angular_coefficient):
  pass
  # return y + (-1 * (angular_coefficient * x)) - point.y + (-1 * (angular_coefficient * point.x)))

def line_intersection():
  pass
