import numpy as np
import math
from matplotlib.pyplot import plot, show, quiver
import matplotlib.pyplot as plt
import time

class SplineGenerator:
    def __init__(self):
        self.rEquations = []
        self.thetaEquations = []

        self.rVelEquations = []
        self.thetaVelEquations = []

        self.rAccelEquations = []
        self.thetaAccelEquations = []

    def sample_pos(self, key_points: list, time: float):
        index = 0
        for i in range(len(key_points) - 1):
            if time >= key_points[i][0] and time <= key_points[i + 1][0]:
                index = i
                break
        rEquation = self.rEquations[index]
        thetaEquation = self.thetaEquations[index]
        r = float(np.polyval(rEquation, time))
        theta = float(np.polyval(thetaEquation, time))
        return [r, theta]

    def sample_lin_vel(self, key_points: list, time: float):
        index = 0
        for i in range(len(key_points) - 1):
            if time >= key_points[i][0] and time <= key_points[i + 1][0]:
                index = i
                break
        rEquation = self.rEquations[index]
        rVelEquation = self.rVelEquations[index]
        thetaEquation = self.thetaEquations[index]
        thetaVelEquation = self.thetaVelEquations[index]
        r = float(np.polyval(rEquation, time))
        theta = float(np.polyval(thetaEquation, time))
        vr = float(np.polyval(rVelEquation, time))
        vtheta = float(np.polyval(thetaVelEquation, time))
        try:
            return (r * vr + theta * vtheta) / math.sqrt(r ** 2 + theta ** 2)
        except:
            return 0

    def sample_raw_linear_info(self, key_points: list, time: float):
        index = 0
        for i in range(len(key_points) - 1):
            if time >= key_points[i][0] and time <= key_points[i + 1][0]:
                index = i
                break
        rEquation = self.rEquations[index]
        rVelEquation = self.rVelEquations[index]
        rAccelEquation = self.rAccelEquations[index]
        thetaEquation = self.thetaEquations[index]
        thetaVelEquation = self.thetaVelEquations[index]
        thetaAccelEquation = self.thetaAccelEquations[index]
        r = float(np.polyval(rEquation, time))
        theta = float(np.polyval(thetaEquation, time))
        vr = float(np.polyval(rVelEquation, time))
        vtheta = float(np.polyval(thetaVelEquation, time))
        ar = float(np.polyval(rAccelEquation, time))
        atheta = float(np.polyval(thetaAccelEquation, time))
        return [r, theta, vr, vtheta, ar, atheta]

    def sample_lin_accel(self, key_points: list, time: float):
        index = 0
        for i in range(len(key_points) - 1):
            if time >= key_points[i][0] and time <= key_points[i + 1][0]:
                index = i
                break
        rEquation = self.rEquations[index]
        rVelEquation = self.rVelEquations[index]
        rAccelEquation = self.rAccelEquations[index]
        thetaEquation = self.thetaEquations[index]
        thetaVelEquation = self.thetaVelEquations[index]
        thetaAccelEquation = self.thetaAccelEquations[index]
        r = float(np.polyval(rEquation, time))
        theta = float(np.polyval(thetaEquation, time))
        vr = float(np.polyval(rVelEquation, time))
        vtheta = float(np.polyval(thetaVelEquation, time))
        ar = float(np.polyval(rAccelEquation, time))
        atheta = float(np.polyval(thetaAccelEquation, time))
        try:
            return (r ** 3 * ar + r ** 2 * vtheta ** 2 + r ** 2 * theta * atheta + theta ** 2 * r * ar - 2 * r * theta * vr * vtheta + theta ** 2 * vr ** 2 + theta ** 3 * atheta) / ((r ** 2 + theta ** 2) * math.sqrt(r ** 2 + theta ** 2))
        except:
            return 0

    def generateSplineCurves(self, points):
        overallSysEqArray = []
        xArray = []
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
            xArray.append(currentPoint[3])
            xArray.append(nextPoint[3])
            xArray.append(currentPoint[5])
            xArray.append(nextPoint[5])

            thetaArray.append(currentPoint[2])
            thetaArray.append(nextPoint[2])
            thetaArray.append(currentPoint[4])
            thetaArray.append(nextPoint[4])
            thetaArray.append(currentPoint[6])
            thetaArray.append(nextPoint[6])

        overallSysEqArray = np.array(overallSysEqArray)

        # print("eqs: ", overallSysEqArray)

        xMatrix = np.array(xArray)
        thetaMatrix = np.array(thetaArray)

        # print("x: ", xMatrix)
        # print("y: ", yMatrix)

        M = np.linalg.inv(overallSysEqArray)

        xCoefficients = np.matmul(M, xMatrix)
        thetaCoefficients = np.matmul(M, thetaMatrix)

        # print(f"X: {xCoefficients}")

        self.rVelEquations = []
        self.thetaVelEquations = []

        self.rEquations = [list(np.flip(xCoefficients[i * 6:(i + 1) * 6])) for i in range(int(len(xCoefficients) / 6))]
        self.thetaEquations = [list(np.flip(thetaCoefficients[i * 6:(i + 1) * 6])) for i in range(int(len(thetaCoefficients) / 6))]

        for e in self.rEquations:
            self.rVelEquations.append(list(np.polyder(e)))
        for e in self.thetaEquations:
            self.thetaVelEquations.append(list(np.polyder(e)))

        self.rAccelEquations = []
        self.thetaAccelEquations = []

        for e in self.rVelEquations:
            self.rAccelEquations.append(list(np.polyder(e)))
        for e in self.thetaVelEquations:
            self.thetaAccelEquations.append(list(np.polyder(e)))

        # print(f"XP: {self.rEquations}")
        # print(f"XV: {self.rVelEquations}")
        # print(f"XA: {self.rAccelEquations}")