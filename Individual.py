from Printable import Printable

class Individual(Printable):
    """Class defining what an individual is composed of
    for our example it's going to be composed of:
    - a set of items
    - a score
    - a name ?
    """

    def __init__(self, items = [], score = 0): # Constructeur
        """Pour l'instant, on ne va définir qu'un seul attribut"""
        self.items = items
        self.score = score

    def fitness(self, sackCapacity):
        fitness = 0
        totalWeight = 0
        
        for item in self.items:
            fitness += item.value * item.weight
            totalWeight += item.weight

        # penality for exceeding sack capacity
        if totalWeight > sackCapacity:
            fitness *= 0.2

        self.score = fitness

        return self