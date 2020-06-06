import random as rn


def get_theta_1(D_a, D_b, mi, phi_a_max, phi_b_max, d3, N_max, N_r):
    return ((D_a[0] + D_a[1]) * mi * phi_a_max)/(2*N_max*d3) + \
           (((D_b[0] + D_b[1] - mi*D_b[0] - mi*D_b[1])*phi_b_max) + 2*d3*(N_max - N_r)) / (2*N_max*d3)


def get_theta_2(D_a, mi, phi_a_max, d3, N_max, N_r):
    return (mi*phi_a_max*D_a[0] + mi*phi_a_max*D_a[1] + 2*d3*N_max - 2*d3*N_r)/(2*N_max*d3)


def get_theta_3(D_b, mi, phi_b_max, d3, N_max, N_r):
    return ((1 - mi)*phi_b_max*D_b[0] + (1 - mi)*phi_b_max*D_b[1] + 2*d3*N_max - 2*d3*N_r)/(2*d3*N_max)


def u_d(D_a, D_b, mi, phi_a, phi_b, d3, d4, N, theta, N_r):
    return mi * (D_a[0]*theta*phi_a*N - D_a[1]*(1-theta)*phi_a*N - d3*((1-theta)*N - N_r)**2 - d4*N) + \
        (1-mi) * (D_b[0]*theta*phi_b*N - D_b[1]*(1-theta)*phi_b*N - d3*((1-theta)*N - N_r)**2 - d4*N)


def u_a(A, theta, phi, N):
    return A[0]*(1-theta)*phi*N - A[1]*theta*phi*N - A[2]*phi*N


def get_random_profiles():
    d3 = rn.random()
    d4 = rn.random()
    A_a = [0]*3
    A_b = [0]*3
    D_a = [0]*2
    D_b = [0]*2

    A_a[0] = rn.random()
    A_a[1] = rn.random() * A_a[0]
    A_a[2] = rn.random() * A_a[1]

    D_a[0] = rn.random()
    D_a[1] = D_a[0] * rn.random()

    A_b[1] = rn.random()
    A_b[0] = rn.random() * A_a[1]
    A_b[2] = rn.random() * A_a[0]

    D_b[1] = rn.random()
    D_b[0] = D_a[1] * rn.random()

    return A_a, A_b, D_a, D_b, d3, d4


def get_equilibrium(D_a, D_b, A_a, A_b, phi_a_max, phi_b_max, mi, d3, d4, N_r, N_max, all_branches=False):
    theta1 = get_theta_1(D_a, D_b, mi, phi_a_max, phi_b_max, d3, N_max, N_r)
    theta2 = get_theta_2(D_a, mi, phi_a_max, d3, N_max, N_r)
    theta3 = get_theta_3(D_b, mi, phi_b_max, d3, N_max, N_r)

    if 0 <= theta1 <= 1 and mi * D_a[0] * phi_a_max + D_b[0] * phi_b_max * (1 - mi) >= d4 and \
        -mi * (D_a[0] + D_a[1]) * phi_a_max + (mi - 1) * (D_b[0] + D_b[1]) * phi_b_max + 2 * d3 * N_r >= \
        (2 * d3 * (A_a[1] + A_a[2]) * N_max) / (A_a[0] + A_a[1]) and \
        -mi * (D_a[0] + D_a[1]) * phi_a_max + (mi - 1) * (D_b[0] + D_b[1]) * phi_b_max + 2 * d3 * N_r >= \
            (2 * d3 * (A_b[1] + A_b[2]) * N_max) / (A_b[0] + A_b[1]):

        print("I'm in branch 1")
        theta_optimal = theta1
        N_optimal = N_max
        phi_a_optimal = phi_a_max
        phi_b_optimal = phi_b_max
        U_d_optimal = u_d(D_a, D_b, mi, phi_a_optimal, phi_b_optimal, d3, d4, N_optimal, theta_optimal, N_r)
        U_a_a_optimal = u_a(A_a, theta_optimal, phi_a_optimal, N_optimal)
        U_a_b_optimal = u_a(A_b, theta_optimal, phi_b_optimal, N_optimal)

        return ({
            "mi": mi,
            "N": N_optimal,
            "U_d": U_d_optimal,
            "U_a_a": U_a_a_optimal,
            "U_a_b": U_a_b_optimal,
            "theta": theta1,
            "phi_a": phi_a_optimal,
            "phi_b": phi_b_optimal
        })

    elif A_a[0] > A_a[2] and A_b[0] > A_b[2] and 0 <= theta2 <= 1 and mi * phi_a_max * D_a[0] >= d4 and \
            (A_a[0] + A_a[1]) * (2 * d3 * N_r - mi * phi_a_max * (D_a[0] + D_a[1])) / (d3 * (A_a[1] + A_a[2])) >= \
            N_max >= (A_b[0] + A_b[1]) * (2 * d3 * N_r - mi * phi_a_max * (D_a[0] + D_a[1])) / (d3 * (A_a[1] + A_a[2])):

        print("I'm in branch 5")
        theta_optimal = theta2
        N_optimal = N_max
        phi_a_optimal = phi_a_max
        phi_b_optimal = 0
        U_d_optimal = u_d(D_a, D_b, mi, phi_a_optimal, phi_b_optimal, d3, d4, N_optimal, theta_optimal, N_r)
        U_a_a_optimal = u_a(A_a, theta_optimal, phi_a_optimal, N_optimal)
        U_a_b_optimal = u_a(A_b, theta_optimal, phi_b_optimal, N_optimal)

        return ({
            "mi": mi,
            "N": N_optimal,
            "U_d": U_d_optimal,
            "U_a_a": U_a_a_optimal,
            "U_a_b": U_a_b_optimal,
            "theta": theta_optimal,
            "phi_a": phi_a_optimal,
            "phi_b": phi_b_optimal
        })

    elif A_a[0] > A_a[2] and A_b[0] > A_b[2] and 0 <= theta3 <= 1 and (1 - mi) * phi_b_max * D_b[0] >= d4 and \
            (A_a[0] + A_a[1]) * (2 * d3 * N_r - mi * phi_a_max * (D_a[0] + D_a[1])) / (d3 * (A_a[1] + A_a[2])) <= \
            N_max <= (A_b[0] + A_b[1]) * (2 * d3 * N_r - mi * phi_a_max * (D_a[0] + D_a[1])) / (d3 * (A_a[1] + A_a[2])):

        print("I'm in branch 7")
        theta_optimal = theta3
        N_optimal = N_max
        phi_a_optimal = 0
        phi_b_optimal = phi_b_max
        U_d_optimal = u_d(D_a, D_b, mi, phi_a_optimal, phi_b_optimal, d3, d4, N_optimal, theta_optimal, N_r)
        U_a_a_optimal = u_a(A_a, theta_optimal, phi_a_optimal, N_optimal)
        U_a_b_optimal = u_a(A_b, theta_optimal, phi_b_optimal, N_optimal)

        return ({
            "mi": mi,
            "N": N_optimal,
            "U_d": U_d_optimal,
            "U_a_a": U_a_a_optimal,
            "U_a_b": U_a_b_optimal,
            "theta": theta_optimal,
            "phi_a": phi_a_optimal,
            "phi_b": phi_b_optimal
        })

    # Non popular branches
    elif all_branches is True:
        if theta1 < 0 and A_a[0] > A_a[2] and A_b[0] > A_b[2] and \
                0 < N_r - (d4+D_b[1]*phi_b_max+D_a[1]*mi*phi_a_max-D_b[1]*mi*phi_b_max)/(2*d3) <= N_max:

            theta_optimal = 0
            N_optimal = N_r - (d4+D_b[1]*phi_b_max+D_a[1]*mi*phi_a_max-D_b[1]*mi*phi_b_max)/(2*d3)
            phi_a_optimal = phi_a_max
            phi_b_optimal = phi_b_max
            U_d_optimal = u_d(D_a, D_b, mi, phi_a_optimal, phi_b_optimal, d3, d4, N_optimal, theta_optimal, N_r)
            U_a_a_optimal = u_a(A_a, theta_optimal, phi_a_optimal, N_optimal)
            U_a_b_optimal = u_a(A_b, theta_optimal, phi_b_optimal, N_optimal)
            print("I'm in branch 2")

            return ({
                "mi": mi,
                "N": N_optimal,
                "U_d": U_d_optimal,
                "U_a_a": U_a_a_optimal,
                "U_a_b": U_a_b_optimal,
                "theta": theta_optimal,
                "phi_a": phi_a_optimal,
                "phi_b": phi_b_optimal
            })
        elif theta1 < 0 and N_r - (d4+D_b[1]*phi_b_max+D_a[1]*mi*phi_a_max-D_b[1]*mi*phi_b_max)/(2*d3) > N_max \
            and A_a[0] > A_a[2] and A_b[0] > A_b[2]:
            print("I'm in branch 3")

            theta_optimal = 0
            N_optimal = N_max
            phi_a_optimal = phi_a_max
            phi_b_optimal = phi_b_max
            U_d_optimal = u_d(D_a, D_b, mi, phi_a_optimal, phi_b_optimal, d3, d4, N_optimal,theta_optimal, N_r)
            U_a_a_optimal = u_a(A_a, theta_optimal, phi_a_optimal, N_optimal)
            U_a_b_optimal = u_a(A_b, theta_optimal, phi_b_optimal, N_optimal)

            return ({
                "mi": mi,
                "N": N_optimal,
                "U_d": U_d_optimal,
                "U_a_a": U_a_a_optimal,
                "U_a_b": U_a_b_optimal,
                "theta": theta_optimal,
                "phi_a": phi_a_optimal,
                "phi_b": phi_b_optimal
            })
        elif theta1 < 0 and A_a[0] > A_a[2] and A_b[0] > A_b[2] and N_r < \
            (d4+D_b[1]*phi_b_max+D_a[1]*mi*phi_a_max-D_b[1]*mi*phi_b_max)/(2*d3):
            print("I'm in branch 4")

            theta_optimal = 0
            N_optimal = 0
            phi_a_optimal = phi_a_max
            phi_b_optimal = phi_b_max
            U_d_optimal = u_d(D_a, D_b, mi, phi_a_optimal, phi_b_optimal, d3, d4, N_optimal, theta_optimal, N_r)
            U_a_a_optimal = u_a(A_a, theta_optimal, phi_a_optimal, N_optimal)
            U_a_b_optimal = u_a(A_b, theta_optimal, phi_b_optimal, N_optimal)

            return ({
                "mi": mi,
                "N": N_optimal,
                "U_d": U_d_optimal,
                "U_a_a": U_a_a_optimal,
                "U_a_b": U_a_b_optimal,
                "theta": theta_optimal,
                "phi_a": phi_a_optimal,
                "phi_b": phi_b_optimal
            })
        elif theta1 < 0 and A_a[0] > A_a[2] and A_b[0] > A_b[2] and N_r < (d4+mi*D_a[1]*phi_a_max) / (2 * d3):
            print("I'm in branch 6")

            theta_optimal = 0
            N_optimal = 0
            phi_a_optimal = phi_a_max
            phi_b_optimal = phi_b_max
            U_d_optimal = u_d(D_a, D_b, mi, phi_a_optimal, phi_b_optimal, d3, d4, N_optimal, theta_optimal, N_r)
            U_a_a_optimal = u_a(A_a, theta_optimal, phi_a_optimal, N_optimal)
            U_a_b_optimal = u_a(A_b, theta_optimal, phi_b_optimal, N_optimal)

            return ({
                "mi": mi,
                "N": N_optimal,
                "U_d": U_d_optimal,
                "U_a_a": U_a_a_optimal,
                "U_a_b": U_a_b_optimal,
                "theta": theta_optimal,
                "phi_a": phi_a_optimal,
                "phi_b": phi_b_optimal
            })
        elif theta3 < 0 and A_a[0] > A_a[2] and A_b[0] > A_b[2] and N_r < (d4+(1-mi)*D_b[1]*phi_b_max) / (2 * d3):
            print("I'm in branch 8")

            theta_optimal = 0
            N_optimal = 0
            phi_a_optimal = phi_a_max
            phi_b_optimal = phi_b_max
            U_d_optimal = u_d(D_a, D_b, mi, phi_a_optimal, phi_b_optimal, d3, d4, N_optimal, theta_optimal, N_r)
            U_a_a_optimal = u_a(A_a, theta_optimal, phi_a_optimal, N_optimal)
            U_a_b_optimal = u_a(A_b, theta_optimal, phi_b_optimal, N_optimal)

            return ({
                "mi": mi,
                "N": N_optimal,
                "U_d": U_d_optimal,
                "U_a_a": U_a_a_optimal,
                "U_a_b": U_a_b_optimal,
                "theta": theta_optimal,
                "phi_a": phi_a_optimal,
                "phi_b": phi_b_optimal
            })
        else:
            return None
    else:
        return None
