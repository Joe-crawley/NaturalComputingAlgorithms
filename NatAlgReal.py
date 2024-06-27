#############################################################################################################
############################## DO NOT TOUCH ANYTHING UNTIL I TELL YOU TO DO SO ##############################
#############################################################################################################

# This is the skeleton program NatAlgReal.py around which you should build your implementation.
# Read all comments below carefully.

##############################
#### ENTER YOUR USER-NAME ####
##############################

username = "tpkl28"

###############################################################
#### ENTER THE CODE FOR THE ALGORITHM YOU ARE IMPLEMENTING ####
###############################################################

alg_code = "WO"

#############################################################################################################
############################## DO NOT TOUCH ANYTHING UNTIL I TELL YOU TO DO SO ##############################
#############################################################################################################

import time
import random
import math

#
# The function f is 3-dimensional and you are attempting to MINIMIZE it.
# To compute the value f(a, b, c), call the function 'compute_f(a, b, c)'.
# The variables 'f', 'a', 'b' and 'c' are reserved.
# On termination your algorithm should be such that:
#   - the reserved variable 'min_f' holds the minimum value that you have computed for the function f 
#   - the reserved variable 'minimum' is a list of length 3 holding the minimum point that you have found.
#

def compute_f(a, b, c):
    f = a**2/4000 + b**2/4000 + c**2/4000 - (math.sin(math.pi/2 + a) * math.sin(math.pi/2 + b/math.sqrt(2)) \
                                          * math.sin(math.pi/2 + c/math.sqrt(3))) + 1
    return f

#
# The ranges for the values for a, b and c are [-500, 500]. The lists below hold the minimum and maximum
# values for each a, b and c, respectively, and you should use these list variables in your code.
#

min_range = [-500, -500, -500]
max_range = [500, 500, 500]

start_time = time.time()

#############################################################################################################
########################################### ENTER YOUR CODE BELOW ###########################################
#############################################################################################################


#The notion of normal In D is the component wise abosulte value

def WhaleAddition(WhaleA,WhaleB):              #Elementwise addition of whales
    values = [0] * len(WhaleB)
    for i in range(len(WhaleB)):
        values[i] = WhaleA[i] + WhaleB[i]
    return values
def WhaleMultiplication(WhaleA,WhaleB):         #Elementwise multiplication of whales
    values = [0] * len(WhaleB)
    for i in range(len(WhaleB)):
        values[i] = WhaleA[i] * WhaleB[i]
    return values
def WhaleSubtraction(WhaleA,WhaleB):            #Elementwise subtraction of whales
    values = [0] * len(WhaleB)
    for i in range(len(WhaleB)):
        values[i] = WhaleA[i] - WhaleB[i]
    return values

test = WhaleAddition([1,2,3],[4,3,1])
def NormalOfVector(Vector):     #Calculates the normal of vector   (elementwise (sum of squares)^1/2)
    total = 0
    for item in Vector:
        total += item ** 2
    return math.sqrt(total)
def CalculateDDash(Whale,MostFitWhale):     #Calculates manhattan distance between two whales
    return WhaleSubtraction(MostFitWhale,Whale)
def CalculateD(Whale,FitWhale,C):
    step1 = WhaleSubtraction(WhaleMultiplication(C,FitWhale),Whale)     #Manhattan distance with inclusion of C (randomness)

    for i in range(len(step1)):     #Ensure absolute values of step1
        step1[i] = abs(step1[i])
    return step1



def WOA(n,N,num_cyc,b):     #N = number of wales
    Whales = [[random.uniform(-500,500) for _ in range(3)] for _ in range(N)]           #Create list of N whales with random values


    t = 1   #Initialise t
    while t <= num_cyc:     #Main loop for number of iterations
        Fitness = [compute_f(w[0], w[1], w[2]) for w in Whales]     #Calculate fitness of whales and store in list
        MostFitValue = min(Fitness)       #Store value of best whale
        MostFitWhale = Whales[Fitness.index(MostFitValue)]  #Most fit values
        stepa = float(2 / N)        #variable to store the increase of a each iteration
        a = 2 + stepa

        lStep = 0.1         #Step variable for l
        l = random.uniform(-1,1) + lStep    #l is a random value between 1 and -1



        for i in range(0,N):    #Iterate through each whale
            #update a,A,c,1,p
            a = a - stepa       #Decrease a by step variable
            A = [random.uniform(-a,a) for _ in range(3)]        #A is a vector^n with random values between (-a,a)
            C = [random.uniform(0,2) for _ in range(3)]         #C is a vector^n with random values between 0 and 2
            l = l - lStep           #Decerease l by step variable
            p = random.random()     #Random value to decide wether to encircle or bubble net attack
            if p < 0.5:
                if NormalOfVector(A) < 1:               #If normal < 1 search with most fit whale
                    #X'[i] = Max_X - dotProduct(A,D_i*)
                    Whales[i] = WhaleSubtraction(MostFitWhale,WhaleMultiplication(A,CalculateD(Whales[i],MostFitWhale,C)))     #Functions which update whale position with best whale

                else:           #else search with random whale
                    JRange = list(range(0,N))
                    JRange.remove(i)        #To avoid random whale being I'th whale
                    JWhale = Whales[random.choice(JRange)]  #chooses Whale
                    Whales[i] = WhaleSubtraction(MostFitWhale,WhaleMultiplication(A,CalculateD(Whales[i],JWhale,C)))           #Functions which update whale position with j Whale

            else:
                SpiralConstant = (math.e ** (b*l)) * math.cos(2*math.pi * l)        #Calculation required for bubblenet
                Ddash = CalculateDDash(Whales[i],MostFitWhale)          #Manhatten Distance between i'th whale and most fit whale
                for k in range(len(Ddash)):
                    Ddash[k] = Ddash[k] * SpiralConstant    #Alter Ddash vector with product of spiral constant

                Whales[i] = WhaleAddition(MostFitWhale,Ddash)

        t += 1  #Increment
    Fitness = [compute_f(w[0], w[1], w[2]) for w in Whales]     #Calculate fitness
    MostFitValue = min(Fitness)         #Most Fit Value
    MostFitWhale = Whales[Fitness.index(MostFitValue)]      #Most fit whale found by most fit value
    return MostFitWhale,MostFitValue
minimum,min_f = WOA(3,150,1100,0.01)
# total = 0
# for i in range(50):
#     minimum, min_f = WOA(3, 150, 1100, 0.01)
#     if min_f == 0.0:
#         total += 1
# print(total / 50)
    
pass
#############################################################################################################
################################## DO NOT TOUCH ANYTHING BELOW THIS COMMENT #################################
#############################################################################################################

# You should now have computed your minimum value for the function f in the variable 'min_f' and the reserved
# variable 'minimum' should hold a list containing the values a, b and c for which function f is such that
# f(a, b, c) achieves its minimum; that is, your minimum point.

now_time = time.time()
elapsed_time = round(now_time - start_time, 1)
    
error_flag = False
if type(min_f) != float and type(min_f) != int:
    print("\n*** error: you don't have a real-valued variable 'min_f'")
    error_flag = True
if type(minimum) != list:
    print("\n*** error: you don't have a tuple 'minimum' giving the minimum point")
    error_flag = True
elif len(minimum) != 3:
    print("\n*** error: you don't have a 3-tuple 'minimum' giving the minimum point; you have a {0}-tuple".format(len(minimum)))
    error_flag = True
else:
    var_names = ['a', 'b', 'c']
    for i in range(0, 3):
        if type(minimum[i]) != float and type(minimum[i]) != int:
            print("\n*** error: the value for {0} in your minimum point (a, b, c) is not numeric".format(var_names[i]))
            error_flag = True

if error_flag == False:
    print("\nYou have found a minimum value of {0} and a minimum point of [{1}, {2}, {3}].".format(min_f, minimum[0], minimum[1], minimum[2]))
    print("Your elapsed time was {0} seconds.".format(elapsed_time))


    

















    
