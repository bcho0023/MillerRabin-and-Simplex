"""
Name: Brian Choo Way Yip
Student_Id: 31056334
"""

import sys
import numpy


def simplex(objective, constraintsLHS, constraintsRHS):
    numVar = len(objective)
    numConst = len(constraintsLHS)

    CjZj = [0] * (numVar + numConst)
    RHS = numpy.array(constraintsRHS[:], dtype=float)

    Cj = [0] * (numVar + numConst)
    for i in range(numVar):
        Cj[i] = objective[i]

    basic = list(range(numVar, numConst + numVar))
    basic_coefficient = [0] * len(basic)
    for i in range(len(basic)):
        basic_coefficient[i] = Cj[basic[i]]
    # print("Basic", basic)

    # Construct Initial Matrix
    matrix = []
    for i in range(numVar):
        matrix_lst = [0] * numConst

        for j in range(len(constraintsLHS)):
            matrix_lst[j] = constraintsLHS[j][i]

        matrix.append(numpy.array(matrix_lst, dtype=float))

    for i in range(numConst):
        matrix_lst = [0] * numConst

        matrix_lst[i] = 1

        matrix.append(numpy.array(matrix_lst, dtype=float))
    # print(matrix)

    # Loop should start here
    while True:
        # print("======================")
        for i in range(len(CjZj)):
            CjZj[i] = Cj[i] - numpy.dot(matrix[i], basic_coefficient)
        # print("CjZj:", CjZj)
        if max(CjZj) <= 0:
            break
        z = numpy.dot(RHS, basic_coefficient)
        # print("z:", z)

        index_col = 0
        for i in range(index_col + 1, len(CjZj)):
            if CjZj[i] > CjZj[index_col]:
                index_col = i
        # print("index_col:", index_col)

        # if chosen column is negative stop loop.

        theta = [0] * numConst
        for i in range(len(theta)):
            theta[i] = RHS[i] / matrix[index_col][i]
        # print("theta:", theta)

        index_row = 0
        for i in range(index_row + 1, len(theta)):
            if theta[i] < theta[index_row] and theta[i] >= 0:
                index_row = i
        # print("index_row:", index_row)

        # Switch basic variables
        basic[index_row] = index_col
        basic_coefficient[index_row] = Cj[index_col]
        # print("basic:", basic)
        # print("basic_coeff", basic_coefficient)

        # Divide selected row RHS by pivot
        RHS[index_row] = RHS[index_row] / matrix[index_col][index_row]

        # Divide row by pivot
        for i in range(len(matrix)):
            if i != index_col:
                matrix[i][index_row] = matrix[i][index_row] / matrix[index_col][index_row]

        matrix[index_col][index_row] = 1

        # print("Before M:", matrix)

        # Construct new RHS
        for i in range(len(RHS)):
            if i != index_row:
                factor = matrix[index_col][i]
                RHS[i] = RHS[i] - (RHS[index_row] * factor)

        # Construct new Matrix after chosen column and chosen row
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if i != index_col and j != index_row:
                    factor = matrix[index_col][j]
                    matrix[i][j] = matrix[i][j] - (matrix[i][index_row] * factor)

        # Setting the values of the selected column to 0 apart from pivot
        for i in range(len(matrix[index_col])):
            if i != index_row:
                matrix[index_col][i] = 0

        # print("Matrix:", matrix)
        # print("RHS: ", RHS)
    result = [0] * numVar
    for i in range(len(basic)):
        if basic[i] < numVar:
            result[basic[i]] = RHS[i]
    z = numpy.dot(RHS, basic_coefficient)
    # print("z:", z)

    return result, z


if __name__ == "__main__":
    _, filename = sys.argv
    with open(filename, 'r') as f:
        f.readline()
        numVar = int(f.readline().strip())
        f.readline()
        numConst = int(f.readline().strip())
        f.readline()
        objective = list(map(lambda x : int(x), f.readline().strip().split(',')))
        f.readline()
        constraintsLHS = []
        for _ in range(numConst):
            constraintsLHS.append(list(map(lambda x: int(x), f.readline().strip().split(','))))
        f.readline()
        constraintsRHS = []
        for _ in range(numConst):
            constraintsRHS.append(int(f.readline().strip()))

    # print(objective)
    # print(constraintsLHS)
    # print(constraintsRHS)
    result, z = simplex(objective, constraintsLHS, constraintsRHS)

    with open('lpsolution.txt', 'w') as f:
        f.write("# optimalDecisions\n")
        f.write(str(result)[1:-1] + "\n")
        f.write("# optimalObjective\n")
        f.write(str(z) + "\n")


    # numVar = 2
    # numConst = 7
    # objective = [1, 2]
    # constraintsLHS = [[4, 1], [3, 2], [2, 3], [0, 1], [-1, 1]]
    # constraintsRHS = [44, 39, 37, 9, 6]

    # numVar = 2
    # numConst = 2
    # objective = [1,2]
    # constraintsLHS = [[2,4],[4,3]]
    # constraintsRHS = [12,16]
    # simplex(objective, constraintsLHS, constraintsRHS)
