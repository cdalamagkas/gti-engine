import random as rn
import numpy as np
import cvxpy as cp
import matplotlib.pyplot as plt


def u_d(phi):
    return d1*theta*phi*n - d2*(1-theta)*phi*n - d3*((1-theta)*n-n_r)**2 - d4*n


def get_theta_optimal():
    return (d1 + d2 + 2 * d3 * n_max - 2 * d3 * n_r) / (2 * d3 * n_max)


def get_random_a():  # return random values for (a1, a2, a3)
    _a1 = rn.random()
    return [_a1, rn.random() * _a1, rn.random()]


def get_random_d():  # return random values for (d1, d2, d3, d4)
    _d1 = rn.random()
    if bias_plug_out_real_device:
        _d3 = 1000
    else:
        _d3 = rn.random()
    return [_d1, rn.random(), _d3, rn.random() * _d1]


def parameters_valid():
    if 0 <= (d1 + d2 + 2 * d3 * n_max - 2 * d3 * n_r) / (2 * d3) <= n_max and d1 > d4 and \
            (a1 + a2) * n_r >= (a2 + a3) * n_max + ((a1 + a2) * (d1 + d2)) / (2 * d3) and a1 > a3:
        return True
    else:
        return False


if __name__ == "__main__":
    n_max = 10
    n_r = 3
    bias_plug_out_real_device = False

    Analysis = 2000
    solutions_defender = np.zeros((3, Analysis))

    while True:
        # Actually we need only d, but d still needs to be valid
        d1, d2, d3, d4 = get_random_d()
        a1, a2, a3 = get_random_a()
        if parameters_valid():
            break

    # Solve the convex optimisation problem to get n1, n2
    n1 = cp.Variable()
    n2 = cp.Variable()
    y = cp.Variable()

    constraints = [n1 + n2 <= n_max,
                   d1 * n1 - d2 * n2 - d3 * (n2 - n_r) ** 2 - d4 * (n1 + n2) >= y,
                   -d3 * (n2 - n_r) ** 2 - d4 * (n1 + n2) >= y,
                   n1 >= 0,
                   n2 >= 0]
    obj = cp.Maximize(y)

    prob = cp.Problem(obj, constraints)
    prob.solve()

    # By solving the system of n1, n2, we get theta and n
    n_optimal = n1.value + n2.value
    theta_optimal = n1.value/(n1.value+n2.value)

    n = n_optimal
    theta = theta_optimal

    utility_phi_1 = u_d(phi=1)
    utility_phi_0 = u_d(phi=0)
    random = rn.random()
    utility_phi_random = u_d(phi=random)

    # prob.status
    # prob.value
    # n1.value
    # n2.value

    theta_array = np.linspace(0, 1, num=Analysis)

    for i in range(0, theta_array.__len__()):
        theta = theta_array[i]
        n = rn.randint(0, n_max+1)

        solutions_defender[0][i] = u_d(phi=0)
        solutions_defender[1][i] = u_d(phi=1)
        random = rn.random()
        solutions_defender[2][i] = u_d(phi=random)

    print(solutions_defender)

    plot_title = "Defender Utility (maxmin)"
    fig = plt.figure(num=plot_title)

    for i in range(0, 3):
        if i == 0:
            label_text = "phi = 0"
        elif i == 1:
            label_text = "phi = 1"
        else:
            label_text = "phi in (0, 1)"

        plt.plot(theta_array, solutions_defender[i], label=label_text)

    plt.yscale('symlog')
    plt.title(plot_title)
    plt.xlabel("theta")
    plt.ylabel("Utility")
    plt.grid(True)

    x_optimal = theta_optimal
    y_optimal = utility_phi_1
    plt.plot(x_optimal, y_optimal, 'ro')

    #x_optimal = theta_optimal
    #y_optimal = utility_phi_0
    #plt.plot(x_optimal, y_optimal, 'go')

    plt.legend(fontsize='xx-small')

    #plt.annotate('Nash equilibrium', xy=(x_optimal, y_optimal),
    #             xytext=(x_optimal - x_optimal * 0.5, y_optimal + y_optimal * 0.25), arrowprops=dict(facecolor='black',
    #                                                                                                 shrink=0.05))
    plt.show()
