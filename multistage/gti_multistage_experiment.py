import matplotlib.pyplot as plt
import numpy as np
import multistage.gti_multistage_measurement as gti
import json

mi = 0.5
phi_a_max = 0.3
phi_b_max = 0.7
max_rounds = 50
N_r = 5
N_max = 8
type_of_the_real_attacker = 'r'

D_a = [0.4472531755411864, 0.2967125188510017]
D_b = [0.11410501323488792, 0.35406490281778435]
A_a = [0.5346035201072344, 0.33471264028448916, 0.1252598958349572]
A_b = [0.26871386868702746, 0.23505802780611662, 0.027600494097260224]
d3 = 0.41943123123741644
d4 = 0.06949467531580411

while True:
    history_equilibrium, parameters = gti.gti_multistage_measurement(mi, phi_a_max, phi_b_max, max_rounds, N_r, N_max,
                                                                     type_of_the_real_attacker, D_a, D_b, A_a, A_b, d3,
                                                                     d4)
    if history_equilibrium is not None:
        break

utilities_attacker_a = []
utilities_attacker_b = []
utilities_defender = []
history_belief = []

for i in history_equilibrium:
    utilities_attacker_a.append(i['U_a_a'])
    utilities_attacker_b.append(i['U_a_b'])
    utilities_defender.append(i['U_d'])
    history_belief.append(i['mi'])

# Belief through time
plot_title = "Belief"
fig = plt.figure(num=plot_title)

plt.plot(list(range(0, history_belief.__len__())), history_belief)
plt.title(plot_title)
plt.xlabel("round")
plt.ylabel("Belief")
plt.grid(True)
plt.ylim([0, 1])
plt.show()

# Attacker Utility through time
plot_title = "Utility"
fig2 = plt.figure(num=plot_title)

plt.plot(list(range(0, utilities_attacker_a.__len__())), utilities_attacker_a, label="Attacker type A utility")
plt.plot(list(range(0, utilities_attacker_b.__len__())), utilities_attacker_b, label="Attacker type B utility")
plt.plot(list(range(0, utilities_defender.__len__())), utilities_defender, label="Defender utility")
plt.title(plot_title)
plt.xlabel("round")
plt.ylabel("Utility")
plt.grid(True)
plt.legend()

with open('results/parameters.txt', 'w') as outfile:
    json.dump(parameters, outfile)

with open('results/equilibriums.txt', 'w') as outfile:
    json.dump(history_equilibrium, outfile)

with open('results/beliefs.txt', 'w') as outfile:
    json.dump(history_belief, outfile)

plt.show()

'''
    plot_title = "Defender Utility"
    fig = plt.figure(num=plot_title)

    for i in range(0, N_max + 1):
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
'''