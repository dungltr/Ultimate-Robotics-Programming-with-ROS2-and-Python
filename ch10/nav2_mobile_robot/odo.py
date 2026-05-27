import math
class DifferentialDriveRobot:
def __init__(self, wheel_separation, wheel_radius, encoder_resolution):
  self.wheel_separation = wheel_separation
  self.wheel_radius = wheel_radius
  self.encoder_resolution = encoder_resolution
  self.x = 0.0
  self.y = 0.0
  self.theta = 0.0
def update_odometry(self, rotationsL, rotationsR):
  circumference = 2 * math.pi * self.wheel_radius
  dL = rotationsL * circumference
  dR = rotationsR * circumference
  d = (dL + dR) / 2
  delta_theta = (dR - dL) / self.wheel_separation
  self.theta += delta_theta
  delta_x = d * math.cos(self.theta)
  delta_y = d * math.sin(self.theta)
  self.x += delta_x
  self.y += delta_y
  return self.x, self.y, self.theta
  
