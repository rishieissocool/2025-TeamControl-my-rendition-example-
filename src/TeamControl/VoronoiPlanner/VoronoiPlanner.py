#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 14:43:34 2024

@author: oliver
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import time
from scipy.spatial import Voronoi, voronoi_plot_2d
import networkx as nx
from TeamControl.VoronoiPlanner.Obstacle import Obstacle

class VoronoiPlanner:
    def __init__(self, xsize, ysize, obstacles = None):
        """
        Initialize the Voronoi Planner. Optionally provide initial obstacles.
        
        :param xsize: area x-size
        :param ysize: area y-size
        :param obstacles: List of obstacles (optional).
        """
        self.xsize = xsize
        self.ysize = ysize
        self.obstacle_points = None
        self.voronoi_diagram = None
        self.voronoi_vertices = None
        self.graph = None
        self.update_obstacles(obstacles)

    def update_obstacles(self, obstacles, radius = 75):
        """
        Update the obstacles and rebuild the Voronoi diagram and graph.
        
        :param obstacles: List or array of new obstacle points.
        :param diameter: default robot diameter in mm (if not  in obstacles).
        """
        self.obstacles = obstacles
        self.radius = radius
        self.graph = None
        if obstacles is None:
            self.obstacle_points = None
            return
        self.obstacle_points = [np.array((o.x, o.y)) for o in obstacles]
        self.voronoi_diagram = Voronoi(self.obstacle_points)
        self.voronoi_vertices = self.voronoi_diagram.vertices
        self.graph = self.build_voronoi_graph()
        
    def size(self):
        return np.array((self.xsize, self.ysize))
        
    def is_path_free(self, start, goal, clearance, d0 = None, exclude_unums=[]):
        """
        Check if path to a point at distance d0 from start towards goal is 
        free of obstacles.
    
        :param start: The start point as array(x, y).
        :param goal: The goal point as an array(x, y).
        :param clearance: space the robot needs in any direction from centre.
        :param d0: The distance to check along the direction from start to goal.
        :param exclude_unums: Don't check collision with those.
        :return: True if the path is free of obstacles, False otherwise.
        """
        
        direction = goal - start
        distance = np.linalg.norm(direction)
    
        if distance == 0:
            return False, None  # Start and goal are the same

        if d0 is None or d0 >= distance:    
            target_point = goal
        else:
            direction = direction / distance  # Normalise direction
            target_point = start + d0 * direction
    
        for obstacle in self.obstacles:
            if obstacle.id in exclude_unums:
                continue

            d1 = np.linalg.norm(direction)

            
            if obstacle.intersects_line(start, target_point, clearance):
                return False, None  # Path is not free
    
        return True, target_point
    
    def find_nearest_voronoi_vertex(self, point):
        """Find the nearest Voronoi vertex to a given point."""
        distances = np.linalg.norm(self.voronoi_vertices - point, axis=1)
        nearest_index = np.argmin(distances)
        return self.voronoi_vertices[nearest_index], nearest_index
    
    def build_voronoi_graph(self):
        """Build a graph from Voronoi diagram vertices and ridges."""
        G = nx.Graph()
        for point in self.voronoi_diagram.ridge_vertices:
            if -1 not in point:  # Ignore ridges that extend to infinity 
                if all(0 <= self.voronoi_vertices[point[i]][j] <= [self.xsize, self.ysize][j] for i in range(2) for j in range(2)):                   
                    G.add_edge(point[0], point[1])
        return G
    
    def plan(self, start, goal):
        if self.graph is None:
            self.obstacle_points = [o.centre() for o in self.obstacles]
            self.voronoi_diagram = Voronoi(self.obstacle_points)
            self.voronoi_vertices = self.voronoi_diagram.vertices
            self.graph = self.build_voronoi_graph()
        
        start_vertex, start_vertex_index = self.find_nearest_voronoi_vertex(start.centre())
        goal_vertex, goal_vertex_index = self.find_nearest_voronoi_vertex(goal)

        # Use Dijkstra's algorithm to find the shortest path on the Voronoi graph
        try:
            path = nx.dijkstra_path(self.graph, start_vertex_index, goal_vertex_index)
            path = list(self.voronoi_vertices[path])
        except nx.NetworkXNoPath:
            path = []
        
        return path
    
    def generate_waypoints(self, starts, goals, d0):
        """
        Generate waypoints for each start-goal pair based on obstacle avoidance.
    
        :param starts: List of robots as start of the trajectories.
        :param goals: List of goal points [(x, y), ...].
        :param d0: Distance to check from start towards the goal.
        :return: List of waypoints or None for each start-goal pair.
        """
        waypoints = []
    
        for start, goal in zip(starts, goals):      
            if isinstance(start, Obstacle):
                path_free, waypoint = self.is_path_free(start.centre(), goal,
                                                        start.radius, d0, 
                                                        [start.unum()])
            else:
                path_free, waypoint = self.is_path_free(np.array((start.x, start.y)), 
                                                        goal,
                                                        self.radius, d0, 
                                                        [start.id])
                
            if path_free:
                waypoints.append([waypoint])
            else:
                waypoints.append(self.plan(start, goal))
    
        return waypoints    
    
    def simplify(self, path, clearance, exclude_unums = []):
        """
        Simplify a computed path by greedily skipping intermediate waypoints
        without running into obstacles.
    
        :param path: List of waypoints [(x, y), ...].
        :param clearance: The clearance distance required from obstacles.
        :return: Simplified path.
        """
        if not path or len(path) < 3:
            return path  # No simplification needed
    
        simple_path = [path[0]]  
    
        i = 0
        while i < len(path) - 1:
            next_i = i + 1
            for j in range(i + 2, len(path)):
                if self.is_path_free(np.array(path[i]), np.array(path[j]), 
                                     clearance, d0 = None,
                                     exclude_unums=exclude_unums)[0]:
                    next_i = j
            simple_path.append(path[next_i])
            i = next_i
        
        return simple_path


    
def add_jitter(path, jitter_amount=0.05):
    jitter = np.random.uniform(-jitter_amount, jitter_amount, path.shape)
    return path + jitter

def generate_points(N, dmin, xrange=(0, 1), yrange=(0, 1), other_points = []):
    """
    Generate N random points within specified ranges ensuring each point
    is at least dmin distance from every other point, using rejection sampling.
    
    :param N: Number of points to generate.
    :param dmin: Minimum distance between points.
    :param xrange: Range for x coordinates as (min, max).
    :param yrange: Range for y coordinates as (min, max).
    :param other_points: Additional points to be considered.
    :return: Array of shape (N, 2) with generated points.
    """
    points = []
    allpoints = other_points.copy()
    
    while len(points) < N:
        # Generate a random point within the specified range
        new_point = np.array([
            round(np.random.uniform(*xrange),1),
            round(np.random.uniform(*yrange),1)
        ])
        
        # Check if the new point is at least dmin away from all existing points
        if all(np.linalg.norm(new_point - point) >= dmin for point in allpoints):
            points.append(new_point)
            allpoints.append(new_point)
    
    return np.array(points)


if __name__ == "__main__":

    np.random.seed(23) 
    
    vp = VoronoiPlanner(9000,6000)
    
    starts = [np.array((200, 1800)), np.array((1000, 800)), np.array((500, 2300)),
              np.array((2500, 1000)), np.array((1000, 1500)), np.array((500, 300)),]
    goals = [np.array((3000, 1800)), np.array((4000, 1200)), np.array((2300, 2300)),
             np.array((3000, 200)), np.array((3800, 350)), np.array((1800, 400))]
    clearance = 75
    d0 = 1000
    weAreYellow = True

    # Generate N random opponents
    N = 11
    our_robots = Obstacle.from_numpy_array(starts, clearance,
                                           [i for i in range(1,1+len(starts))],
                                           weAreYellow)

    their_robots = Obstacle.from_numpy_array(generate_points(N, 2*clearance,
                                                             (0,vp.size()[0]),
                                                             (0,vp.size()[1]),
                                                             starts),
                                             clearance,
                                             [i for i in range(1,N)],
                                             not weAreYellow)

    obstacles = our_robots + their_robots
    centres = np.vstack([o.centre() for o in obstacles])

    start_time = time.time()

    vp.update_obstacles(obstacles)

    # Generate waypoints
    initial_waypoints = vp.generate_waypoints(our_robots, goals, d0)
    waypoints = [vp.simplify([s] + w + [g], clearance, [o.unum()]) for s,w,g,o in zip(starts,initial_waypoints,goals,obstacles)]
#    waypoints = [([s] + w + [g], o.unum()) for s,w,g,o in zip(starts,initial_waypoints,goals,obstacles)]
    print(f'{initial_waypoints}')

    end_time = time.time()

    execution_time = end_time - start_time
    print(f"Execution time: {execution_time:.4f} seconds")
        
    # Plot the Voronoi diagram
    fig, ax = plt.subplots(figsize=(10, 10))
    voronoi_plot_2d(vp.voronoi_diagram, ax=ax)
    
    # Set axis limits
    ax.set_xlim(0, vp.xsize)
    ax.set_ylim(0, vp.ysize)

    # Plot the original points (obstacles)
#    ax.plot(centres[:, 0], centres[:, 1], 'bo', label='Obstacles')

    for obstacle in obstacles:
        circle = Circle(obstacle.centre(), obstacle.radius, color='b', fill=False)
        ax.add_patch(circle)

    # Plot the start and goal points
    label1 = 'Start'
    label2 = 'Goal'
    for start, goal in zip(starts,goals):
        ax.plot(start[0], start[1], 'go', label=label1)
        ax.plot(goal[0], goal[1], 'ro', label=label2)
        label1 = None
        label2 = None

    # Plot the Voronoi vertices
    ax.plot(vp.voronoi_vertices[:, 0], vp.voronoi_vertices[:, 1], 'ko', label='Voronoi Vertices')

    colourmap = plt.colormaps['tab10'] 

    # Plot the planned paths
    for i, path in enumerate(waypoints):
        if path is not None:
            p = add_jitter(np.array(path))
            colour = colourmap(i % colourmap.N)  # Cycle through the colormap
            ax.plot(p[:, 0], p[:, 1], '-', linewidth=2, 
                    color=colour, label='Planned Path')

    # Set aspect ratio
    ax.set_aspect('equal', adjustable='box')

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Voronoi Diagram for Navigation')
    plt.legend()
    plt.show()
