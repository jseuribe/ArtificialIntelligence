#!/usr/bin/python

import random
import collections
import math
import sys
from collections import Counter
from util import *

############################################################
# Problem 2: binary classification
############################################################

def sparseVectorDotProduct(v1, v2):
    return sum([v1[i] * v2[i] for i in v1 & v2])

############################################################
# Problem 2a: feature extraction

def extractWordFeatures(x):
    strlist = x.split()
    featureVector = {}

    for word in strlist:
        if word in featureVector:
            featureVector[word] += 1
        elif not word in featureVector:
            featureVector[word] = 1

    return featureVector

############################################################
# Problem 2b: stochastic gradient descent

def learnPredictor(trainExamples, testExamples, featureExtractor):
    weights = {}
    numIters = 1
    trainingCorrect = 0
    testingCorrect = 0
    eta = 10

    for t in range(0, numIters):
     for i in range(0, len(trainExamples)):
            currentString = collections.Counter(featureExtractor((trainExamples[i][0]))) #We have our featurevector here. This will be the relevant updates

            for j in currentString:
                if j not in weights:
                    weights[j] = 0

            weightList = collections.Counter(weights)#our weightList vector
            print(weightList)

            prediction = sparseVectorDotProduct(weightList, currentString)
            margin = prediction * trainExamples[i][1]

            if margin < 1:
                print("We'll be using -y times phi")
                for j in currentString:
                    weights[j] -= (eta * ( -(trainExamples[i][1]) * currentString[j]))
            elif margin > 1:
                print("A prediction was correct!")
                trainingCorrect += 1
            elif margin == 1:
                print("We'll be using 0; no change")


     for i in range(0,len(testExamples)):
         currentString = collections.Counter(featureExtractor((testExamples[i][0]))) #We have our featurevector here. This will be the relevant updates

         weightList = collections.Counter(weights)#our weightList vector

         prediction = sparseVectorDotProduct(weightList, currentString)
         margin = prediction * testExamples[i][1]

         if margin < 1 or margin == 1:
            print("Incorrect prediction...")
         elif margin > 1:
             print("A prediction was correct!")
             testingCorrect += 1


     print("Training Error: ")
     print(trainingCorrect/len(trainExamples))
     print("Testing Error: ")
     print(testingCorrect/len(testExamples))
     return weights

############################################################
# Problem 2c: generate test case

def generateDataset(numExamples, weights):
    '''
    Return a set of examples (phi(x), y) randomly which are classified correctly by
    |weights|.
    '''
    random.seed(42)
    # Return a single example (phi(x), y).
    # phi(x) can be anything (randomize!) with a nonzero score under the given weight vector
    # y should be 1 or -1 as classified by the weight vector.
    def generateExample():
        phi = ""
        randomWord = ""
        y = 0
        # BEGIN_YOUR_CODE (around 5 lines of code expected)
        for i in range(0, random.randint(0,len(weights))):
            randomWord = random.choice(list(weights.keys()))
            phi = phi + randomWord
            y += weights[randomWord]
        if y < 0: y = -1
        elif y > 0: y = 1
        return (phi, y)
    return [generateExample() for _ in range(numExamples)]

############################################################
# Problem 2f: n-gram features

def extractNgramFeatures(n):
    '''
    Return a function that takes a string |x| and returns a sparse feature
    vector consisting of all 1,2,3,...,n-grams of |x| without spaces.
    EXAMPLE: (n = 3) "I like tacos" --> {'I': 1, 'like': 1, 'tacos': 1, 'I like': 1, 'like tacos': 1, 'I like tacos' : 1}
    EXAMPLE: (n = 3) "not good. This movie not good" ->
    '''
    def extract(x):
        # BEGIN_YOUR_CODE (around 10 lines of code expected)
        startpt = 0
        theList = list()
        for i in range(n,len(x)+1):
            if ' ' not in x[startpt:i]:
                theList.append(x[startpt:i])
            startpt += 1
        return theList

        # END_YOUR_CODE
    return extract

############################################################
# Problem 2h: extra credit features

def extractExtraCreditFeatures(x):
    strlist = x.split()
    featureVector = {}

    for word_count, word in enumerate(strlist):
        if word in featureVector and "tion" in word:
            featureVector[strlist[word_count -1 ] + " " + word] += 1
            featureVector[word] += 1
        elif not word in featureVector and "tion" in word:
            featureVector[strlist[word_count - 1] + " " + word] = 1
            featureVector[word] = 1

    return featureVector

############################################################
# Problem 3: k-means
############################################################


def calcEuclid(x1, x2):
    x = math.sqrt(math.pow((x1[0] - x2[0]), 2) + math.pow((x1[1] - x2[1]), 2))
    return x

def kmeans(examples, K, maxIters):
    '''
    examples: list of examples, each example is a string-to-double dict representing a sparse vector.
    K: number of desired clusters
    maxIters: maximum number of iterations to run for (you should terminate early if the algorithm converges).
    Return: (length K list of cluster centroids,
            list of assignments, (i.e. if examples[i] belongs to centers[j], then assignments[i] = j)
            final reconstruction loss)
    '''
    # BEGIN_YOUR_CODE (around 35 lines of code expected)
    random.seed(622)

    cluster_map = list()
    pastCenters = list()
    past_mapping = list()
    past_distances = list()

    centers = list()
    convergent = False
    recon_Loss = 0.0

    test_dict1 = {0: 1, 1: 2}
    test_dict2 = {0: 1, 1:2}

    rand_center = {}
    #for k in range(K):
    #   create new _center_ randomly
    #   while New_center is already in centers:
    #       create new_center
    #   insert new_center into centers

    rand_center = random.choice(examples)

    for k in range(K):
        while rand_center in centers:
            rand_center = random.choice(examples)
        centers.append(rand_center)

    #print 'original centers: ', centers

    current_iter = 0
    while not convergent and current_iter is not maxIters:  # Obtain k random centers.
        recon_Loss = 0.0
        print 'new iteration!'
        for example_num, example in enumerate(examples):
            for center_num, center in enumerate(centers):

                current_val = calcEuclid(example, center)

                if len(past_distances) <= example_num:
                    past_distances.append(current_val)
                    cluster_map.append(center_num)
                elif current_val <= past_distances[example_num]:
                    print 'euclidean distance of ', example, ' from ', center, ' is ', current_val, 'and is therefore in cluster: ', center_num
                    past_distances[example_num] = current_val
                    cluster_map[example_num] = center_num
                    recon_Loss += 1

        #Step 2: Now compute the new centroids.
        # for every index in cluster_map:
        #   for every example:
        #       center_x, center_y = 0
        #       center_x = example[index][0]
        #       center_y = example[index][1]
        #       center[example[index]][0] = center_x
        #       center[example[index]][1] = center_y

        new_centers_x = {}
        new_centers_y = {}

        for index in range(0, len(cluster_map)):
            if cluster_map[index] not in new_centers_x:
                new_centers_x[cluster_map[index]] = 0.0

            if cluster_map[index] not in new_centers_y:
                new_centers_y[cluster_map[index]] = 0.0

            new_centers_x[cluster_map[index]] += examples[index][0]
            new_centers_y[cluster_map[index]] += examples[index][1]

        print 'past mapping is: ', past_mapping, ' and current mapping is: ', cluster_map
        if not past_mapping:
            convergent = False
        else:
            convergent = past_mapping == cluster_map
        past_mapping = cluster_map
        pastCenters = list(centers)
        #print 'past centers:', pastCenters

        #Calculate the true average...by assigning the center the new value obtained from above
        # The new centroids are obtained by doing: (sum_x/avg_x, sum_y/avg_y)
        new_center = {}
        for center_num, center in enumerate(centers):
            new_center[0] = new_centers_x[center_num]/cluster_map.count(center_num)
            new_center[1] = new_centers_y[center_num]/cluster_map.count(center_num)
            centers[center_num] = new_center

        current_iter += 1


    print centers, cluster_map, recon_Loss
    return centers, cluster_map, recon_Loss

    #print 'Cluster map: ', cluster_map, ' New centers: ', centers, ' Previous centers: ', pastCenters
    #print 'total loss: ', recon_Loss
