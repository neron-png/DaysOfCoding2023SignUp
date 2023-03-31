def run(test_case):
    #User input
    try:
        params = test_case.split("\n")
        print(params)
        n = int(params[0])
        m = int(params[1])
        rotation_char = params[2]
        arr = params[3].split(",")
    except Exception as e:
        return "Error on input. example input: 3\n2\nL\nO,X,O,X,O,X"
    # n = int(input("Give n:"))
    # m = int(input("Give m:"))
    # rotation_char = input("Give rotation:")
    # arr = list(input("Give array:").split(","))


    rotarr = []

    if rotation_char == "L":  # left rotation
        for i in range(n):
            for j in range(1,m+1):
                rotarr.append(arr[n*j-1-i])


    if rotation_char == "R":  # right rotation
        for i in range(n):
            for j in range(m-1,-1,-1):
                rotarr.append(arr[n*j+i])


    for i in range(n-1):
        for j in range(len(rotarr) - m):  # Last row does not need to be checked
            if rotarr[j] == "O" and rotarr[j+m] == "X":   # compare each element with the one below it
                rotarr[j] = "X"
                rotarr[j+m] = "O"
                # swap the elements if gravity needs to be applied
    return rotarr

