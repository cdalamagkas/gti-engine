import random as rn
import cvxpy as cp
import math as mth

# GTI (Game Theoretic Intelligence)
# === INPUTS:
# N_r:                         Number of connected real devices
# N_max:                       Maximum number of connected honeypots and real devices (this number can be limited
#                                  either due to available public IPs or due to limited computational resources)
# bias_plug_out_real_device:   (Optional) A boolean that indicates if a bias should be activates that makes impossible
#                                  for the GTI engine to suggest the plugging out of a real device
# max_tries               (Optional) How many times should GTI try with random a and d in order to find Nash equilibrium
# a, d                         (Optional) Determine specific values for a, d
# attacker_known               (Optional) Boolean value to indicate if the attacker (thus the a values) should be
#                                  considered as known by the GTI engine
# === OUTPUT:
# n*theta                      Number of honeypots (rounded to accomplish the best possible utility)
# real_devices_to_disconnect   (Optional) Number of real devices that should be disconnected

def gti(n_r, n_max, bias_plug_out_real_device=False, max_tries=2000, a=None, d=None, attacker_known=True):

    # ========================== METHODS DEFINITION ====================================================================

    # Returns the optimal value of theta according to the equilibrium (equation 13, branch 4)
    def get_theta_optimal():
        return (d1 + d2 + 2 * d3 * n_max - 2 * d3 * n_r) / (2 * d3 * n_max)

    # Returns random values of a that satisfy some general relations imposed by the equilibrium (equation 13, branch 4)
    def get_random_a():  # return random values for (a1, a2, a3)
        _a1 = rn.random()
        return [_a1, rn.random() * _a1, rn.random()]

    # Returns random values of d that satisfy some general relations imposed by the equilibrium (equation 13, branch 4)
    def get_random_d():  # return random values for (d1, d2, d3, d4)
        _d1 = rn.random()
        if bias_plug_out_real_device:
            _d3 = 1000
        else:
            _d3 = rn.random()
        return [_d1, rn.random(), _d3, rn.random() * _d1]

    # Checks whether the combination of d, a, n_max and n_r satisfies the condition of the Nash equilibrium (equation 13
    # branch 4)
    def parameters_valid():
        if 0 <= (d1 + d2 + 2 * d3 * n_max - 2 * d3 * n_r) / (2 * d3) <= n_max and d1 > d4 and \
                (a1 + a2) * n_r >= (a2 + a3) * n_max + ((a1 + a2) * (d1 + d2)) / (2 * d3) and a1 > a3:
            return True
        else:
            return False

    # Max-min algorithm to determine optimal n, theta if Nash equilibrium does not exist
    def maxmin():
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

        # 1.3 By solving the system of n1, n2, we get theta and n
        _n = n1.value + n2.value
        _theta = n1.value / (n1.value + n2.value)
        return [_n, _theta]

    # Utility function for the defender
    def u_d(phi=1):
        return d1 * theta * phi * n - d2 * (1 - theta) * phi * n - d3 * ((1 - theta) * n - n_r) ** 2 - d4 * n

    # If the sum of honeypots (n*theta) and real devices exceed N_max, then some real devices should be disconnected
    def get_real_devices_to_disconnect():
        if n*theta + n_r > n_max:
            return n_max - n*theta
        else:
            return 0

    # Checks if the inserted parameters are valid -- IF NOT, ERROR CODE 10 IS RETURNED
    def validation_check():
        if not 0 < n_r <= n_max:
            print("INVALID INPUT: N_r and N_max should be greater than zero and N_r should be less or equal than N_max")
            exit(10)
        elif a is not None:
            for i in range(0, a.__len__()):
                if not 0 <= a[i] <= 1:
                    print("INVALID INPUT: a should be between 0 and 1")
                    exit(10)
        elif d is not None:
            for i in range(0, d.__len__()):
                if not 0 <= d[i] <= 1 and i is not 2:  # d3 is allowed to be greater than 1 in order to bias the result
                    print("INVALID INPUT: d should be between 0 and 1")
                    exit(10)
        elif max_tries < 0:
            print("INVALID INPUT: max_tries should be > 0")
            exit(10)

    # ====================================END METHODS DEFINITION========================================================

    validation_check()
    print("Inputs are valid. Proceeding to the next step...")

    tries = 0
    # CASE 1: The attacker strategy is unknown, the maxmin strategy is activated, instead of the Nash equilibrium.
    if attacker_known is False:
        print("Maxmin option is chosen since the attacker is unknown")
        # Iteratively try to select valid a and d in order to satisfy the Nash equilibrium conditions (not required)
        while True:
            if d is not None:
                d1 = d[0]
                d2 = d[1]
                d3 = d[2]
                d4 = d[3]
            else:
                d1, d2, d3, d4 = get_random_d()

            a1, a2, a3 = get_random_a()
            if parameters_valid():
                break

        # Solve the convex optimisation problem to get theta and n.
        n, theta = maxmin()

    # CASE 2: The attacker is known, therefore a Nash equilibrium could exist
    else:
        if a is not None:
            a1 = a[0]
            a2 = a[1]
            a3 = a[2]

        if d is not None:
            d1 = d[0]
            d2 = d[1]
            d3 = d[2]
            d4 = d[3]

        # If both a and d have been determined, do not enter the loop, check instantly if they are valid
        if a is not None and d is not None:
            if parameters_valid():
                theta = get_theta_optimal()
                n = n_max
            else:
                print("Provided parameters a and d do not give equilibrium. Choosing the max-min option...")
                n, theta = maxmin()
        else:
            # Iteratively, try to find appropriate a and d to satisfy branch 4 of Nash equilibrium (equation 13)
            while True:
                if a is None:
                    a1, a2, a3 = get_random_a()

                if d is None:
                    d1, d2, d3, d4 = get_random_d()

                if parameters_valid():
                    print("Equilibrium is found!")
                    theta = get_theta_optimal()
                    n = n_max
                    break

                if tries > max_tries:
                    print("No equilibrium was found. Choosing the max-min option...")
                    n, theta = maxmin()
                    break

                tries += 1

    # We need to choose an integer, so we round up to the nearest integer and choose the solutions that gives the
    # greater utility
    honeypots_ceil = mth.ceil(n*theta)
    honeypots_floor = mth.floor(n*theta)

    theta = honeypots_ceil/n
    utility_ceil = u_d()

    theta = honeypots_floor/n
    utility_floor = u_d()

    if utility_ceil > utility_floor:
        return [honeypots_ceil, get_real_devices_to_disconnect()]
    else:
        return [honeypots_floor, get_real_devices_to_disconnect()]
