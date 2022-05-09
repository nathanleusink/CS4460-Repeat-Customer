"""
Author: Jenna Chadwick
Project: Demonstration of Repeat Customer's Learning AI
Class: Intelligent Robotics - 2022Sp CS 4460 001
Professor: Adham Atyabi
"""

# Imports
import random
import re

# For easy tweaking, these are the modifier variables for the velocity function later
selfAdj = .9
globAdj = .6
inertia = .2


# Class definition, the important individual particle
class Particle:
    # Initialization, where the initial position and velocity are added
    def __init__(self, dims, maxval, maxvel):
        # self.maxCoord = [width, height]
        self.maxCoord = maxval
        # The coordinates and velocities are stored in an array to allow for easy expanding
        self.coord = []
        for dim in range(dims):
            self.coord.append(random.randint(0, self.maxCoord))
        # The velocity
        self.vel = []
        for dim in range(dims):
            self.vel.append(random.randint(-maxvel, maxvel))
        # The best coordinates and high score
        self.best = []
        for dim in range(dims):
            self.best.append(self.coord[dim])
        self.best.append(0)

    # This class function moves the particle to a valid location based on the provided velocity
    def move(self, movVec):
        for element in range(len(self.coord)):
            self.vel = movVec.copy()
            self.coord[element] += self.vel[element]

            # After moving it, check to make sure it's in bounds
            if self.coord[element] >= self.maxCoord:
                self.coord[element] = self.maxCoord
            elif self.coord[element] < 0:
                self.coord[element] = 0

    # This sets the high score for this individual particle
    def eval(self, score):
        if int(score) > int(self.best[-1]):
            self.best = self.coord.copy()
            self.best.append(score)


# Writes over a single given line of text
def writeLine(filename, linenum, string):
    f = open(filename, "r")
    current = f.readlines()
    f.close()

    if linenum <= len(current):
        #print(current)
        current[linenum] = str(string) + "\n"

        # open and read the file after the appending:
        f = open(filename, "w")
        f.close()
        f = open(filename, "a")
        for line in current:
            f.writelines(line)
        f.close()

        print("Successfully wrote to file.")
        print("Line written: " + str(string) + " at position: " + str(linenum))
        print()
    else:
        print("WARNING: Could not write to file. Index too high.")
        print("Line not written: " + str(string))
        print()


# This function sets the global high score for the best any particle has ever gotten
def globalBest(particles):
    top = 0
    topInd = 0
    for element, scorePart in enumerate(particles):
        if int(scorePart.best[-1]) >= top:
            top = int(scorePart.best[-1])
            topInd = element

    return particles[topInd]


# Used only for the training, since individual customers are done one at a time
def PSO(particles, table, runs):

    # The loop where the algorithm is run, the number in the range is how many iterations it runs for
    for run in range(runs):
        # globalBest() returns the best particle, this gets its coordinates
        globBest = globalBest(particles).best[0:-1].copy()

        # Now run the algorithm for each particle
        for j, part in enumerate(particles):
            # Print statements to see what it's doing
            #print("Value before move: " + str(trainingScore(table[j], part)))
            #print("Coordinates: " + str(part.coord))

            # Get random value between 0 and 1
            randself = random.random()
            randglob = random.random()
            vec = []
            # For each coordinate, determine a velocity
            for i in range(len(part.coord)):
                vec.append(round((part.vel[i] * inertia) + (selfAdj * randself * (part.best[i] - part.coord[i]))
                                 + (globAdj * randglob * (globBest[i] - part.coord[i]))))
            # Move the particle
            part.move(vec)
            # Score the particle
            part.eval(trainingScore(table[j], part))

            # More print statements for viewing
            #print("Value after move: " + str(trainingScore(table[j], part)))
            #print("Coordinates: " + str(part.coord))
            #print()
        #print("------------------------------------------------")
        #print("global best: " + str(globalBest(particles).best[0:-1]))
        #print("global best value: " + str(globalBest(particles).best[-1]))
        #print()
        #print("------------------------------------------------")

        


# Scores the training data based on the provided file
def trainingScore(training, particle):
    mistakes = 0
    mistakes += abs(int(training["Meat"][0]) - particle.coord[0])
    mistakes += abs(int(training["Cheese"][0]) - particle.coord[1])
    mistakes += abs(int(training["Lettuce"][0]) - particle.coord[2])
    mistakes += abs(int(training["Tomatoes"][0]) - particle.coord[3])
    mistakes += abs(int(training["Onions"][0]) - particle.coord[4])
    return 50 - mistakes

# Gets a decent global baseline
def train(filename):
    # This sets up the random generator
    random.seed()

    # This is a temporary code block for reading in the value information from a file
    # In this case, a 10x10 multiplication table
    f = open(filename, "r")
    text = f.readlines()
    f.close()

    table = []
    for (i, line) in enumerate(text):
        temp_dict = {"Meat": [], "Cheese": [], "Lettuce": [], "Tomatoes": [], "Onions": []}
        match = re.search(r'([\d]+),([\d]+),([\d]+),([\d]+),([\d]+)', line)
        if match:
            temp_dict["Meat"].append(match.group(1))
            temp_dict["Cheese"].append(match.group(2))
            temp_dict["Lettuce"].append(match.group(3))
            temp_dict["Tomatoes"].append(match.group(4))
            temp_dict["Onions"].append(match.group(5))
            table.append(temp_dict)
            #print(temp_dict)
            #print()
        else:
            print("Error in training data, line: " + str(i + 1))

    # End File reading

    # Set up the particle. Value inside the range determines how many
    # For training, one particle per training particles
    particles = []
    for i in range(len(table)):
        # 10 is the max coordinate, and 5 is the max starting velocity
        particles.append(Particle(5, 10, 5))
        particles[i].eval(trainingScore(table[i], particles[i]))
        #print(particles[i].best[-1])

    PSO(particles, table, 30)

    return globalBest(particles)


# Returns a dictionary from the file that stores user data, as well as other info
def dicFromStr(dicStr):
    temp_dict = {"Meat": 0, "Cheese": 0, "Lettuce": 0, "Tomatoes": 0, "Onions": 0}
    bestCoords = []
    best = 0
    match = re.search(r'\[([\d]+), ([\d]+), ([\d]+), ([\d]+), ([\d]+), ([\d]+), ([\d]+), ([\d]+), ([\d]+), ([\d]+), ([\d]+)]', dicStr)
    if match:
        temp_dict["Meat"] = int(match.group(1))
        temp_dict["Cheese"] = int(match.group(2))
        temp_dict["Lettuce"] = int(match.group(3))
        temp_dict["Tomatoes"] = int(match.group(4))
        temp_dict["Onions"] = int(match.group(5))
        bestCoords = [int(match.group(6)), int(match.group(7)), int(match.group(8)), int(match.group(9)), int(match.group(10))]
        best = int(match.group(11))
    else:
        print("WARNING: Failed to match file data")
    return temp_dict, bestCoords, best


# Makes a sandwich (returns the ingredient amounts from the file)
def make(custID):
    f = open("customers.txt", "r")
    current = f.readlines()
    f.close()

    sandwich = {"Meat": 0, "Cheese": 0, "Lettuce": 0, "Tomatoes": 0, "Onions": 0}
    bestCoords = []
    best = 0

    # Negative numbers are not allowed. 0 is the global best.
    if custID < 0:
        print("WARNING: Invalid customer ID")
        print("ID must be 0 or greater. Entered: " + str(custID))
        print()
    # If the index is the next open spot
    elif custID == len(current) - 1:
        print("Preparing new customer profile. ID: " + str(custID))
        print()
        writeLine("customers.txt", custID, current[0])
        sandwich, bestCoords, best = dicFromStr(current[0])
    # If the index is beyond the next spot
    elif custID >= len(current):
        print("WARNING: Invalid customer ID")
        print("ID must be existing or the next available slot. Entered: " + str(custID))
        print()
    # If the index is an existing user
    else:
        print("Retrieving data from existing customer. ID: " + str(custID))
        print()
        sandwich, bestCoords, best = dicFromStr(current[custID])

    print("Your sandwich Quantities from 0 - 10: " + str(sandwich))
    print()
    return sandwich, bestCoords, best


# Uses face recog ition data to score the customer's sandwich and move it based on the PSO equation
def score(custID, score):
    # If the ID is the global best
    if custID < 1:
        print("WARNING: Bad score ID. ID must be 1 or greater.")

    # make a theoretical sandwich to compare. Should be identical to the last prepared.
    sandwich, bestCoords, bestScore = make(custID)

    # A score of 0 or lower indicates an error.
    if int(bestScore) > 0:
        # Only the best of the global best is used.
        unused, globBestCoords, gbest = make(0)

        # Make some particles-- the current user particle, and the global best benchmark
        sand = Particle(5, 10, 5)
        globBest = Particle(5, 10, 5)
        sand.coord = [int(sandwich["Meat"]), int(sandwich["Cheese"]), int(sandwich["Lettuce"]), int(sandwich["Tomatoes"]), int(sandwich["Onions"])]
        globBest.coord = globBestCoords
        sand.best = bestCoords + [bestScore]
        sand.eval(score)
        globBest.eval(gbest)

        # If the current set is the best, make it so
        if int(bestScore) > int(gbest):
            newbest = sand.coord.copy() + sand.coord.copy()
            newbest.append(int(bestScore))
            writeLine("customers.txt", 0, newbest)

        # Get random value between 0 and 1
        randself = random.random()
        randglob = random.random()
        vec = []

        # For each coordinate, determine a velocity
        for i in range(len(sand.coord)):
            vec.append(round((sand.vel[i] * inertia) + (selfAdj * randself * (sand.best[i] - sand.coord[i]))
                             + (globAdj * randglob * (globBest.coord[i] - sand.coord[i]))))
        # Move the particle
        sand.move(vec)

        # Save the results
        printer = sand.coord.copy() + sand.best.copy()
        writeLine("customers.txt", custID, printer)
    else:
        print("WARNING: Failed to score.")

