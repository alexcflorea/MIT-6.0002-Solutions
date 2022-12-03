# -*- coding: utf-8 -*-
# Problem Set 3: Simulating robots
# Name: Alex Florea
# Collaborators (discussion): None
# Time: 6:00

import math
import random

import ps3_visualize
import pylab

# For python 2.7:
from ps3_verify_movement27 import test_robot_movement

# === Provided class Position
class Position(object):
    """
    A Position represents a location in a two-dimensional room, where
    coordinates are given by floats (x, y).
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y
        
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def get_new_position(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: float representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.get_x(), self.get_y()
        
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        
        return Position(new_x, new_y)

    def __str__(self):  
        return "Position: " + str(math.floor(self.x)) + ", " + str(math.floor(self.y))


# === Problem 1
class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. Each tile
    has some fixed amount of dirt. The tile is considered clean only when the amount
    of dirt on this tile is 0.
    """
    def __init__(self, width, height, dirt_amount):
        """
        Initializes a rectangular room with the specified width, height, and 
        dirt_amount on each tile.

        width: an integer > 0
        height: an integer > 0
        dirt_amount: an integer >= 0
        """
        if (width <= 0) or (height <= 0) or (dirt_amount < 0):
            raise ValueError('Invalid Parameter')
        
        self.width = width
        self.height = height
        self.dirt_amount = dirt_amount
        
        #Initialize an w x h size room
        room = {}
        for i in range(width):
            for j in range(height):
                room[(i,j)] = dirt_amount
        
        self.room = room
    
    def clean_tile_at_position(self, pos, capacity):
        """
        Mark the tile under the position pos as cleaned by capacity amount of dirt.

        Assumes that pos represents a valid position inside this room.

        pos: a Position object
        capacity: the amount of dirt to be cleaned in a single time-step
                  can be negative which would mean adding dirt to the tile

        Note: The amount of dirt on each tile should be NON-NEGATIVE.
              If the capacity exceeds the amount of dirt on the tile, mark it as 0.
        """
        #Get (x, y) of position round down to int
        x = math.floor(pos.get_x())
        y = math.floor(pos.get_y())
    
        #Cleans dirt at loc(x, y)
        self.room[(x, y)] -= capacity
        
        #If dirt negative set it to zero
        if self.room[(x, y)] < 0:
            self.room[(x, y)] = 0

    def is_tile_cleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        
        Returns: True if the tile (m, n) is cleaned, False otherwise

        Note: The tile is considered clean only when the amount of dirt on this
              tile is 0.
        """
        
        return self.room[(m, n)] == 0

    def get_num_cleaned_tiles(self):
        """
        Returns: an integer; the total number of clean tiles in the room
        """
        numCleanTiles = 0
        
        #Goes through each tile in a given room and check if it's zero
        for tile in list(self.room.values()):
            if tile == 0:
                numCleanTiles += 1
                    
        return numCleanTiles
            
        
    def is_position_in_room(self, pos):
        """
        Determines if pos is inside the room.

        pos: a Position object.
        Returns: True if pos is in the room, False otherwise.
        """
        x = math.floor(pos.get_x())
        y = math.floor(pos.get_y())
        
        return (x, y) in self.room
        
    def get_dirt_amount(self, m, n):
        """
        Return the amount of dirt on the tile (m, n)
        
        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer

        Returns: an integer
        """
        return self.room[(m, n)]
        
    def get_num_tiles(self):
        """
        Returns: an integer; the total number of tiles in the room
        """
        # do not change -- implement in subclasses.
        raise NotImplementedError 
        
    def is_position_valid(self, pos):
        """
        pos: a Position object.
        
        returns: True if pos is in the room and (in the case of FurnishedRoom) 
                 if position is unfurnished, False otherwise.
        """
        # do not change -- implement in subclasses
        raise NotImplementedError         

    def get_random_position(self):
        """
        Returns: a Position object; a random position inside the room
        """
        # do not change -- implement in subclasses
        raise NotImplementedError        


class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times, the robot has a particular position and direction in the room.
    The robot also has a fixed speed and a fixed cleaning capacity.

    Subclasses of Robot should provide movement strategies by implementing
    update_position_and_clean, which simulates a single time-step.
    """
    def __init__(self, room, speed, capacity):
        """
        Initializes a Robot with the given speed and given cleaning capacity in the 
        specified room. The robot initially has a random direction and a random 
        position in the room.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        capacity: a positive interger; the amount of dirt cleaned by the robot 
                  in a single time-step
        """
        if (speed <=0) or (capacity <0):
            raise ValueError('Invalid speed')
            
        self.room = room
        self.speed = speed
        self.capacity = capacity
        
        #Returns random position object using Room's attribute
        self.position = room.get_random_position()
        
        #Returns random direction (in degrees 0<=direction<360) by generating
        #a random int between [0, 359] then adding a random float [0.0, 1.0)
        self.direction = random.randint(0, 359) + random.random()

    def get_robot_position(self):
        """
        Returns: a Position object giving the robot's position in the room.
        """
        return self.position

    def get_robot_direction(self):
        """
        Returns: a float d giving the direction of the robot as an angle in
        degrees, 0.0 <= d < 360.0.
        """
        return self.direction

    def set_robot_position(self, position):
        """
        Set the position of the robot to position.

        position: a Position object.
        """
        self.position = position

    def set_robot_direction(self, direction):
        """
        Set the direction of the robot to direction.

        direction: float representing an angle in degrees
        """
        self.direction = direction

    def update_position_and_clean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new random position (if the new position is invalid, 
        rotate once to a random new direction, and stay stationary) and mark the tile it is on as having
        been cleaned by capacity amount. 
        """
        # do not change -- implement in subclasses
        raise NotImplementedError

# === Problem 2
class EmptyRoom(RectangularRoom):
    """
    An EmptyRoom represents a RectangularRoom with no furniture.
    """
    def get_num_tiles(self):
        """
        Returns: an integer; the total number of tiles in the room
        """
        return len(self.room)
        
    def is_position_valid(self, pos):
        """
        pos: a Position object.
        
        Returns: True if pos is in the room, False otherwise.
        """
        x = math.floor(pos.get_x())
        y = math.floor(pos.get_y())
        
        return (x, y) in self.room
        
    def get_random_position(self):
        """
        Returns: a Position object; a valid random position (inside the room).
        """
        #Generates random (x, y) float s.t. 0 <= x < roomWidth, same for y
        randX = self.width * random.random()
        randY = self.height * random.random()
        
        return Position(randX, randY)


class FurnishedRoom(RectangularRoom):
    """
    A FurnishedRoom represents a RectangularRoom with a rectangular piece of 
    furniture. The robot should not be able to land on these furniture tiles.
    """
    def __init__(self, width, height, dirt_amount):
        """ 
        Initializes a FurnishedRoom, a subclass of RectangularRoom. FurnishedRoom
        also has a list of tiles which are furnished (furniture_tiles).
        """
        # This __init__ method is implemented for you -- do not change.
        
        # Call the __init__ method for the parent class
        RectangularRoom.__init__(self, width, height, dirt_amount)
        # Adds the data structure to contain the list of furnished tiles
        self.furniture_tiles = []
        
    def add_furniture_to_room(self):
        """
        Add a rectangular piece of furniture to the room. Furnished tiles are stored 
        as (x, y) tuples in the list furniture_tiles 
        
        Furniture location and size is randomly selected. Width and height are selected
        so that the piece of furniture fits within the room and does not occupy the 
        entire room. Position is selected by randomly selecting the location of the 
        bottom left corner of the piece of furniture so that the entire piece of 
        furniture lies in the room.
        """
        # This addFurnitureToRoom method is implemented for you. Do not change it.
        furniture_width = random.randint(1, self.width - 1)
        furniture_height = random.randint(1, self.height - 1)

        # Randomly choose bottom left corner of the furniture item.    
        f_bottom_left_x = random.randint(0, self.width - furniture_width)
        f_bottom_left_y = random.randint(0, self.height - furniture_height)

        # Fill list with tuples of furniture tiles.
        for i in range(f_bottom_left_x, f_bottom_left_x + furniture_width):
            for j in range(f_bottom_left_y, f_bottom_left_y + furniture_height):
                self.furniture_tiles.append((i,j))             

    def is_tile_furnished(self, m, n):
        """
        Return True if tile (m, n) is furnished.
        """
        return (m,n) in self.furniture_tiles
        
    def is_position_furnished(self, pos):
        """
        pos: a Position object.

        Returns True if pos is furnished and False otherwise
        """
        fx = math.floor(pos.get_x())
        fy = math.floor(pos.get_y())
        
        return (fx, fy) in self.furniture_tiles
        
    def is_position_valid(self, pos):
        """
        pos: a Position object.
        
        returns: True if pos is in the room and is unfurnished, False otherwise.
        """
        x = math.floor(pos.get_x())
        y = math.floor(pos.get_y())
        
        return ((x, y) in self.room) and ((x, y) not in self.furniture_tiles)
        
    def get_num_tiles(self):
        """
        Returns: an integer; the total number of tiles in the room that can be accessed.
        """
        totTiles = len(self.room)
        furnTiles = len(self.furniture_tiles)
        
        #Returns #total available tiles - #inaccessible tiles
        return totTiles - furnTiles
        
    def get_random_position(self):
        """
        Returns: a Position object; a valid random position (inside the room and not in a furnished area).
        """
        #Sets boolean stop and loops through random positions until a valid one is found
        stop = False
        while not stop:
            randX = self.width * random.random()
            randY = self.height * random.random()
            stop = self.is_position_valid(Position(randX, randY))
        
        return Position(randX, randY)

# === Problem 3
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current
    direction; when it would hit a wall or furtniture, it *instead*
    chooses a new direction randomly.
    """
    def update_position_and_clean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new random position (if the new position is invalid, 
        rotate once to a random new direction, and stay stationary) and clean the dirt on the tile
        by its given capacity. 
        """
        #Calculate new position for current angle and speed
        newPos = self.position.get_new_position(self.direction, self.speed)
        
        #If newPos is valid move there and clean tile
        if self.room.is_position_valid(newPos):
            self.set_robot_position(newPos)
            self.room.clean_tile_at_position(newPos, self.capacity)
        
        #Else set new random direction (do not clean current tile or move)   
        else:
            self.set_robot_direction(random.randint(0, 359) + random.random())
            

# Uncomment this line to see your implementation of StandardRobot in action!
# test_robot_movement(StandardRobot, EmptyRoom)
# test_robot_movement(StandardRobot, FurnishedRoom)

# === Problem 4
class FaultyRobot(Robot):
    """
    A FaultyRobot is a robot that will not clean the tile it moves to and
    pick a new, random direction for itself with probability p rather
    than simply cleaning the tile it moves to.
    """
    p = 0.15

    @staticmethod
    def set_faulty_probability(prob):
        """
        Sets the probability of getting faulty equal to PROB.

        prob: a float (0 <= prob <= 1)
        """
        FaultyRobot.p = prob
    
    def gets_faulty(self):
        """
        Answers the question: Does this FaultyRobot get faulty at this timestep?
        A FaultyRobot gets faulty with probability p.

        returns: True if the FaultyRobot gets faulty, False otherwise.
        """
        return random.random() < FaultyRobot.p
    
    def update_position_and_clean(self):
        """
        Simulate the passage of a single time-step.

        Check if the robot gets faulty. If the robot gets faulty,
        do not clean the current tile and change its direction randomly.

        If the robot does not get faulty, the robot should behave like
        StandardRobot at this time-step (checking if it can move to a new position,
        move there if it can, pick a new direction and stay stationary if it can't)
        """
        #If robot gets faulty
        if self.gets_faulty():
            self.set_robot_direction(random.randint(0, 359) + random.random())
            
        #Else robot NOT faulty (behaves like StandardRobot)
        else:
            #Calculate new position for current angle and speed
            newPos = self.position.get_new_position(self.direction, self.speed)
            
            #If newPos is valid move there and clean tile
            if self.room.is_position_valid(newPos):
                self.set_robot_position(newPos)
                self.room.clean_tile_at_position(newPos, self.capacity)
            
            #Else set new random direction (do not clean current tile or move)   
            else:
                self.set_robot_direction(random.randint(0, 359) + random.random())
        
    
# test_robot_movement(FaultyRobot, EmptyRoom)

# === Problem 5
def run_simulation(num_robots, speed, capacity, width, height, dirt_amount, min_coverage, num_trials,
                  robot_type):
    """
    Runs num_trials trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction min_coverage of the room.

    The simulation is run with num_robots robots of type robot_type, each       
    with the input speed and capacity in a room of dimensions width x height
    with the dirt dirt_amount on each tile.
    
    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    capacity: an int (capacity >0)
    width: an int (width > 0)
    height: an int (height > 0)
    dirt_amount: an int
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. StandardRobot or
                FaultyRobot)
    """
    avgTimeSteps = []
    
    #Loop for number of trials to run in simulation
    while num_trials > 0:
        timeSteps = 0
        
        #Uncomment to see visualization
        ### anim = ps3_visualize.RobotVisualization(num_robots, width, height, False, 0)
        
        
        #Create an empty list to house Robot objects
        robotList = []
        
        #Create a new Empty room for one simulation
        newRoom = EmptyRoom(width, height, dirt_amount)
        
        #Add specified number of robots to room
        for robot in range(num_robots):
            #Make a new robot object and add to list
            robotList.append(robot_type(newRoom, speed, capacity))
        
        #Return the current fraction of cleaned tiles to total tiles
        currentRoomCoverage = newRoom.get_num_cleaned_tiles() / newRoom.get_num_tiles()
        
        #While the room is stil below min cleaned move a robot
        while currentRoomCoverage < min_coverage:
            #Move each robot and recalculate room coverage
            for robot in robotList:
                robot.update_position_and_clean()
                currentRoomCoverage = newRoom.get_num_cleaned_tiles() / newRoom.get_num_tiles()
                
                #Update animation
                ### anim.update(newRoom, robotList)
                
            #Increment time steps (NOTE we consider each robot moves in unison so time updated only
            #after they've all moved)
            timeSteps += 1
        
        #Close animation
        ### anim.done()        
       
        #Once room is sufficiently clean add num timeSteps to avg list
        avgTimeSteps += [timeSteps]
        
        #Decrement numTrials
        num_trials -= 1
        
    #When all trials complete compute average Time Steps
    return sum(avgTimeSteps)/len(avgTimeSteps)

# print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 5, 5, 3, 1.0, 50, StandardRobot)))
# print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 10, 10, 3, 0.8, 50, StandardRobot)))
# print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 10, 10, 3, 0.9, 50, StandardRobot)))
# print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 20, 20, 3, 0.5, 50, StandardRobot)))
# print ('avg time steps: ' + str(run_simulation(3, 1.0, 1, 20, 20, 3, 0.5, 50, StandardRobot)))

# === Problem 6
#
# ANSWER THE FOLLOWING QUESTIONS:
#
# 1) How does the performance of the two robot types compare when cleaning 80%
#       of a 20x20 room?
#
#   The Standard Robot is superior to the Faulty Robot at every number of 
#   robots tested.
#
# 2) How does the performance of the two robot types compare when two of each
#       robot cleans 80% of rooms with dimensions 
#       10x30, 20x15, 25x12, and 50x6?
#
#   The Standard Robot is superior to the Faulty Robot at every number of 
#   robots tested. The increase in performance at ~1.33 is interesting, perhaps
#   the optimal aspect ration is near 1:1. Also interesting is that the faulty
#   robot starts to decrease in performance at a much faster rate at higher aspect
#   ratios than the standard robot.

def show_plot_compare_strategies(title, x_label, y_label):
    """
    Produces a plot comparing the two robot strategies in a 20x20 room with 80%
    minimum coverage.
    """
    num_robot_range = range(1, 11)
    times1 = []
    times2 = []
    for num_robots in num_robot_range:
        print ("Plotting", num_robots, "robots...")
        times1.append(run_simulation(num_robots, 1.0, 1, 20, 20, 3, 0.8, 20, StandardRobot))
        times2.append(run_simulation(num_robots, 1.0, 1, 20, 20, 3, 0.8, 20, FaultyRobot))
    pylab.plot(num_robot_range, times1)
    pylab.plot(num_robot_range, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'FaultyRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()
    
def show_plot_room_shape(title, x_label, y_label):
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """
    aspect_ratios = []
    times1 = []
    times2 = []
    for width in [10, 20, 25, 50]:
        height = 300//width
        print ("Plotting cleaning time for a room of width:", width, "by height:", height)
        aspect_ratios.append(float(width) / height)
        times1.append(run_simulation(2, 1.0, 1, width, height, 3, 0.8, 200, StandardRobot))
        times2.append(run_simulation(2, 1.0, 1, width, height, 3, 0.8, 200, FaultyRobot))
    pylab.plot(aspect_ratios, times1)
    pylab.plot(aspect_ratios, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'FaultyRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()


# show_plot_compare_strategies('Time to clean 80% of a 20x20 room, for various numbers of robots','Number of robots','Time / steps')
# show_plot_room_shape('Time to clean 80% of a 300-tile room for various room shapes','Aspect Ratio', 'Time / steps')