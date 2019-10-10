class Point:
  def __init__(self, x, y):
    self.x = x
    self.y = y

class Line:
  def __init__(self, point_A, point_B):
    self.point_A = point_A
    self.point_B = point_B
    self.coefficient_x, self.coefficient_y, self.coefficient_c = self.get_coefficients()

  def determinant2x2(column_1, column_2):
    m_diagonal = column_1[0] * column_2[1]
    s_diagonal = column_1[1] * column_2[0]

    return m_diagonal - s_diagonal

  def intersection(line_r, line_s):
    # Using the Cramer's rule
    det = Line.determinant2x2([line_r.coefficient_x, line_s.coefficient_x],
                        [line_r.coefficient_y, line_s.coefficient_y])

    det_x = Line.determinant2x2([line_r.coefficient_c, line_s.coefficient_c],
                          [line_r.coefficient_y, line_s.coefficient_y])

    det_y = Line.determinant2x2([line_r.coefficient_x, line_s.coefficient_x],
                          [line_r.coefficient_c, line_s.coefficient_c])

    coordinate_x = det_x / det
    coordinate_y = det_y / det
    
    return Point(coordinate_x, coordinate_y)

  def get_coefficients(self):
    coefficient_x = self.point_A.y - self.point_B.y
    coefficient_y = self.point_B.x - self.point_A.x
    coefficient_c = (self.point_A.x * self.point_B.y) - (self.point_A.y * self.point_B.x)

    return (coefficient_x, coefficient_y, -coefficient_c)
