import numpy as np
import math
from matplotlib.pyplot import plot, show, quiver
import matplotlib.pyplot as plt
import time

class SplineGenerator:
    def __init__(self):
        self.xEquations = []
        self.yEquations = []
        self.thetaEquations = []

        self.xVelEquations = []
        self.yVelEquations = []
        self.thetaVelEquations = []

        self.xAccelEquations = []
        self.yAccelEquations = []
        self.thetaAccelEquations = []

    def sample_pos(self, key_points: list, time: float):
        index = 0
        for i in range(len(key_points) - 1):
            if time >= key_points[i].time and time <= key_points[i + 1].time:
                index = i
                break
        xEquation = self.xEquations[index]
        yEquation = self.yEquations[index]
        thetaEquation = self.thetaEquations[index]
        x = float(np.polyval(xEquation, time))
        y = float(np.polyval(yEquation, time))
        theta = float(np.polyval(thetaEquation, time))
        return [x, y, theta]

    def sample_lin_vel(self, key_points: list, time: float):
        index = 0
        for i in range(len(key_points) - 1):
            if time >= key_points[i].time and time <= key_points[i + 1].time:
                index = i
                break
        xEquation = self.xEquations[index]
        xVelEquation = self.xVelEquations[index]
        yEquation = self.yEquations[index]
        yVelEquation = self.yVelEquations[index]
        x = float(np.polyval(xEquation, time))
        y = float(np.polyval(yEquation, time))
        vx = float(np.polyval(xVelEquation, time))
        vy = float(np.polyval(yVelEquation, time))
        try:
            return (x * vx + y * vy) / math.sqrt(x ** 2 + y ** 2)
        except:
            return 0

    def sample_raw_linear_info(self, key_points: list, time: float):
        index = 0
        for i in range(len(key_points) - 1):
            if time >= key_points[i].time and time <= key_points[i + 1].time:
                index = i
                break
        xEquation = self.xEquations[index]
        xVelEquation = self.xVelEquations[index]
        xAccelEquation = self.xAccelEquations[index]
        yEquation = self.yEquations[index]
        yVelEquation = self.yVelEquations[index]
        yAccelEquation = self.yAccelEquations[index]
        x = float(np.polyval(xEquation, time))
        y = float(np.polyval(yEquation, time))
        vx = float(np.polyval(xVelEquation, time))
        vy = float(np.polyval(yVelEquation, time))
        ax = float(np.polyval(xAccelEquation, time))
        ay = float(np.polyval(yAccelEquation, time))
        return [x, y, vx, vy, ax, ay]

    def sample_lin_accel(self, key_points: list, time: float):
        index = 0
        for i in range(len(key_points) - 1):
            if time >= key_points[i].time and time <= key_points[i + 1].time:
                index = i
                break
        xEquation = self.xEquations[index]
        xVelEquation = self.xVelEquations[index]
        xAccelEquation = self.xAccelEquations[index]
        yEquation = self.yEquations[index]
        yVelEquation = self.yVelEquations[index]
        yAccelEquation = self.yAccelEquations[index]
        x = float(np.polyval(xEquation, time))
        y = float(np.polyval(yEquation, time))
        vx = float(np.polyval(xVelEquation, time))
        vy = float(np.polyval(yVelEquation, time))
        ax = float(np.polyval(xAccelEquation, time))
        ay = float(np.polyval(yAccelEquation, time))
        try:
            return (x ** 3 * ax + x ** 2 * vy ** 2 + x ** 2 * y * ay + y ** 2 * x * ax - 2 * x * y * vx * vy + y ** 2 * vx ** 2 + y ** 3 * ay) / ((x ** 2 + y ** 2) * math.sqrt(x ** 2 + y ** 2))
        except:
            return 0
        
    def sample_derivs(self, key_points: list, time: float):
        index = 0
        for i in range(len(key_points) - 1):
            if time >= key_points[i].time and time <= key_points[i + 1].time:
                index = i
                break
        xEquation = self.xEquations[index]
        xVelEquation = self.xVelEquations[index]
        xAccelEquation = self.xAccelEquations[index]
        yEquation = self.yEquations[index]
        yVelEquation = self.yVelEquations[index]
        yAccelEquation = self.yAccelEquations[index]
        x = float(np.polyval(xEquation, time))
        y = float(np.polyval(yEquation, time))
        vx = float(np.polyval(xVelEquation, time))
        vy = float(np.polyval(yVelEquation, time))
        ax = float(np.polyval(xAccelEquation, time))
        ay = float(np.polyval(yAccelEquation, time))
        return (vx, vy, ax, ay)

    def generateSplineCurves(self, points):
        overallSysEqArray = []
        xArray = []
        yArray = []
        thetaArray = []

        size = (len(points) - 1) * 6

        for i in range(len(points) - 1):
            currentPoint = points[i]
            nextPoint = points[i+1]
            
            startPad = [0 for j in range(0, i * 6)]

            firstPointEq = startPad + [1, currentPoint[0], currentPoint[0] ** 2, currentPoint[0] ** 3, currentPoint[0] ** 4, currentPoint[0] ** 5]
            secondPointEq = startPad + [1, nextPoint[0], nextPoint[0] ** 2, nextPoint[0] ** 3, nextPoint[0] ** 4, nextPoint[0] ** 5]
            firstVelEq = startPad + [0, 1,  2 * currentPoint[0], 3 * (currentPoint[0] ** 2), 4 * (currentPoint[0] ** 3), 5 * (currentPoint[0] ** 4)]
            secondVelEq = startPad + [0, 1,  2 * nextPoint[0], 3 * (nextPoint[0] ** 2), 4 * (nextPoint[0] ** 3), 5 * (nextPoint[0] ** 4)]
            firstAccelEq = startPad + [0, 0, 2, 6 * currentPoint[0], 12 * currentPoint[0] ** 2, 20 * (currentPoint[0] ** 3)]
            secondAccelEq = startPad + [0, 0, 2, 6 * nextPoint[0], 12 * nextPoint[0] ** 2, 20 * (nextPoint[0] ** 3)]

            firstEndPad = [0 for j in range(0, size - len(firstPointEq))]
            secondEndPad = [0 for j in range(0, size - len(secondPointEq))]
            firstVelEndPad = [0 for j in range(0, size - len(firstVelEq))]
            secondVelEndPad = [0 for j in range(0, size - len(secondVelEq))]
            firstAcelEndPad = [0 for j in range(0, size - len(firstAccelEq))]
            secondAcelEndPad = [0 for j in range(0, size - len(secondAccelEq))]

            overallSysEqArray.append(firstPointEq + firstEndPad)
            overallSysEqArray.append(secondPointEq + secondEndPad)
            overallSysEqArray.append(firstVelEq + firstVelEndPad)
            overallSysEqArray.append(secondVelEq + secondVelEndPad)
            overallSysEqArray.append(firstAccelEq + firstAcelEndPad)
            overallSysEqArray.append(secondAccelEq + secondAcelEndPad)
            
            xArray.append(currentPoint[1])
            xArray.append(nextPoint[1])
            xArray.append(currentPoint[4])
            xArray.append(nextPoint[4])
            xArray.append(currentPoint[7])
            xArray.append(nextPoint[7])

            yArray.append(currentPoint[2])
            yArray.append(nextPoint[2])
            yArray.append(currentPoint[5])
            yArray.append(nextPoint[5])
            yArray.append(currentPoint[8])
            yArray.append(nextPoint[8])

            thetaArray.append(currentPoint[3])
            thetaArray.append(nextPoint[3])
            thetaArray.append(currentPoint[6])
            thetaArray.append(nextPoint[6])
            thetaArray.append(currentPoint[9])
            thetaArray.append(nextPoint[9])

        overallSysEqArray = np.array(overallSysEqArray)

        # print("eqs: ", overallSysEqArray)

        xMatrix = np.array(xArray)
        yMatrix = np.array(yArray)
        thetaMatrix = np.array(thetaArray)

        # print("x: ", xMatrix)
        # print("y: ", yMatrix)

        M = np.linalg.inv(overallSysEqArray)

        xCoefficients = np.matmul(M, xMatrix)
        yCoefficients = np.matmul(M, yMatrix)
        thetaCoefficients = np.matmul(M, thetaMatrix)

        # print(f"X: {xCoefficients}")

        self.xVelEquations = []
        self.yVelEquations = []
        self.thetaVelEquations = []

        self.xEquations = [list(np.flip(xCoefficients[i * 6:(i + 1) * 6])) for i in range(int(len(xCoefficients) / 6))]
        self.yEquations = [list(np.flip(yCoefficients[i * 6:(i + 1) * 6])) for i in range(int(len(yCoefficients) / 6))]
        self.thetaEquations = [list(np.flip(thetaCoefficients[i * 6:(i + 1) * 6])) for i in range(int(len(thetaCoefficients) / 6))]

        for e in self.xEquations:
            self.xVelEquations.append(list(np.polyder(e)))
        for e in self.yEquations:
            self.yVelEquations.append(list(np.polyder(e)))
        for e in self.thetaEquations:
            self.thetaVelEquations.append(list(np.polyder(e)))

        self.xAccelEquations = []
        self.yAccelEquations = []
        self.thetaAccelEquations = []

        for e in self.xVelEquations:
            self.xAccelEquations.append(list(np.polyder(e)))
        for e in self.yVelEquations:
            self.yAccelEquations.append(list(np.polyder(e)))
        for e in self.thetaVelEquations:
            self.thetaAccelEquations.append(list(np.polyder(e)))

        # print(f"XP: {self.xEquations}")
        # print(f"XV: {self.xVelEquations}")
        # print(f"XA: {self.xAccelEquations}")