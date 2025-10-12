#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 18:27:43 2024

@author: oliver
"""
import numpy as np

class Obstacle:
    def __init__(self, point:tuple[float,float], radius: float, unum:int, isYellow:bool):
        """
        RoboCup obstacles are disks.
        
        :param point: The centre coordinate (array with x, y).
        :param radius: The radius.
        :param unum: The uniform number (object id)
        :param isYellow: bool 
        """
        self.x, self.y = point
        self.radius = radius
        self.radius2 = radius * radius
        self.id = unum
        self.isYellow = isYellow
        
    @classmethod
    def from_numpy_array(cls, points, radius, unums, isYellow):
        """
        Create a list of Obstacle objects from a NumPy array of points.
        
        :param points: NumPy array of shape (n, 2) where n is the number of points.
        :param radius: The radius for all obstacles.
        :params isYellow: bool or list of bools (if list, length must be len(unums))
        :return: List of Obstacle objects.
        """
        if isinstance(isYellow, list):
            return [cls(point, radius, unum, yellow) for point, unum, yellow in zip(points, unums, isYellow)]
        else:
            return [cls(point, radius, unum, isYellow) for point, unum in zip(points, unums)]
            

    def is_point_inside(self, point):
        """
        Check if a given point is inside the obstacle.
        
        :param point: The point to check (tuple of x, y).
        :return: True if the point is inside the obstacle, False otherwise.
        """
        px, py = point
        return (px - self.x) ** 2 + (py - self.y) ** 2 <= self.radius2
    
    def unum(self):
        return self.id
    
    def centre(self):
        return np.array((self.x, self.y))
    
    def intersects_line(self, start, goal, clearance):
        """
        Check if the line segment from start to goal intersects the 
        obstacle's centre and radius + clearance.
    
        :param start: The start point as array(x, y).
        :param goal: The goal point as array(x, y).
        :param clearance: The clearance distance required from the obstacle.
        :return: True if the line intersects the circle, False otherwise.
        """
        c = self.centre()
        r = self.radius + clearance
        
        # Vector from start to goal
        line_vec = goal - start
        line_len = np.linalg.norm(line_vec)
        line_dir = line_vec / line_len
        
        # Vector from start to circle centre
        to_centre = c - start
        
        # Projection of to_centre onto line_vec
        proj_len = np.dot(to_centre, line_dir)
        
        if proj_len < 0:
            closest_point = start
        elif proj_len > line_len:
            closest_point = goal
        else:
            closest_point = start + proj_len * line_dir
        
        # Distance from the closest point to the circle centre
        distance_to_centre = np.linalg.norm(c - closest_point)
        
        return distance_to_centre < r        

    
    def __repr__(self):
        return f"Obstacle(ID={self.id} ({self.x}, {self.y}), radius={self.radius})"

    
def main():
    # create some obstacle with radius 2
    obstacle = Obstacle((5, 5), 2)

    # define a lines that intersects with obstacle
    line1_start = (3, 3)
    line1_end = (7, 7)  
    # define another one that doesn't
    line2_start = (1, 1)
    line2_end = (2, 2)  

    # do the check if the lines intersect with the obstacle
    intersects_line1 = obstacle.intersects_line(line1_start, line1_end)
    intersects_line2 = obstacle.intersects_line(line2_start, line2_end)

    print(f"Line from {line1_start} to {line1_end} intersects with obstacle: {intersects_line1}")
    print(f"Line from {line2_start} to {line2_end} intersects with obstacle: {intersects_line2}")

if __name__ == "__main__":
    main()    