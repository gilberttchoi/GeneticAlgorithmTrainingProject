#!/usr/bin/python3.6
# -*-coding:Utf-8 -*

import random
import numpy as np
# temporary
# using this for debugging purpose with sys.exit()
import sys

from Individual import Individual
from Item import Item

def generateSetOfItem(nbOfItems):
    setOfItems = []
    for i in range(0,nbOfItems):
        weight = random.randint(1,9)
        value = random.randint(1,19)

        setOfItems.append(Item(weight, value))
    return setOfItems


def generateIndividual(setOfItems):
    nbOfItems = len(setOfItems)
    nbOfPickedItemps = random.randint(1,nbOfItems)

    individualSetOfItems = random.sample(setOfItems, nbOfPickedItemps)
    individual = Individual(individualSetOfItems, 0)

    return individual

def generateInitialPopulation(populationSize, setOfItems):
    population = []

    for i in range(0, populationSize):
        population.append(generateIndividual(setOfItems))

    return population

# Tooling function for sorting
def takeIndividualScore(elem):
    return elem.score

def computePopulationPerf(population, sackCapacity):
    # update each individual score
    for individual in population:
        individual.fitness(sackCapacity)
        
    population.sort(key = takeIndividualScore, reverse=True)

    return population

def selectFromPopulation(populationSorted, best_sample, lucky_few):
    nextGeneration = []
    for i in range(best_sample):
        nextGeneration.append(populationSorted[i])
    for i in range(lucky_few):
        nextGeneration.append(random.choice(populationSorted))
    random.shuffle(nextGeneration)

    return nextGeneration

def createChildren(nextBreeders, number_of_child, previousGeneration):
    nextPopulation = []
    # TODO fix to handle any number of breeders and children
    for i in range(int(len(nextBreeders)/2)):
        for j in range(number_of_child):
            nextPopulation.append(createChild(nextBreeders[i], nextBreeders[len(nextBreeders) -1 -i]))
    return nextPopulation


def createChild(breeder1, breeder2):
    # Take the fittest number of items
    if (breeder1.score > breeder2.score):
        childNumberOfItems = len(breeder1.items)
    else:
        childNumberOfItems = len(breeder2.items)


    # making local copies to use pop
    breedersItems = list(breeder1.items)
    breedersItems.extend(x for x in list(breeder2.items) if x not in breedersItems)

    childItems = []
    while len(childItems) < childNumberOfItems:
        randomItem = breedersItems.pop(random.randrange(len(breedersItems)))
        childItems.append(randomItem)

    return Individual(childItems, 0)

# TOOD improve with more multiple mutations handling
def mutateIndividual(individual, setOfItems):
    
    indexModification = int(random.random() * len(individual.items))
    allowedItems = [item for item in setOfItems if item not in individual.items]
    # individual has potentially already all the items
    if allowedItems != []:
        individual.items[indexModification] = random.choice(allowedItems)
    # random addition
    if (bool(random.getrandbits(1))):
        allowedItems = [item for item in setOfItems if item not in individual.items]
        if(allowedItems != []):
            individual.items.append(random.choice(allowedItems))

    return individual

def mutatePopulation(population, chance_of_mutation, setOfItems):
    for i in range(len(population)):
        if random.random() * 100 < chance_of_mutation:
            population[i] = mutateIndividual(population[i], setOfItems)

    return population


def nextGeneration(population, sackCapacity, best_sample, lucky_few, number_of_child, chance_of_mutation, setOfItems):
    nextBreeders = selectFromPopulation(population, best_sample, lucky_few)
    nextPopulation = createChildren(nextBreeders, number_of_child, population)
    nextGeneration = mutatePopulation(nextPopulation, chance_of_mutation, setOfItems)
    population = computePopulationPerf(nextGeneration, sackCapacity)

    return population

def run():
    populationSize = 100
    sackCapacity = 20
    nbOfItems = 50

    setOfItems = generateSetOfItem(nbOfItems)

    # overload to compare to benchmark
    # OK for this one
    # test sample from this website
    # https://people.sc.fsu.edu/~jburkardt/datasets/knapsack_01/knapsack_01.html
    
    # TODO automate reading from file and compare to benchmark

    sackCapacity  = 170
    setOfItems = [Item(41, 442), Item(50, 525), Item(49,511), Item(59,593), Item(55, 546), Item(57, 564), Item(60, 617)]

    population = generateInitialPopulation(populationSize, setOfItems)
    population = computePopulationPerf(population, sackCapacity)

    # looping part
    number_of_generation = 100
    timer = 5
    best = 0
    score = 1

    generationCounter = 0
    best_sample = 20
    lucky_few = 20
    number_of_child = 5
    chance_of_mutation = 10

    # TODO create historic and display of evolution of perf

    if ((best_sample + lucky_few) / 2 * number_of_child != populationSize):
        print ("population size not stable")
    else:

        while generationCounter < number_of_generation and timer > 0:
            population = nextGeneration(population, sackCapacity, best_sample, lucky_few, number_of_child, chance_of_mutation, setOfItems)
            
            for i in range(10): 
                score += population[i].score
            score /= 10

            if int(score) == int(best):
                timer += -1
            else:
                best = score
            print("Score : ")
            print(score)
            generationCounter += 1

        print("*************")
        print("Sack Capacity")
        print(sackCapacity)
        print("Set of items")
        print(setOfItems)
        print("Nb of generation : " + str(generationCounter))
        print("Final Score : " + str(score))
        print("Final individual : ")
        print(population[0])

run()