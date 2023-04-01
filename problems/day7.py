# CIPHER PROBLEM

alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U",
            "V", "W", "X", "Y", "Z"]
rearranged_alphabet = alphabet.copy()


def alphabet_rotation(shift, letter):
    rotation = ""
    global rearranged_alphabet

    if shift >= 0:
        shift_amount = shift % 26
        rotation = "right"
    else:
        shift_amount = abs(shift) % 26
        rotation = "left"

    if rotation == "left":
        rearranged_alphabet = rearranged_alphabet[shift_amount:] + rearranged_alphabet[:shift_amount]
    elif rotation == "right":
        rearranged_alphabet = rearranged_alphabet[-shift_amount:] + rearranged_alphabet[:-shift_amount]
    # print(rearranged_alphabet)

    index = 0
    for i in range(0, 26):
        if alphabet[i] == letter:
            index = i
    encrypted_letter = rearranged_alphabet[index]

    return encrypted_letter


def run(arg):
    correct_input = True
    data = arg.split(",")

    shift = ""
    step = ""
    message = ""

    try:
        shift = int(data[1])
        step = int(data[2])
        message = data[0]
    except Exception:
        correct_input = False

    for i in message:
        if not (("A" <= i <= "Z") or i == " "):
            correct_input = False
            break


    if not correct_input:
        return "Wrong Input! Example of acceptable input: HELLO WORLD,5,2 "

    encrypted_message = ""
    for letter in message:
        if alphabet.count(letter) == 1:
            encrypted_message += alphabet_rotation(shift, letter)
            shift += step
        else:
            encrypted_message += letter

    global rearranged_alphabet
    rearranged_alphabet = alphabet.copy()


    return encrypted_message

