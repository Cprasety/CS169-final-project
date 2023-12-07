import random
import numpy as np
import math

def PrintSudoku(sudoku):
    print("\n")
    for i in range(len(sudoku)):
        line = ""
        if i == 3 or i == 6:
            print("---------------------")
        for j in range(len(sudoku[i])):
            if j == 3 or j == 6:
                line += "| "
            line += str(sudoku[i, j]) + " "
        print(line)


def CreateList3x3Blocks():
    finalListOfBlocks = []
    for r in range(0, 9):
        tmpList = []
        block1 = [i + 3 * ((r) % 3) for i in range(0, 3)]
        block2 = [i + 3 * math.trunc((r) / 3) for i in range(0, 3)]
        for x in block1:
            for y in block2:
                tmpList.append([x, y])
        finalListOfBlocks.append(tmpList)
    return (finalListOfBlocks)


def number_of_error(sudoku):

    noe = 0
    for i in range(len(sudoku)):
        noe += (9 - len(np.unique(sudoku[:, i]))) + (9 - len(np.unique(sudoku[i, :])))
    return noe

def CalculateNumberOfErrorsRowColumn(row, column, sudoku):
    numberOfErrors = (9 - len(np.unique(sudoku[:,column]))) + (9 - len(np.unique(sudoku[row,:])))
    return(numberOfErrors)

def fill_initial_grid(sudoku):
    list_of_blocks = CreateList3x3Blocks()
    for block in list_of_blocks:
        list_of_nine = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for cordinate in block:
            row, col = cordinate
            if (sudoku[row][col] != 0):
                list_of_nine.remove(sudoku[row][col])
        for cordinate in block:
            row, col = cordinate
            if (sudoku[row, col] == 0):
                random_value = random.choice(list_of_nine)
                sudoku[row][col] = random_value
                list_of_nine.remove(random_value)

    return sudoku;


def FixSudokuValues(fixed_sudoku):
    for i in range(0, 9):
        for j in range(0, 9):
            if fixed_sudoku[i, j] != 0:
                fixed_sudoku[i, j] = 1

    return (fixed_sudoku)

def SumOfOneBlock(sudoku, oneBlock):
    finalSum = 0
    for box in oneBlock:
        finalSum += sudoku[box[0], box[1]]
    return (finalSum)

def flip_two_numbers(sudoku, locked_sudoku):
    copy = np.copy(sudoku)
    list_of_blocks = CreateList3x3Blocks()
    locked_squres = locked_sudoku
    list_of_nine = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    random_value = random.choice(list_of_nine)
    if(SumOfOneBlock(sudoku,list_of_blocks[random_value]) > 6):
        random_value = random.choice(list_of_nine)
    second_random_value = random.choice(list_of_nine)
    third_random_value = random.choice(list_of_nine)

    row, col = list_of_blocks[random_value][second_random_value]
    row2, col2 = list_of_blocks[random_value][third_random_value]

    while (locked_squres[row][col] == 1):
        second_random_value = random.choice(list_of_nine)
        row, col = list_of_blocks[random_value][second_random_value]
    while (locked_squres[row2][col2] == 1):
        third_random_value = random.choice(list_of_nine)
        row2, col2 = list_of_blocks[random_value][third_random_value]

    value1 = sudoku[row][col]
    value2 = sudoku[row2][col2]

    copy[row][col] = value2
    copy[row2][col2] = value1

    return copy




def simulated_annealing(sudoku):

    copy = np.copy(sudoku)

    locked_sudoku = FixSudokuValues(copy)
    initial_temperature = 10
    stuckCount = 0

    iterations = 1


    fill_initial_grid(sudoku)

    current_error_number = number_of_error(sudoku)
    current_sudoku = np.copy(sudoku)

    while current_error_number != 0:

        previous_noe = current_error_number

        proposed_state = flip_two_numbers(current_sudoku, locked_sudoku)
        proposed_error_number = number_of_error(proposed_state)
        acceptance_probability = np.exp(
                -(proposed_error_number - current_error_number) / (
                        initial_temperature/iterations))
        if proposed_error_number < previous_noe or  random.random() < acceptance_probability:
            current_sudoku = proposed_state
            current_error_number = proposed_error_number

        if current_error_number == 0:
            # PrintSudoku(current_sudoku)
            return number_of_error(current_sudoku), iterations
            break

        iterations += 1


        if current_error_number >= previous_noe:
            stuckCount += 1
        else:
            stuckCount = 0
        if (stuckCount > 250):
            initial_temperature += 20






