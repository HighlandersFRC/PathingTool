import numpy as np

def generateSplineCurves(points):
    overallSysEqArray = []
    yArray = []
    for point in points:
        sysEqArray = [1, point[0], point[0] ** 2, point[0] ** 3]
        overallSysEqArray.append(sysEqArray)
        yArray.append(point[1])
    print("OVERALL: " + str(overallSysEqArray))
    print("Y MATRIX: " + str(yArray))

    yMatrix = np.array(yArray)

    sysEqMatrix = np.array(overallSysEqArray)

    M = np.linalg.inv(sysEqMatrix)

    coefficientMatrix = np.matmul(M, yMatrix)

    print(coefficientMatrix)

pointList = [[-10,-8], [7.68,5], [3,15], [-4, -2.743]]

generateSplineCurves(pointList)