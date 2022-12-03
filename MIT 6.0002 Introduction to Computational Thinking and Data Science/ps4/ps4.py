# Problem Set 4: Simulating the Spread of Disease and Bacteria Population Dynamics
# Name: Alex Florea
# Collaborators (Discussion): None
# Time: 4:00

import math
import numpy as np
import pylab as pl
import random

#TODO REMEMBER TO REMOVE
# random.seed(0)

##########################
# End helper code
##########################

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleBacteria
    and ResistantBacteria classes to indicate that a bacteria cell does not
    reproduce. You should use NoChildException as is; you do not need to
    modify it or add any code.
    """


def make_one_curve_plot(x_coords, y_coords, x_label, y_label, title):
    """
    Makes a plot of the x coordinates and the y coordinates with the labels
    and title provided.

    Args:
        x_coords (list of floats): x coordinates to graph
        y_coords (list of floats): y coordinates to graph
        x_label (str): label for the x-axis
        y_label (str): label for the y-axis
        title (str): title for the graph
    """
    pl.figure()
    pl.plot(x_coords, y_coords)
    pl.xlim([x_coords[0], x_coords[-1]+1])
    pl.xlabel(x_label)
    pl.ylabel(y_label)
    pl.title(title)
    pl.show()


def make_two_curve_plot(x_coords,
                        y_coords1,
                        y_coords2,
                        y_name1,
                        y_name2,
                        x_label,
                        y_label,
                        title):
    """
    Makes a plot with two curves on it, based on the x coordinates with each of
    the set of y coordinates provided.

    Args:
        x_coords (list of floats): the x coordinates to graph
        y_coords1 (list of floats): the first set of y coordinates to graph
        y_coords2 (list of floats): the second set of y-coordinates to graph
        y_name1 (str): name describing the first y-coordinates line
        y_name2 (str): name describing the second y-coordinates line
        x_label (str): label for the x-axis
        y_label (str): label for the y-axis
        title (str): the title of the graph
    """
    pl.figure()
    pl.plot(x_coords, y_coords1, label=y_name1)
    pl.plot(x_coords, y_coords2, label=y_name2)
    pl.legend()
    pl.xlim([x_coords[0], x_coords[-1]+1])
    pl.xlabel(x_label)
    pl.ylabel(y_label)
    pl.title(title)
    pl.show()


##########################
# PROBLEM 1
##########################

class SimpleBacteria(object):
    """A simple bacteria cell with no antibiotic resistance"""

    def __init__(self, birth_prob, death_prob):
        """
        Args:
            birth_prob (float in [0, 1]): Maximum possible reproduction
                probability
            death_prob (float in [0, 1]): Maximum death probability
        """
        self.birth_prob = birth_prob
        self.death_prob = death_prob

    def is_killed(self):
        """
        Stochastically determines whether this bacteria cell is killed in
        the patient's body at a time step, i.e. the bacteria cell dies with
        some probability equal to the death probability each time step.

        Returns:
            bool: True with probability self.death_prob, False otherwise.
        """
        return (random.random() <= self.death_prob)
        

    def reproduce(self, pop_density):
        """
        Stochastically determines whether this bacteria cell reproduces at a
        time step. Called by the update() method in the Patient and
        TreatedPatient classes.

        The bacteria cell reproduces with probability
        self.birth_prob * (1 - pop_density).

        If this bacteria cell reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleBacteria (which has the same
        birth_prob and death_prob values as its parent).

        Args:
            pop_density (float): The population density, defined as the
                current bacteria population divided by the maximum population

        Returns:
            SimpleBacteria: A new instance representing the offspring of
                this bacteria cell (if the bacteria reproduces). The child
                should have the same birth_prob and death_prob values as
                this bacteria.

        Raises:
            NoChildException if this bacteria cell does not reproduce.
        """
        if (random.random() <= (self.birth_prob * (1 - pop_density))):
            return SimpleBacteria(self.birth_prob, self.death_prob)
        
        raise NoChildException()


class Patient(object):
    """
    Representation of a simplified patient. The patient does not take any
    antibiotics and his/her bacteria populations have no antibiotic resistance.
    """
    def __init__(self, bacteria, max_pop):
        """
        Args:
            bacteria (list of SimpleBacteria): The bacteria in the population
            max_pop (int): Maximum possible bacteria population size for
                this patient
        """
        self.bacteria = bacteria
        self.max_pop = max_pop

    def get_total_pop(self):
        """
        Gets the size of the current total bacteria population.

        Returns:
            int: The total bacteria population
        """
        return len(self.bacteria)

    def update(self):
        """
        Update the state of the bacteria population in this patient for a
        single time step. update() should execute the following steps in
        this order:

        1. Determine whether each bacteria cell dies (according to the
           is_killed method) and create a new list of surviving bacteria cells.

        2. Calculate the current population density by dividing the surviving
           bacteria population by the maximum population. This population
           density value is used for the following steps until the next call
           to update()

        3. Based on the population density, determine whether each surviving
           bacteria cell should reproduce and add offspring bacteria cells to
           a list of bacteria in this patient. New offspring do not reproduce.

        4. Reassign the patient's bacteria list to be the list of surviving
           bacteria and new offspring bacteria

        Returns:
            int: The total bacteria population at the end of the update
        """
        #Create new list of surviving bacteria
        survivors = []
        
        #1 Check to see which bacteria cells die and survivors to list
        for bac in self.bacteria:
            if not bac.is_killed():
                survivors.append(bac)
           
        #2 Calculate new pop_density
        pop_density = len(survivors)/self.max_pop
        
        #3 Use new pop_density to determine reproduction, offspring added to list
        newBacteria = []
        for bac in survivors:
            try:
                newBacteria.append(bac.reproduce(pop_density))
            except NoChildException:
                continue
            
        #4 Reassign patient bacteria list
        self.bacteria = survivors + newBacteria
        
        return self.get_total_pop()
            


##########################
# PROBLEM 2
##########################

def calc_pop_avg(populations, n):
    """
    Finds the average bacteria population size across trials at time step n

    Args:
        populations (list of lists or 2D array): populations[i][j] is the
            number of bacteria in trial i at time step j

    Returns:
        float: The average bacteria population size at time step n
    """
    if n > len(populations[0]): 
        raise ValueError()
    
    tot = sum([populations[x][n] for x in range(len(populations))])
    num = len(populations)
    
    return tot/num
    


def simulation_without_antibiotic(num_bacteria,
                                  max_pop,
                                  birth_prob,
                                  death_prob,
                                  num_trials):
    """
    Run the simulation and plot the graph for problem 2. No antibiotics
    are used, and bacteria do not have any antibiotic resistance.

    For each of num_trials trials:
        * instantiate a list of SimpleBacteria
        * instantiate a Patient using the list of SimpleBacteria
        * simulate changes to the bacteria population for 300 timesteps,
          recording the bacteria population after each time step. Note
          that the first time step should contain the starting number of
          bacteria in the patient

    Then, plot the average bacteria population size (y-axis) as a function of
    elapsed time steps (x-axis) You might find the make_one_curve_plot
    function useful.

    Args:
        num_bacteria (int): number of SimpleBacteria to create for patient
        max_pop (int): maximum bacteria population for patient
        birth_prob (float in [0, 1]): maximum reproduction
            probability
        death_prob (float in [0, 1]): maximum death probability
        num_trials (int): number of simulation runs to execute

    Returns:
        populations (list of lists or 2D array): populations[i][j] is the
            number of bacteria in trial i at time step j
    """
    populations = []
    y_coords = []
    
    #Iterate for each trial in num_trials
    for i in range(num_trials):
        
        #Instantiate list of Simple Bacteria
        bacteria = []
        for bac in range(num_bacteria):
            bacteria.append(SimpleBacteria(birth_prob, death_prob))
            
        #Instantiate Patient
        patient = Patient(bacteria, max_pop)
        populations.append([patient.get_total_pop()])
        
        #Run one tick
        for j in range(1, 300):
            populations[i].append(patient.update())
        
        
    #Plot after all trials
    for n in range(len(populations[0])):
        y_coords.append(calc_pop_avg(populations, n))
    
    x_coords = list(range(0,300))
    x_label = 'Timestep'
    y_label = 'Average Population'
    title = 'Without Antibiotic'
    make_one_curve_plot(x_coords, y_coords, x_label, y_label, title)
            
            
    return populations
            
    


# When you are ready to run the simulation, uncomment the next line
# populations = simulation_without_antibiotic(100, 1000, 0.1, 0.025, 50)
# print(calc_95_ci(populations, 299))
# # 95% confidence interval for population is (760.22, 4.709318393483286)

##########################
# PROBLEM 3
##########################

def calc_pop_std(populations, t):
    """
    Finds the standard deviation of populations across different trials
    at time step t by:
        * calculating the average population at time step t
        * compute average squared distance of the data points from the average
          and take its square root

    You may not use third-party functions that calculate standard deviation,
    such as numpy.std. Other built-in or third-party functions that do not
    calculate standard deviation may be used.

    Args:
        populations (list of lists or 2D array): populations[i][j] is the
            number of bacteria present in trial i at time step j
        t (int): time step

    Returns:
        float: the standard deviation of populations across different trials at
             a specific time step
    """
    mean = calc_pop_avg(populations, t)
    n = len(populations)
    diffSq = []
    
    for i in range(n):
        diffSq.append((populations[i][t] - mean)**2)
    
    stdev = np.sqrt(1/n*sum(diffSq))
    return stdev


def calc_95_ci(populations, t):
    """
    Finds a 95% confidence interval around the average bacteria population
    at time t by:
        * computing the mean and standard deviation of the sample
        * using the standard deviation of the sample to estimate the
          standard error of the mean (SEM)
        * using the SEM to construct confidence intervals around the
          sample mean

    Args:
        populations (list of lists or 2D array): populations[i][j] is the
            number of bacteria present in trial i at time step j
        t (int): time step

    Returns:
        mean (float): the sample mean
        width (float): 1.96 * SEM

        I.e., you should return a tuple containing (mean, width)
    """
    mean = calc_pop_avg(populations, t)
    stdev = calc_pop_std(populations, t)
    
    SEM = stdev/(np.sqrt(len(populations)))
    
    width = 1.96 * SEM
    
    return mean, width


##########################
# PROBLEM 4
##########################

class ResistantBacteria(SimpleBacteria):
    """A bacteria cell that can have antibiotic resistance."""

    def __init__(self, birth_prob, death_prob, resistant, mut_prob):
        """
        Args:
            birth_prob (float in [0, 1]): reproduction probability
            death_prob (float in [0, 1]): death probability
            resistant (bool): whether this bacteria has antibiotic resistance
            mut_prob (float): mutation probability for this
                bacteria cell. This is the maximum probability of the
                offspring acquiring antibiotic resistance
        """
        SimpleBacteria.__init__(self, birth_prob, death_prob)
        self.resistant = resistant
        self.mut_prob = mut_prob
        

    def get_resistant(self):
        """Returns whether the bacteria has antibiotic resistance"""
        return self.resistant

    def is_killed(self):
        """Stochastically determines whether this bacteria cell is killed in
        the patient's body at a given time step.

        Checks whether the bacteria has antibiotic resistance. If resistant,
        the bacteria dies with the regular death probability. If not resistant,
        the bacteria dies with the regular death probability / 4.

        Returns:
            bool: True if the bacteria dies with the appropriate probability
                and False otherwise.
        """
        if self.get_resistant():
            return (random.random() <= self.death_prob)

        return (random.random() <= self.death_prob/4)
    
    def reproduce(self, pop_density):
        """
        Stochastically determines whether this bacteria cell reproduces at a
        time step. Called by the update() method in the TreatedPatient class.

        A surviving bacteria cell will reproduce with probability:
        self.birth_prob * (1 - pop_density).

        If the bacteria cell reproduces, then reproduce() creates and returns
        an instance of the offspring ResistantBacteria, which will have the
        same birth_prob, death_prob, and mut_prob values as its parent.

        If the bacteria has antibiotic resistance, the offspring will also be
        resistant. If the bacteria does not have antibiotic resistance, its
        offspring have a probability of self.mut_prob * (1-pop_density) of
        developing that resistance trait. That is, bacteria in less densely
        populated environments have a greater chance of mutating to have
        antibiotic resistance.

        Args:
            pop_density (float): the population density

        Returns:
            ResistantBacteria: an instance representing the offspring of
            this bacteria cell (if the bacteria reproduces). The child should
            have the same birth_prob, death_prob values and mut_prob
            as this bacteria. Otherwise, raises a NoChildException if this
            bacteria cell does not reproduce.
        """
        if (random.random() <= (self.birth_prob * (1 - pop_density))):
            #If parent is anti resistant so is offspring
            if self.get_resistant():
                return ResistantBacteria(self.birth_prob, self.death_prob, self.resistant, self.mut_prob)
           
            #If parent not resistant, offspring has chance to be
            else:
                offHasRes = (random.random() <= (self.mut_prob * (1-pop_density)))
                return ResistantBacteria(self.birth_prob, self.death_prob, offHasRes, self.mut_prob)
        
        raise NoChildException()


class TreatedPatient(Patient):
    """
    Representation of a treated patient. The patient is able to take an
    antibiotic and his/her bacteria population can acquire antibiotic
    resistance. The patient cannot go off an antibiotic once on it.
    """
    def __init__(self, bacteria, max_pop):
        """
        Args:
            bacteria: The list representing the bacteria population (a list of
                      bacteria instances)
            max_pop: The maximum bacteria population for this patient (int)

        This function should initialize self.on_antibiotic, which represents
        whether a patient has been given an antibiotic. Initially, the
        patient has not been given an antibiotic.

        Don't forget to call Patient's __init__ method at the start of this
        method.
        """
        Patient.__init__(self, bacteria, max_pop)
        self.on_antibiotic = False

    def set_on_antibiotic(self):
        """
        Administer an antibiotic to this patient. The antibiotic acts on the
        bacteria population for all subsequent time steps.
        """
        self.on_antibiotic = True

    def get_resist_pop(self):
        """
        Get the population size of bacteria cells with antibiotic resistance

        Returns:
            int: the number of bacteria with antibiotic resistance
        """
        num_res = 0
        for bac in self.bacteria:
            if type(bac) == ResistantBacteria:
                if bac.get_resistant():
                    num_res += 1
                    
        return num_res

    def update(self):
        """
        Update the state of the bacteria population in this patient for a
        single time step. update() should execute these actions in order:

        1. Determine whether each bacteria cell dies (according to the
           is_killed method) and create a new list of surviving bacteria cells.

        2. If the patient is on antibiotics, the surviving bacteria cells from
           (1) only survive further if they are resistant. If the patient is
           not on the antibiotic, keep all surviving bacteria cells from (1)

        3. Calculate the current population density. This value is used until
           the next call to update(). Use the same calculation as in Patient

        4. Based on this value of population density, determine whether each
           surviving bacteria cell should reproduce and add offspring bacteria
           cells to the list of bacteria in this patient.

        5. Reassign the patient's bacteria list to be the list of survived
           bacteria and new offspring bacteria

        Returns:
            int: The total bacteria population at the end of the update
        """
        #Create new list of surviving bacteria
        survivors = []
        
        #1 Check to see which bacteria cells die and survivors to list
        for bac in self.bacteria:
            if not bac.is_killed():
                #2 If on antibiotics only resistant survive further
                if self.on_antibiotic:
                    if type(bac) == ResistantBacteria:
                        if bac.get_resistant():
                            survivors.append(bac)
                
                #2 Else append
                else:
                    survivors.append(bac)
                        
        #3 Calculate new pop_density
        pop_density = len(survivors)/self.max_pop
        
        #4 Use new pop_density to determine reproduction, offspring added to list
        newBacteria = []
        for bac in survivors:
            try:
                newBacteria.append(bac.reproduce(pop_density))
            except NoChildException:
                continue
            
        #5 Reassign patient bacteria list
        self.bacteria = survivors + newBacteria
        
        return self.get_total_pop()


##########################
# PROBLEM 5
##########################

def simulation_with_antibiotic(num_bacteria,
                               max_pop,
                               birth_prob,
                               death_prob,
                               resistant,
                               mut_prob,
                               num_trials):
    """
    Runs simulations and plots graphs for problem 4.

    For each of num_trials trials:
        * instantiate a list of ResistantBacteria
        * instantiate a patient
        * run a simulation for 150 timesteps, add the antibiotic, and run the
          simulation for an additional 250 timesteps, recording the total
          bacteria population and the resistance bacteria population after
          each time step

    Plot the average bacteria population size for both the total bacteria
    population and the antibiotic-resistant bacteria population (y-axis) as a
    function of elapsed time steps (x-axis) on the same plot. You might find
    the helper function make_two_curve_plot helpful

    Args:
        num_bacteria (int): number of ResistantBacteria to create for
            the patient
        max_pop (int): maximum bacteria population for patient
        birth_prob (float int [0-1]): reproduction probability
        death_prob (float in [0, 1]): probability of a bacteria cell dying
        resistant (bool): whether the bacteria initially have
            antibiotic resistance
        mut_prob (float in [0, 1]): mutation probability for the
            ResistantBacteria cells
        num_trials (int): number of simulation runs to execute

    Returns: a tuple of two lists of lists, or two 2D arrays
        populations (list of lists or 2D array): the total number of bacteria
            at each time step for each trial; total_population[i][j] is the
            total population for trial i at time step j
        resistant_pop (list of lists or 2D array): the total number of
            resistant bacteria at each time step for each trial;
            resistant_pop[i][j] is the number of resistant bacteria for
            trial i at time step j
    """
    populations = []
    resistant_pop = []
    y_coords1 = []
    y_coords2 = []
    
    #Iterate for each trial in num_trials
    for i in range(num_trials):
        
        #Instantiate list of Resistant Bacteria
        bacteria = []
        for bac in range(num_bacteria):
            bacteria.append(ResistantBacteria(birth_prob, death_prob, resistant, mut_prob))
            
        #Instantiate Patient
        patient = TreatedPatient(bacteria, max_pop)
        populations.append([patient.get_total_pop()])
        resistant_pop.append([patient.get_resist_pop()])
        
        #Run one tick for 150 timesteps
        for j in range(1, 150):
            populations[i].append(patient.update())
            resistant_pop[i].append(patient.get_resist_pop())
            
        #Add antibiotic
        patient.set_on_antibiotic()
            
        for j in range(150, 400):
            populations[i].append(patient.update())
            resistant_pop[i].append(patient.get_resist_pop())
        
        
    #Plot after all trials
    for n in range(len(populations[0])):
        y_coords1.append(calc_pop_avg(populations, n))
        y_coords2.append(calc_pop_avg(resistant_pop, n))
    
    x_coords = list(range(0,400))
    x_label = 'Timestep'
    y_label = 'Average Population'
    y_name1 = 'Total'
    y_name2 = 'Resistant'
    title = 'With an Antibiotic'
    make_two_curve_plot(x_coords,
                        y_coords1,
                        y_coords2,
                        y_name1,
                        y_name2,
                        x_label,
                        y_label,
                        title)
            
    return populations, resistant_pop


# When you are ready to run the simulations, uncomment the next lines one
# at a time
    
# total_pop, resistant_pop = simulation_with_antibiotic(num_bacteria=100,
#                                                       max_pop=1000,
#                                                       birth_prob=0.3,
#                                                       death_prob=0.2,
#                                                       resistant=False,
#                                                       mut_prob=0.8,
#                                                       num_trials=50)

# print(calc_95_ci(total_pop, 299))
# # 95% CI = (190.0, 10.091697213055888)
# print(calc_95_ci(resistant_pop, 299))
# # 95% CI = (190.0, 10.091697213055888)

###############################

total_pop, resistant_pop = simulation_with_antibiotic(num_bacteria=100,
                                                      max_pop=1000,
                                                      birth_prob=0.17,
                                                      death_prob=0.2,
                                                      resistant=False,
                                                      mut_prob=0.8,
                                                      num_trials=50)

# print(calc_95_ci(total_pop, 299))
# # 95% CI = (0.0, 0.0)
# print(calc_95_ci(resistant_pop, 299))
# # 95% CI = (0.0, 0.0)