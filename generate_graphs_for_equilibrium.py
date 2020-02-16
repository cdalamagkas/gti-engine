# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 18:16:02 2019

@author: cdal
"""

import random as rn
import sys
import matplotlib.pyplot as plt
import numpy as np
import math


def wait():
    input("Press Enter to continue...")


def print_output(_ans, _a1, _a2, _a3, _d1, _d2, _d3, _d4, _N_max, _N_r):
    print("The following random parameters have been determined to obtain the equilibrium for condition #" + str(ans) + ":")
    print("a1 = " + str(_a1))
    print("a2 = " + str(_a2))
    print("a3 = " + str(_a3))
    print("d1 = " + str(_d1))
    print("d2 = " + str(_d2))
    print("d3 = " + str(_d3))
    print("d4 = " + str(_d4))
    print("N_max = " + str(_N_max))
    print("N_r = " + str(_N_r))


def print_equilibrium(_N, _theta, _phi):
    print("Candidate Equilibrium is:")
    print("\tN* = " + str(_N))
    print("\ttheta* = " + str(_theta))
    print("\tphi* = " + str(_phi))


# d1*theta*phi*N - d2*(1-theta)*phi*N - d3*((1-theta)*N-N_r)**2 - d4*N
def u_d(_d1, _d2, _d3, _d4, _theta, _phi, _N, _N_r):
    return _d1*_theta*_phi*_N - _d2*(1-_theta)*_phi*_N - _d3*((1-_theta)*_N-_N_r)**2 - _d4*_N


def u_a(_a1, _a2, _a3, _theta, _phi, _N, _N_r):
    return _a1*(1-_theta)*_phi*_N - _a2*_theta*_phi*_N - _a3*_phi*_N


N_max = 10
N_r = 3

ans = int(input("Which condition of the NE you want to validate? 1, 3, 4 or 5? Press 6 to set predetermined "
                "parameters\n"))
print("Calculating the parameters a1, a2, a3 and d1, d2, d3, d4. Please wait...")

if ans == 1:
    a2 = rn.random()
    a3 = rn.random()
    a1 = rn.random()*a3
    d1 = rn.random()
    d2 = rn.random()
    d3 = rn.random()
    d4 = 0
    print_output(ans, a1, a2, a3, d1, d2, d3, d4, N_max, N_r)
elif ans == 3:
    a1 = rn.random()
    a2 = rn.random()
    a3 = rn.random()
    d2 = rn.random()
    d3 = rn.random()
    d4 = 2*d3*N_r + rn.random()
    d1 = rn.random()*d4
    print_output(ans, a1, a2, a3, d1, d2, d3, d4, N_max, N_r)

elif ans == 4:
    while True:
        d1 = rn.random()*0.1
        d3 = rn.random()
        d2 = rn.random()
        d4 = rn.random()*d1
        a1 = rn.random()
        a3 = rn.random()*a1
        a2 = rn.random()
        if 0 <= (d1 + d2 + 2 * d3 * N_max - 2 * d3 * N_r) / (2 * d3) <= N_max and d1 > d4 and \
             (a1 + a2) * N_r >= (a2 + a3) * N_max + ((a1 + a2) * (d1 + d2)) / (2 * d3) and a1 > a3:
            break
    print_output(ans, a1, a2, a3, d1, d2, d3, d4, N_max, N_r)

elif ans == 5:
    a1 = rn.random()
    a2 = rn.random()
    a3 = rn.random()*a1
    d1 = rn.random()
    d2 = rn.random()
    d3 = -1*(d1+d2)/(2*(N_max-N_r)) + rn.random()
    d4 = rn.random()
    print_output(ans, a1, a2, a3, d1, d2, d3, d4, N_max, N_r)
elif ans == 6:
    N_max = 10
    N_r = 9
    a1 = 0.5
    a2 = 0.5
    a3 = 0.1
    d1 = 1
    d2 = 1
    d3 = 0.5
    d4 = 0.25375689424589043  # rn.random()*d1
    print_output(ans, a1, a2, a3, d1, d2, d3, d4, N_max, N_r)
else:
    sys.exit(1)

# Obtain the optimal values of (theta, N, phi) according to the chosen type of equilibrium and the random
# d*, a* that satisfy the equilibrium condition
N_optimal = None
theta_optimal = None
phi_optimal = None

if 0 <= (2 * d3 * N_r - d4)/(2 * d3) <= N_max and (a1 <= a3):
    if ans != 1:
        print("I fell into the wrong equilibrium branch, 1 instead of {:d}.".format(ans))
        exit()
    theta_optimal = 0
    N_optimal = (2*d3*N_r-d4)/(2*d3)
    phi_optimal = 0
elif (2*d3*N_r-d4)/(2*d3) < 0 or d1 < d4:
    if ans != 3:
        print("I fell into the wrong equilibrium branch, 3 instead of {:d}.".format(ans))
        exit()
    theta_optimal = 0
    N_optimal = 0
    phi_optimal = 0
elif 0 <= (d1 + d2 + 2*d3*N_max - 2*d3*N_r)/(2 * d3) <= N_max and d1 > d4 and \
        (a1+a2)*N_r >= (a2+a3)*N_max+((a1+a2)*(d1+d2))/(2*d3) and a1 > a3:
    if ans != 4 and ans != 6:
        print("I fell into the wrong equilibrium branch, 4 instead of {:d}.".format(ans))
        exit()
    theta_optimal = (d1+d2+2*d3*N_max-2*d3*N_r)/(2*d3*N_max)
    N_optimal = N_max
    phi_optimal = 1
elif (d1+d2+2*d3*N_max-2*d3*N_r)/(2*d3) < 0 and a1 > a3:
    if ans != 5:
        print("I fell into the wrong equilibrium branch, 5 instead of {:d}.".format(ans))
        exit()
    theta_optimal = 0
    N_optimal = N_r - (d2+d4)/(2*d3)
    phi_optimal = 1
else:
    print("Random d*, a* values did not give any equilibrium, That was unexpected.")
    sys.exit()

Analysis = 2000
solutions_defender = np.zeros((N_max+1, Analysis))
print_equilibrium(N_optimal, theta_optimal, phi_optimal)
Payoff_Attacker_Equilibrium = u_a(a1, a2, a3, theta_optimal, phi_optimal, N_optimal, N_r)
Payoff_Defender_Equilibrium = u_d(d1, d2, d3, d4, theta_optimal, phi_optimal, N_optimal, N_r)
print("U_d* = " + str(Payoff_Defender_Equilibrium))
print("U_a* = " + str(Payoff_Attacker_Equilibrium))
print("Now trying random N, theta, phi in order to validate the equilibrium")
flag = True
theta = np.linspace(0, 1, num=Analysis)
for N in range(0, N_max+1):

    # Evaluate the defender strategy; By holding stable the attacker strategies, can the defender alter its strategy
    # in order to gain more utility?

    for i in range(0, theta.__len__()):
        Ud = u_d(d1, d2, d3, d4, theta[i], phi_optimal, N, N_r)
        if Ud > Payoff_Defender_Equilibrium:
            exit(-10)
        solutions_defender[N][i] = Ud

plot_title = "Defender Utility"
fig = plt.figure(num=plot_title)

for i in range(0, N_max+1):
    label_text = "N = " + str(i)
    plt.plot(theta, solutions_defender[i], label=label_text)

plt.yscale('symlog')
plt.title(plot_title)
plt.xlabel("theta")
plt.ylabel("Utility")
plt.grid(True)

x_optimal = theta_optimal
y_optimal = Payoff_Defender_Equilibrium
plt.plot(x_optimal, y_optimal, 'ro')

plt.legend(fontsize='xx-small')

# plt.annotate('Nash equilibrium', xy=(x_optimal, y_optimal),
#             xytext=(x_optimal - x_optimal * 0.5, y_optimal + y_optimal * 0.25), arrowprops=dict(facecolor='black',
#                                                                                                 shrink=0.05))
plt.show()
