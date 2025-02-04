from Algorithms.sharpeFitness import fitness
import numpy as np
import random
import math
import matplotlib.pyplot as plt

def GA(popSize, numPlays, generations, prices):
    chromPop = np.random.rand(numPlays+1, popSize)
    for t in range(0, popSize):
        temp = 0
        for row in range(0,numPlays+1):
            if (chromPop[row][t] < 0):
                chromPop[row][t] = -1 * chromPop[row][t]
            temp = temp + chromPop[row][t]
        for row in range(0, numPlays+1):
            chromPop[row][t] /= temp
    # GA PARAMETERS
    elitism = 0.1
    pm = 0.1 # prob. mutation
    orelax = 1.4 # over relaxation factor for mating
    epsilon = 0.07 # mutation range
    evect = np.full((numPlays+1, popSize), epsilon)
    bestFitness = 0
    data = []
    for i in chromPop.T:
        data.append(fitness(i[:numPlays], prices))
    bestFitness = max(data)
    BEST = []
    for i in range(0, generations):
        #print("GA- " + str(BEST))
        chromPop = np.array(chromPop)
        data = []
        for i in chromPop.T:
            data.append(fitness(i[:numPlays], prices))
        sorted = np.argsort(data)[::-1]
        ordered = [[0]*popSize for j in range(numPlays + 1)]
        index = 0
        for s in sorted:
            for j in range(0, numPlays+1):
                ordered[j][index] = chromPop[j][s]
            index = index + 1
        if data[sorted[0]] > bestFitness:
            bestFitness = data[sorted[0]]
            BEST = chromPop.T[sorted[0]]
        newPop = [[0]*popSize for j in range(numPlays + 1)]
        elite = int(elitism * popSize)
        # Preserve elites
        for j in range(0, elite):
            for s in range(0, numPlays + 1):
                newPop[s][j] = ordered[s][j]
        """ for col in range(0, popSize):
            print(col)
            for row in range(0, numPlays+1):
                print(chromPop[row][col]) """
        ## MUTATION
        r = np.random.normal(.5, .5, popSize)
        r2 = np.ones(popSize)
        for j in range(0, len(r)):
            if r[j] >= pm:
                r2[j] = 0
        r = r2 # mutate indices s.t. r[i] = 1
        a = chromPop - evect
        a[a<0] = 0
        b = chromPop + evect
        b[b>1] = 1
        mutations = np.zeros((numPlays+1, popSize))
        for row in range(0, numPlays+1):
            mutations[row] = r * (a[row] + (b[row]-a[row])*[np.random.rand() for _ in range(0, popSize)])
        for row in range(0, numPlays+1):
            chromPop[row] -= chromPop[row] * r
        chromPop += mutations
        ## MATING (crossover)
        permPop = chromPop.copy() # make random permutation
        for col in range(0, popSize):
            k = col + (popSize - col) * np.random.rand()
            k = int(k)
            temp = permPop[:,col].copy()
            permPop[:,col] = permPop[:,k]
            permPop[:,k] = temp
        nextGen = chromPop + orelax*(permPop - chromPop)*np.random.rand(numPlays+1, popSize)
        chromPop = nextGen
        for t in range(0, popSize):
            for s in range(0, numPlays+1):
                if chromPop[s][t] < 0:
                    chromPop[s][t] = -1 * chromPop[s][t]
            temp = sum(chromPop[:,t])
            chromPop[:,t] /= temp
        # Randomly select from modified population
        indicies = []
        for t in range(0, popSize):
            indicies.append(t)
        r = random.sample(indicies, popSize - elite)
        t = elite
        for j in r:
            for s in range(0, numPlays + 1):
                newPop[s][t] = chromPop[s][j]
            t = t + 1
        chromPop = newPop
        """ for t in range(0, popSize):
            temp = 0
            for row in range(0,numPlays+1):
                if chromPop[row][t] < 0:
                    chromPop[row][t] = -1 * chromPop[row][t]
                temp = temp + chromPop[row][t]
            for row in range(0, numPlays+1):
                chromPop[row][t] /= temp """
        #print("fitness: " + str(bestFitness))
        """ for t in range(0, popSize):
            print(chromPop[:,t])
        for t in range(0, popSize):
            print(nextGen[:][t] - chromPop[:][t]) """
    return BEST

""" if __name__ == "__main__":
    popSize = 50
    BEST = GA(popSize, 2, 100)
    time = []
    for ind in range(1, 21):
        time.append(ind)
    for best in BEST:
        plt.plot(time, best)
    plt.show() """