

#Author Apostolos Halis, Paulos Daratzis 2023
import sys
import math


def run(arguments):
    
    output = ""
    try:
        # parsing CLI arguments args = sys.argv[1:]
        args = arguments
        # values = list(map(str, args[0:]))
        values = args.split(" ")
        blackHoles = []  # I will save the coordinates of all black holes in this array
        # it is 1D because it is much easier to handle and in the end of the day
        # every two numbers you get a coordinate
        planets = [] # Same logic applies here but for planets
        absorbedPlanets = [] # coordinate of the planets that will be absorbed by the black holes
        savedPlanets = []
        planetsInGoldilocks = []
        blackHole_and_affectedPlanets = []
        affected = []
        stars = []
        rows = int(math.sqrt(len(values)))
        cols = int(math.sqrt(len(values)))
        universe = [[0 for j in range(cols)] for i in range(rows)]

        for i in range(rows):
            for j in range(cols):
                k = i * cols + j
                universe[i][j] = values[k]

        # printing out the 2d array (Only for testing purposes)
        # print("\n")
        # for i in range(rows):
            # for j in range(cols):
                # print(universe[i][j], end=' ')
            # print()

        # problem 1
        # get positions of all black holes
        for i in range(rows):
            for j in range(cols):
                if universe[i][j] == "o":
                    blackHoles.append(i)
                    blackHoles.append(j)

        # get positions of all planets
        for i in range(rows):
            for j in range(cols):
                if universe[i][j] == "x":
                    planets.append(i)
                    planets.append(j)

        # print("Black holes: ", blackHoles) # Testing (should remove later)
        # print("Planets: ", planets) # Testing (should remove later)

        # For every black hole we check the proximity of every planet, if the planet is close to 2 cells we add the planet to
        # the absorbedPlanets list
        # NOTE: I am using an 1D array, that's why we need to add + 1 to get the collumn of the planet
        for i in range(0, len(blackHoles), 2):
            for j in range(0, len(planets), 2):
                if blackHoles[i] - 2 <= planets[j] <= blackHoles[i] + 2 and blackHoles[i + 1] - 2 <= planets[j + 1] <= blackHoles[i +1] +2:
                    absorbedPlanets.append((planets[j], planets[j + 1]))
                    # absorbedPlanets.append(planets[j + 1]) # example of what I mean by saying + 1 to get the collumn
                else:
                    savedPlanets.append((planets[j], planets[j + 1]))
                    # savedPlanets.append(planets[j + 1])

        output += f"Absorbed planets: {absorbedPlanets}"
        output += f"\nSaved planets: {savedPlanets}"
        # print("Absorbed planets: ", absorbedPlanets) # Result
        # print("Saved planets: ", savedPlanets) # Result

        # problem 2
        for i in range(rows):
            for j in range(cols):
                if universe[i][j] == 'z':
                    n = len(universe)
                    # check cells 2 steps up, down, left, and right
                    if i >= 2 and universe[i - 2][j] == 'x':
                        planetsInGoldilocks.append((i - 2, j))
                    if i <= n - 3 and universe[i + 2][j] == 'x':
                        planetsInGoldilocks.append((i + 2, j))
                    if j >= 2 and universe[i][j - 2] == 'x':
                        planetsInGoldilocks.append((i, j - 2))
                    if j <= n - 3 and universe[i][j + 2] == 'x':
                        planetsInGoldilocks.append((i, j + 2))

        # print("Planets that are in the Golidlocks zone: ",planetsInGoldilocks)
        output += f"\nPlanets that are in the Golidlocks zone: {planetsInGoldilocks}"

        # print("out")
        # if __name__ == "__main__":
            # problem 3
            # if we want to find the affected planets of every black hole we first need find the planets that will be affected,
            # thankfully we got an array for this job called absorbedPlanets, but before we check that we need to make sure the two
            # blackholes do not overlap
            # planetsAffected = 0

            # if len(blackHoles) > 2: # there is not use for this piece of code if there is one black hole
                # for i in range(0, len(blackHoles), 2):
                    # for j in range(i + 2, len(blackHoles), 2):
                        # bhRow1 = blackHoles[i]
                        # bhRow2 = blackHoles[j]
                        # bhCol1 = blackHoles[i + 1]
                        # bhCol2 = blackHoles[j + 1]
                        # if abs(bhRow1 - bhRow2) <= 2 and abs(bhCol1 - bhCol2) <= 2:
                            # print(abs(bhRow1 - bhRow2), abs(bhCol1 - bhCol2))
                            # print("Error: Black holes are overlapping!")
                            # exit()

            # now we will check if what black holes affects what planet
            # for i in range(0, len(blackHoles),2):
                # for j in range(0, len(absorbedPlanets), 2):
                    # if blackHoles[i] - 2 <= absorbedPlanets[j] <= blackHoles[i] + 2 and blackHoles[i + 1] - 2 <= absorbedPlanets[j + 1] <= blackHoles[i + 1] + 2:
                        # print("Planet: ", absorbedPlanets[j], absorbedPlanets[j + 1], "Was absorbed by blackhole: ", blackHoles[i], blackHoles[i + 1])
                        # planetsAffected+=1

            # amountOfBlackHoles = len(blackHoles) / 2
            # avgPlanetsAfected = planetsAffected / amountOfBlackHoles
            # print("Every black hole affects " , avgPlanetsAfected, " on average.")

    except Exception as e:
        output = "Input error: Here's an example of a working input: 0 0 0 0 0 0 0 0 x 0 0 0 x 0 0 z o 0 0 0 0 z 0 0 x 0 0 0 0 0 0 0 0 0 0 0 0 x x 0 x 0 0 z 0 0 z 0 o 0 x 0 0 0 x 0 z 0 0 0 0 0 x z"
    
    return output

