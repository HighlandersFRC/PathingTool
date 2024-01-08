import numpy as np
import math

def samplePoints(equations, pointList, sampleRate):
    sampledTimes = []
    sampledXPoints = []
    sampledYPoints = []
    sampledThetaPoints = []

    pointTimeList = []

    for i in range(0, len(pointList)):
        pointTimeList.append(pointList[i][0])

    print("TIMES: ", pointTimeList)

    xEquations = equations[0]
    yEquations = equations[1]
    thetaEquations = equations[2]

    currentEquationIndex = 0

    for i in range(sampleRate * pointList[-1][0]):
        time = (i + 1)/(sampleRate)

        for i in range(0, len(pointTimeList) - 1):
            if(time >= pointTimeList[i] and time <= pointTimeList[i+1]):
                currentEquationIndex = i
                break

        currentXEquation = xEquations[i * 4: (i * 4) + 4]
        currentYEquation = yEquations[i * 4: (i * 4) + 4]
        currentThetaEquation = thetaEquations[i * 4: (i * 4) + 4]

        sampledX = currentXEquation[0] + (currentXEquation[1] * time) + (currentXEquation[2] * (time ** 2)) + (currentXEquation[3] * (time ** 3))
        sampledY = currentYEquation[0] + (currentYEquation[1] * time) + (currentYEquation[2] * (time ** 2)) + (currentYEquation[3] * (time ** 3))
        sampledTheta = currentThetaEquation[0] + (currentThetaEquation[1] * time) + (currentThetaEquation[2] * (time ** 2)) + (currentThetaEquation[3] * (time ** 3))

        sampledXPoints.append(sampledX)
        sampledYPoints.append(sampledY)
        sampledThetaPoints.append(sampledTheta)

        sampledTimes.append(time)

    print("TIMES: ", sampledTimes)
    print("X: ", sampledXPoints)
    print("Y: ", sampledYPoints)
    print("Theta: ", sampledThetaPoints)

def generateSplineCurves(points):
    # overallSysEqArray = np.zeros(((len(points) - 1) * 4, (len(points) - 1) * 4))
    overallSysEqArray = []
    xArray = []
    yArray = []
    thetaArray = []
    overallOutputArray = []

    size = (len(points) - 1) * 4
    # print(overallSysEqArray)
    for i in range(len(points) - 1):
        currentPoint = points[i]
        nextPoint = points[i+1]
        if(i == 0):
            xArray.append(0)
            yArray.append(0)
            thetaArray.append(0)
            startPad = [0 for j in range(0, i * 4)]
            eq = startPad + [0, 1, 2 * currentPoint[0], 3 * (currentPoint[0] ** 2)]
            firstEndPad = [0 for j in range(0, ((len(points) - 1) * 4) - len(eq))]
            overallSysEqArray.append(eq + firstEndPad)
            # overallSysEqArray[((i) * 4)][(i) * 4:((i) * 4)+4] = eq
        
        startPad = [0 for j in range(0, i * 4)]

        firstEq = startPad + [1, currentPoint[0], currentPoint[0] ** 2, currentPoint[0] ** 3]
        secondEq = startPad + [1, nextPoint[0], nextPoint[0] ** 2, nextPoint[0] ** 3]
        if(i == len(points) - 2):
            thirdEq = startPad + [0, 1,  2 * nextPoint[0], 3 * (nextPoint[0] ** 2)]
        else:
            thirdEq = startPad + [0 , 1, 2 * nextPoint[0], 3 * (nextPoint[0] ** 2), 0, -1, -2 * nextPoint[0], -3 * (nextPoint[0] ** 2)]
        fourthEq = [0, 0, 2, 6 * nextPoint[0], 0, 0, -2, -6 * nextPoint[0]]

        firstEndPad = [0 for j in range(0, size - len(firstEq))]
        thirdEndPad = [0 for j in range(0, size - len(thirdEq))]
        fourthEndPad = [0 for j in range(0, size - len(fourthEq))]

        overallSysEqArray.append(firstEq + firstEndPad)
        overallSysEqArray.append(secondEq + firstEndPad)
        overallSysEqArray.append(thirdEq + thirdEndPad)

        xArray.append(currentPoint[1])
        xArray.append(nextPoint[1])
        xArray.append(0)

        yArray.append(currentPoint[2])
        yArray.append(nextPoint[2])
        yArray.append(0)

        thetaArray.append(currentPoint[3])
        thetaArray.append(nextPoint[3])
        thetaArray.append(0)

        if(i <= len(points) - 3):
            xArray.append(0)
            yArray.append(0)
            thetaArray.append(0)
            fourthEq = startPad + fourthEq
            fourthEndPad = [0 for j in range(0, size - len(fourthEq))]
            if(i != len(points) - 3):
                fourthEq = fourthEq + fourthEndPad
            overallSysEqArray.append(fourthEq)

    print(overallSysEqArray)

    overallSysEqArray = np.array(overallSysEqArray)

    xMatrix = np.array(xArray)
    yMatrix = np.array(yArray)
    thetaMatrix = np.array(thetaArray)

    M = np.linalg.inv(overallSysEqArray)

    xCoefficients = np.matmul(M, xMatrix)
    yCoefficients = np.matmul(M, yMatrix)
    thetaCoefficients = np.matmul(M, thetaMatrix)

    samplePoints([xCoefficients, yCoefficients, thetaCoefficients], pointList, 10)

pointList = [[0, 1, 2, 0], [1, 3, 1, math.pi/4], [2, 5, 4, math.pi/2], [3, 8, 0, (3/4) * math.pi]]

generateSplineCurves(pointList)