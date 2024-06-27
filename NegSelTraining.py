#############################################################################################################
############################## DO NOT TOUCH ANYTHING UNTIL I TELL YOU TO DO SO ##############################
#############################################################################################################

# This is the skeleton program NegSelTraining.py around which you should build your implementation.
#
# The training set should be in a file self_training.txt.
#
# The output is a detector set that is in the file detector_<timestamp>.txt where <timestamp> is a timestamp
# so that you do not overwrite previously produced detector sets. You can always rename these files.
#
# It is assumed that NegSelTraining.py and self_training.txt are in the same folder.

##############################
#### ENTER YOUR USER-NAME ####
##############################

username = "tpkl28"

###############################################################
#### ENTER THE CODE FOR THE ALGORITHM YOU ARE IMPLEMENTING ####
###############################################################

alg_code = "VD"

############################################################################################
#### ENTER THE THRESHOLD: IF YOU ARE IMPLEMENTING VDETECTOR THEN SET THE THRESHOLD AS 0 ####
############################################################################################

threshold = 0

######################################################
#### ENTER THE INTENDED SIZE OF YOUR DETECTOR SET ####
######################################################

num_detectors = 1000

#############################################################################################################
############################## DO NOT TOUCH ANYTHING UNTIL I TELL YOU TO DO SO ##############################
#############################################################################################################

import time
import os.path
import random
import math
import sys


def get_a_timestamp_for_an_output_file():
    local_time = time.asctime(time.localtime(time.time()))
    timestamp = local_time[4:7] + local_time[8:10] + local_time[11:13] + local_time[14:16] + local_time[17:19]
    timestamp = timestamp.replace(" ", "0")
    return timestamp


def read_points(f, point_length, num_points, file):
    list_of_points = []
    count = 0
    error = ""
    the_line = f.readline()
    while the_line != "":
        points = the_line.split("[")
        points.pop(0)
        how_many = len(points)
        for i in range(0, how_many):
            if points[i][len(points[i]) - 1] == ",":
                points[i] = points[i][0:len(points[i]) - 2]
            elif points[i][len(points[i]) - 1] == "\n":
                points[i] = points[i][0:len(points[i]) - 3]
            else:
                points[i] = points[i][0:len(points[i]) - 1]
            split_point = points[i].split(",")
            if len(split_point) != point_length:
                error = "\n*** error: a point number has the wrong length\n"
                return list_of_points, error
            numeric_point = []
            for j in range(0, point_length):
                numeric_point.append(float(split_point[j]))
            list_of_points.append(numeric_point[:])
            count = count + 1
        the_line = f.readline()
    if count != num_points:
        error = "\n*** error: there should be " + str(num_points) + " points in " + file + " but there are " + str(
            count) + "\n"
    return list_of_points, error


self_training = "self_training.txt"

if not os.path.exists(self_training):
    print("\n*** error: " + self_training + " does not exist\n")
    sys.exit()

f = open(self_training, "r")

self_or_non_self = f.readline()
if self_or_non_self != "Self\n":
    print("\n*** error: the file " + self_training + " is not denoted as a Self-file\n")
    f.close()
    sys.exit()
dim = f.readline()
length_of_dim = len(dim)
dim = dim[len("dimension = "):length_of_dim - 1]
n = int(dim)
num_points = f.readline()
length_of_num_points = len(num_points)
num_points = num_points[len("number of points = "):length_of_num_points - 1]
Self_num_points = int(num_points)

list_of_points, error = read_points(f, n, Self_num_points, self_training)
Self = list_of_points[:]

f.close()

if error != "":
    print(error)
    sys.exit()

# The training data has now been read into the following reserved variables:
#   - 'n' = the dimension of the points in the training set
#   - 'Self_num_points' = the number of points in the training set
#   - 'Self' = the list of points in the training set
# These are reserved variables and their names should not be changed.

# The list of detectors needs to be stored in the variable 'detectors'. This is a reserved variable
# and is initialized below. You need to ensure that your computed detector set is stored in 'detectors'
# as a list of points, i.e., as a list of lists-of-reals-of-length-'n' for NS and RV and 'n' + 1 for VD
# (remember: a detector for VD is a point plus its individual radius - see Lecture 4).

detectors = []

start_time = time.time()


#############################################################################################################
########################################### ENTER YOUR CODE BELOW ###########################################
#############################################################################################################

def EucilidianDistance(Dimension, x, y):
    Dimension = int(Dimension)
    distance = 0
    for i in range(0, Dimension):
        distance += (x[i] - y[i]) ** 2
    distance = math.sqrt(distance)
    return distance


def DistanceBetwenVDetectors(x, y, dimension):
    # 2dimension means a vdetector has [a,b,c] where c is the radius
    distance = 0.0
    for i in range(0, dimension):
        distance += (x[i] - y[i]) ** 2

    return math.sqrt(distance)


##DetectorData [1,...n,radius]
# C0: expected coverage rate for non-Selfs
# C1: expected coverage rate for Selfs
# Rs: Self Radius
# N: Number of Detectors
# S: The set of Self training nodes
# The smaller self radius would result in high detection rate but high false alarm rate too
def VDetector(S, c0, c1, Rs, N):
    Detectors = []  #Initilise detector set
    t1 = 0  #Initilise t1
    c0Constant = int(1 / (1 - c0))      #Save constants for expected coverages
    c1Constant = int(1 / (1 - c1))
    while len(Detectors) < N:   #Loop to control the amount of detectors
        t0 = 0      #Initiilise t0
        PhaseOneFlag = False    #Set Phase one flag to false
        while PhaseOneFlag == False:    #Phaseone loop
            RandomIndividual = [random.random() for i in range(int(dim))]   #create a random individual with random location
            RandomIndividual.append(math.inf)       #Set radius to infinity
            PhaseOneFlag = True #set phase one flag to True
            for d in Detectors: #Iterate through detector set
                if DistanceBetwenVDetectors(d, RandomIndividual, int(dim)) <= d[-1]:    #Calculate distance between random detector and existing detector d
                    t0 += 1     #Increment t0
                    if t0 >= c0Constant:    #If coverage is met return detector set
                        print("C0")
                        return Detectors
                    PhaseOneFlag = False
                    break
            if PhaseOneFlag == True:        #Phase one complete
                for s in S:         #iterate through training nodes
                    DistanceValue = DistanceBetwenVDetectors(s, RandomIndividual, int(dim)) - Rs        #Calculate distance between training node - self radius
                    if DistanceValue < RandomIndividual[-1]:        #If calculated distance is less then new individual radius
                        RandomIndividual[-1] = DistanceValue        #update new individual radius
                if RandomIndividual[-1] > Rs:       #If new individual radius exceeds self radius
                    Detectors.append(RandomIndividual)      #Add new individual to detector set
                else:
                    t1 += 1         #increment t1
                if t1 >= c1Constant:        #If adequate coverage is made return detector set
                    print("C1")
                    return Detectors
    print("MAXDetector")
    return Detectors

    # 0.94,9.99999,0.01


detectors = VDetector(Self, 0.9995, 0.9995, 0.009, int(num_detectors))
# def NSA(S,r,N):
#     #S = self, r = radius of detector, N = num of detectors
#     Detectors = []
#     while len(Detectors) < N:
#         RandomIndividual = [random.random() for i in range(int(dim))]
#         Flag = False
#         for s in S:
#             distance = EucilidianDistance(dim,s,RandomIndividual)
#             if distance < r:
#                 Flag = True
#         if Flag == False:
#             Detectors.append(RandomIndividual)
#     return Detectors

# detectors = NSA(Self,threshold,num_detectors)
# pass


#############################################################################################################
################################## DO NOT TOUCH ANYTHING BELOW THIS COMMENT #################################
#############################################################################################################

now_time = time.time()
training_time = round(now_time - start_time, 1)

timestamp = get_a_timestamp_for_an_output_file()
detector_set = "detector_" + timestamp + ".txt"

f = open(detector_set, "w")

f.write("username = {0}\n".format(username))
f.write("detector set\n")
f.write("algorithm = {0}\n".format(alg_code))
f.write("dimension = {0}\n".format(n))
if alg_code != "VD":
    f.write("threshold = {0}\n".format(threshold))
else:
    f.write("self-radius = {0}\n".format(threshold))
num_detectors = len(detectors)
f.write("number of points = {0}\n".format(num_detectors))
f.write("training time = {0}\n".format(training_time))
detector_length = n
if alg_code == "VD":
    detector_length = n + 1
for i in range(0, num_detectors):
    f.write("[")
    for j in range(0, detector_length):
        if j != detector_length - 1:
            f.write("{0},".format(detectors[i][j]))
        else:
            f.write("{0}]".format(detectors[i][j]))
            if i == num_detectors - 1:
                f.write("\n")
            else:
                f.write(",\n")
f.close()


















