import random as rn
import math as mth
import numpy as np
import matplotlib.pyplot as plt


def get_theta_1(_D_a, _D_b, _mi, _phi_a_max, _phi_b_max, _d3, _N_max, _N_r):
    return ((_D_a[0] + _D_a[1]) * _mi * _phi_a_max)/(2*_N_max*_d3) + \
           (((_D_b[0] + _D_b[1] - _mi*_D_b[0] - _mi*_D_b[1])*_phi_b_max) + 2*_d3*(_N_max - _N_r)) / (2*_N_max*_d3)


def get_theta_2(_D_a, _mi, _phi_a_max, _d3, _N_max, _N_r):
    return (_mi * _phi_a_max * _D_a[0] + _mi * _phi_a_max * _D_a[1] + 2 * _d3 * _N_max - 2 * _d3 * _N_r)/\
           (2 * _N_max * _d3)


def get_theta_3(_D_b, _mi, _phi_b_max, _d3, _N_max, _N_r):
    return ((1 - _mi) * _phi_b_max * _D_b[0] + (1 - _mi) * _phi_b_max * _D_b[1] + 2 * _d3 * _N_max - 2 * _d3 * _N_r)/\
           (2 * _d3 * _N_max)


def u_d(_D_a, _D_b, _mi, _phi_a, _phi_b, _d3, _d4, _N, _theta, _N_r):
    return _mi * (_D_a[0]*_theta*_phi_a*_N - _D_a[1]*(1 - _theta)*_phi_a*_N - _d3*( (1-_theta)*_N - _N_r)**2 -_d4*_N) + \
           (1-_mi) * (_D_b[0]*_theta*_phi_b*_N - _D_b[1]*(1-_theta)*_phi_b*_N - _d3*( (1-_theta)*_N - _N_r)**2 -_d4*_N)


def u_a(a, _theta, _phi, _N):
    return a[0]*(1-_theta)*_phi*_N - a[1]*_theta*_phi*_N - a[2]*_phi*_N


def print_output():
    print("The following random parameters have been determined to obtain the equilibrium for branch #"
          + str(branch) + ":")
    print("d3 = " + str(d3))
    print("d4 = " + str(d4) + "\n")

    print("Profile A")
    print("a_{1,a} = " + str(A_a[0]))
    print("a_{2,a} = " + str(A_a[1]))
    print("a_{3,a} = " + str(A_a[2]))
    print("d_{1,a} = " + str(D_a[0]))
    print("d_{2,a} = " + str(D_a[1]) + "\n")

    print("Profile B")
    print("a_{1,b} = " + str(A_a[2]))
    print("a_{2,b} = " + str(A_a[2]))
    print("a_{3,b} = " + str(A_a[2]))
    print("d_{1,b} = " + str(A_a[2]))
    print("d_{2,b} = " + str(A_a[2]) + "\n")

    print("N_max = " + str(N_max))
    print("N_r = " + str(N_r))


def print_equilibrium(_N, _theta, _phi_a, _phi_b, _u_d, _u_a_a, _u_a_b):
    print("Candidate Equilibrium is:")
    print("\tN* = " + str(_N))
    print("\ttheta* = " + str(_theta))
    print("\tphi_a* = " + str(_phi_a))
    print("\tphi_b* = " + str(_phi_b))
    print("\tU_d* = " + str(_u_d))
    print("\tU_a_a* = " + str(_u_a_a))
    print("\tU_a_b* = " + str(_u_a_b))


def get_random_profiles():
    _d3 = 1000 * rn.random()
    _d4 = rn.random()
    _A_a = [0]*3
    _A_b = [0]*3
    _D_a = [0]*2
    _D_b = [0]*2

    _A_a[0] = rn.random()
    _A_a[1] = rn.random() * _A_a[0]
    _A_a[2] = rn.random() * _A_a[1]

    _D_a[0] = rn.random()
    _D_a[1] = _D_a[0] * rn.random()

    _A_b[1] = rn.random()
    _A_b[0] = rn.random() * _A_a[1]
    _A_b[2] = rn.random() * _A_a[0]

    _D_b[1] = rn.random()
    _D_b[0] = _D_a[1] * rn.random()

    return _A_a, _A_b, _D_a, _D_b, _d3, _d4


if __name__ == "__main__":
    N_max = 5
    N_r = 2

    phi_a_max = 0.9
    phi_b_max = 0.8

    mi = rn.random()

    # branch = int(input("Plese select the branch to validate: "))

    branch = 7

    '''
    Προφιλ 1 επιτιθέμενου: Τυχαίες τιμές a, με συνθήκη a1 > a2
    Προφίλ 2 επιτιθέμενου: Τυχαίες τιμές, a, με συνθήκη a1 < a2
    
    Προφιλ 1 αμυνόμενου: Τυχαίες τιμές d, με συνθήκη d1 > d2
    Προφίλ 2 αμυνόμενου: Τυχαίες τιμές, d, με συνθήκη d1 < d2
    '''

    if branch == 1:
        while True:
            A_a, A_b, D_a, D_b, d3, d4 = get_random_profiles()
            theta = get_theta_1(D_a, D_b, mi, phi_a_max, phi_b_max, d3, N_max, N_r)
            if 0 <= theta <= 1 and mi*D_a[0]*phi_a_max + D_b[0]*phi_b_max*(1-mi) >= d4 and \
                -mi*(D_a[0] + D_a[1])*phi_a_max + (mi - 1)*(D_b[0] + D_b[1])*phi_b_max + 2*d3*N_r >= \
                    (2*d3*(A_a[1]+A_a[2])*N_max)/(A_a[0]+A_a[1]) and \
                -mi*(D_a[0] + D_a[1])*phi_a_max + (mi - 1)*(D_b[0] + D_b[1])*phi_b_max + 2*d3*N_r >= \
                    (2*d3*(A_b[1]+A_b[2])*N_max)/(A_b[0]+A_b[1]):

                print("I'm in branch 1")
                theta_optimal = theta
                N_optimal = N_max
                phi_a_optimal = phi_a_max
                phi_b_optimal = phi_b_max
                U_d_optimal = u_d(D_a, D_b, mi, phi_a_optimal, phi_b_optimal, d3, d4, N_optimal, theta_optimal)
                U_a_a_optimal = u_a(A_a, theta_optimal, phi_a_optimal, N_optimal)
                U_a_b_optimal = u_a(A_b, theta_optimal, phi_b_optimal, N_optimal)
                break
            else:
                continue
    elif branch == 5:
        while True:
            A_a, A_b, D_a, D_b, d3, d4 = get_random_profiles()
            theta = get_theta_2(D_a, mi, phi_a_max, d3, N_max, N_r)
            if A_a[0] > A_a[2] and A_b[0] > A_b[2] and 0 <= theta <= 1 and mi * phi_a_max * D_a[0] >= d4 and \
                    (A_a[0] + A_a[1])*(2*d3*N_r - mi*phi_a_max*(D_a[0] + D_a[1]))/(d3*(A_a[1] + A_a[2])) >= N_max and \
                    (A_b[0] + A_b[1])*(2*d3*N_r - mi*phi_a_max*(D_a[0] + D_a[1]))/(d3*(A_a[1] + A_a[2])) <= N_max:

                print("I'm in branch 5")
                theta_optimal = theta
                N_optimal = N_max
                phi_a_optimal = phi_a_max
                phi_b_optimal = 0
                U_d_optimal = u_d(D_a, D_b, mi, phi_a_optimal, phi_b_optimal, d3, d4, N_optimal, theta_optimal)
                U_a_a_optimal = u_a(A_a, theta_optimal, phi_a_optimal, N_optimal)
                U_a_b_optimal = u_a(A_b, theta_optimal, phi_b_optimal, N_optimal)
                break
            else:
                continue
    elif branch == 7:
        while True:
            A_a, A_b, D_a, D_b, d3, d4 = get_random_profiles()
            theta = get_theta_3(D_b, mi, phi_b_max, d3, N_max, N_r)
            if A_a[0] > A_a[2] and A_b[0] > A_b[2] and 0 <= theta <= 1 and (1 - mi)*phi_b_max*D_b[0] >= d4 and \
                    (A_a[0] + A_a[1])*(2*d3*N_r - mi*phi_a_max*(D_a[0] + D_a[1]))/(d3*(A_a[1] + A_a[2])) <= N_max and \
                    (A_b[0] + A_b[1])*(2*d3*N_r - mi*phi_a_max*(D_a[0] + D_a[1]))/(d3*(A_a[1] + A_a[2])) >= N_max:

                print("I'm in branch 7")
                theta_optimal = theta
                N_optimal = N_max
                phi_a_optimal = 0
                phi_b_optimal = phi_b_max
                U_d_optimal = u_d(D_a, D_b, mi, phi_a_optimal, phi_b_optimal, d3, d4, N_optimal, theta_optimal)
                U_a_a_optimal = u_a(A_a,theta_optimal, phi_a_optimal, N_optimal)
                U_a_b_optimal = u_a(A_b,theta_optimal, phi_b_optimal, N_optimal)

                print_equilibrium(N_optimal, theta_optimal, phi_a_optimal, phi_b_optimal, U_d_optimal, U_a_a_optimal, U_a_b_optimal)

                break
            else:
                continue
    else:
        print("Branch not implemented. Please try again.")
        exit()

    print_output()
    print_equilibrium(N_optimal, theta_optimal, phi_a_optimal, phi_b_optimal, U_d_optimal, U_a_a_optimal, U_a_b_optimal)

    Analysis = 2000
    solutions_defender = np.zeros((N_max + 1, Analysis))

    Payoff_Attacker_Equilibrium = [U_a_a_optimal, U_a_b_optimal]
    Payoff_Defender_Equilibrium = U_d_optimal
    print("U_d* = " + str(Payoff_Defender_Equilibrium))
    print("U_a* = " + str(Payoff_Attacker_Equilibrium))

    print("Now trying random N, theta, phi in order to validate the equilibrium")
    flag = True
    theta = np.linspace(0, 1, num=Analysis)

    for N in range(0, N_max + 1):

        # Evaluate the defender strategy; By holding stable the attacker strategies, can the defender alter its strategy
        # in order to gain more utility?

        for i in range(0, theta.__len__()):
            ud = u_d(D_a, D_b, mi, phi_a_optimal, phi_b_optimal, d3, d4, N, theta[i])
            if ud > Payoff_Defender_Equilibrium:
                exit(-10)
            solutions_defender[N][i] = ud

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

