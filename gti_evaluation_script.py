import random as rn
import sys
import matplotlib.pyplot as plt


def u_d(_d1, _d2, _d3, _d4, _theta, _phi, _N, _N_r):
    return _d1*_theta*_phi*_N - _d2*(1-_theta)*_phi*_N - _d3*((1-_theta)*_N-_N_r)**2 - _d4*_N


def u_a(_a1, _a2, _a3, _theta, _phi, _N, _N_r):
    return _a1*(1-_theta)*_phi*_N - _a2*_theta*_phi*_N - _a3*_phi*_N


def gti_evaluation_script(n_optimal, n_r, theta_optimal, phi_optimal, a, d):

    Payoff_Attacker_Equilibrium = u_a(a[0], a[1], a[2], theta_optimal, phi_optimal, n_optimal, n_r)

    Payoff_Defender_Equilibrium = u_d(d[0], d[1], d[2], d[3], theta_optimal, phi_optimal, n_optimal, n_r)
    Tries = 2000
    flag = True
    for i in range(0, Tries):

        # Evaluate the attacker strategy; By holding stable the defender strategy (N, theta), can the attacker alter
        # its strategy in order to gain more utility?

        N = N_optimal
        theta = theta_optimal
        phi = rn.random()

        Ua = u_a(a1, a2, a3, theta, phi, N, N_r)

        if Ua > Payoff_Attacker_Equilibrium:
            better_solutions_attacker_counter = better_solutions_attacker_counter + 1
            better_solutions_attacker.append({'theta': theta, 'phi': phi, 'N': N, 'U_a': Ua})

        # Evaluate the defender strategy; By holding stable the attacker strategies, can the defender alter its strategy
        # in order to gain more utility?

        N = rn.randint(1, N_max)
        theta = rn.random()
        phi = phi_optimal

        Ud = u_d(d1, d2, d3, d4, theta, phi, N, N_r)

        if Ud > Payoff_Defender_Equilibrium:
            better_solutions_defender = better_solutions_defender + 1
            solutions_defender.append({'theta': theta, 'phi': phi, 'N': N, 'U_d': Ud})

        solutions_defender.append([N*theta, Ud, N, theta])

    solutions_defender.append([N_optimal * theta_optimal, Payoff_Defender_Equilibrium, N_optimal, theta_optimal])
    solutions_defender.sort(key=lambda tup: tup[0])

    better_solutions_attacker_counter = (better_solutions_attacker_counter / Tries) * 100
    better_solutions_defender_counter = (better_solutions_defender_counter / Tries) * 100
    if better_solutions_attacker_counter == 0 and better_solutions_defender_counter == 0:
        print("No better solution was found after " + str(Tries) + "tries. Success!", flush=True)
    else:
        print("After {:d} tries:\n\t{:12.2f}% of random attacker solutions were better than the equilibrium.\n"
              "\t{:12.2f}% of random defender solutions were better than the equilibrium.".
              format(Tries, better_solutions_attacker_counter, better_solutions_defender_counter))
        print("Solutions that give greater Ud than the equilibrium")
        print(better_solutions_defender)
        print("Solutions that give greater Ua than the equilibrium")
        print(better_solutions_attacker)
        exit(-1)





