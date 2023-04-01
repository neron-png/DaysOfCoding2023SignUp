def print_array(arr: list, x: int, y: int):
    """print the array in a readable format"""

    counter = 0
    for i in range(x):
        if i != 0:
            print("")
        for k in range(y):
            print(arr[counter], end=" ")
            counter += 1
    print("")


# HOW THIS CODE RUNS IS BETWEEN ME AND GOD AND A PIDGEON
def contagion(arr: list, k: int):
    """Implements  one day of contagion. Mutates the array itself and prints each cycle.
    Assumes all contaminated cities are the cells with negative integers, and comparisons are done on
    absolute values."""

    for i in range(5):
        for j in range(5):
            if i != 0 and arr[i * 5 + j] == -k and k > arr[(i - 1) * 5 + j] and arr[(i - 1) * 5 + j] >= 0:
                arr[(i - 1) * 5 + j] *= -1
            if i != 4 and arr[i * 5 + j] == -k and k > arr[(i + 1) * 5 + j] and arr[(i + 1) * 5 + j] >= 0:
                arr[(i + 1) * 5 + j] *= -1
            if j != 0 and arr[i * 5 + j] == -k and k > arr[i * 5 + (j - 1)] and arr[i * 5 + j - 1] >= 0:
                arr[i * 5 + (j - 1)] *= -1
            if j != 4 and arr[i * 5 + j] == -k and k > arr[i * 5 + (j + 1)] and arr[i * 5 + j + 1] >= 0:
                arr[i * 5 + (j + 1)] *= -1

    for i in range(5):
        for j in range(5):
            if arr[i * 5 + j] < 0:
                arr[i * 5 + j] = -k
            else:
                arr[i * 5 + j] += 2


# HOW THIS CODE RUNS IS BETWEEN ME AND GOD (AND A PIDGEON)
def contagion_bonus(arr: list):
    """makes the conversion from arr ->array where array is a 2 dimensional matrix, for convenience. We use a second array called check_contagion
to store data about cells to apply the changes all at once. Each positive cell is checked against its neighbours to apply the largest ifection(if
there is any) and each negative cell is checked to see if it can be cured by a neighbor."""
    array = []
    check_contagion = []
    for j in range(5):
        array.append([arr[i] for i in range((j * 5), (j * 5) + 5)])
        check_contagion.append([0 for i in range(5)])
    for i in range(5):
        for j in range(5):

            if array[i][j] >= 0:  # for every non infected, check the neighbors and mark infected if needed
                cont = 100
                if i != 0:
                    cont = min(cont, array[i - 1][j])
                if i != 4:
                    cont = min(cont, array[i + 1][j])
                if j != 0:
                    cont = min(cont, array[i][j - 1])
                if j != 4:
                    cont = min(cont, array[i][j + 1])
                # print(array[i][j],cont)
                if cont < 0 and abs(cont) > array[i][j]:
                    check_contagion[i][j] = cont  # marks all cells that will be infected later

            else:
                if i != 0:
                    if array[i - 1][j] >= abs(array[i][j] * 2):
                        check_contagion[i][j] = abs(array[i][j])
                if i != 4:
                    if array[i + 1][j] >= abs(array[i][j] * 2):
                        check_contagion[i][j] = abs(array[i][j])
                if j != 0:
                    if array[i][j - 1] >= abs(array[i][j] * 2):
                        check_contagion[i][j] = abs(array[i][j])
                if j != 4:
                    if array[i][j + 1] >= abs(array[i][j] * 2):
                        check_contagion[i][j] = abs(array[i][j])
            # print(array[i][j],cont)

    arr = []
    for i in range(5):
        for j in range(5):
            if check_contagion[i][j] == 0:
                array[i][j] += (2 if array[i][j] > 0 else 0)
            else:
                array[i][j] = check_contagion[i][j]
            arr.append(array[i][j])

    return arr


def run(array_str):
    try:
        wrong_input = 0
        infected = 0
        running_arr = array_str.split(',')
        running_arr = [int(x) for x in running_arr]  # cast to int
        for city in running_arr:
            if city > 99:
                wrong_input = 1
            if city < 0:
                infected += 1
        if infected > 1 or wrong_input or len(running_arr) > 25:
            return "Wrong Input! Please notice that the input must be a string of 25 integers splitted with comma ' , ' .Here is an acceptable input: 5,7,3,8,9,4,-10,5,10,7,54,5,8,0,3,5,6,2,5,7,4,4,21,4,8" \
                   " .Please make sure you follow the problems instructions"
        contagion_level = 0
        for i in running_arr:
            if i < 0:
                contagion_level = i
        for i in range(5):
            contagion(running_arr, contagion_level * (-1))
        return str(running_arr)[1:-1]
    except Exception:
        return "Wrong Input! Please notice that the input must be a string of 25 integers splitted with comma ' , ' .Here is an acceptable input: 5,7,3,8,9,4,-10,5,10,7,54,5,8,0,3,5,6,2,5,7,4,4,21,4,8" \
               " .Please make sure you follow the problems instructions"
