import multistage.gti_engine_multistage as gti
import random


def gti_multistage_measurement(mi, phi_a_max, phi_b_max, max_rounds, N_r, N_max, type_of_the_real_attacker='r', D_a=None, D_b=None, A_a=None, A_b=None, d3=None, d4=None):
    history_equilibrium = []

    if D_a is None and D_b is None and A_a is None and A_b is None and d3 is None and d4 is None:
        while True:
            A_a, A_b, D_a, D_b, d3, d4 = gti.get_random_profiles()
            equilibrium = gti.get_equilibrium(D_a, D_b, A_a, A_b, phi_a_max, phi_b_max, mi, d3, d4, N_r, N_max)
            if equilibrium is not None:
                history_equilibrium.append(equilibrium)
                break
            else:
                continue
    else:
        equilibrium = gti.get_equilibrium(D_a, D_b, A_a, A_b, phi_a_max, phi_b_max, mi, d3, d4, N_r, N_max)
        if equilibrium is not None:
            history_equilibrium.append(equilibrium)
        else:
            print("FATAL: Provided parameters do not give equilibrium")
            exit(-10)

    counter = 0
    attacker_type = 'a'
    rounds_before_changing = 5
    for current_round in range(1, max_rounds):
        sum = 0
        if type_of_the_real_attacker == 'r':
            if counter % rounds_before_changing == 0:
                if attacker_type == 'a':
                    attacker_type = 'b'
                    rounds_before_changing = rounds_before_changing + 5
                else:
                    attacker_type = 'a'
            counter += 1
        else:
            attacker_type = type_of_the_real_attacker

        if attacker_type == 'a':
            for i in range(0, round(equilibrium['N'])):
                rnd = random.random()
                if rnd <= equilibrium["phi_a"]:
                    attacked = 1
                else:
                    attacked = 0
                sum += attacked
        elif attacker_type == 'b':
            for i in range(1, round(equilibrium['N'])):
                rnd = random.random()
                if rnd <= equilibrium["phi_b"]:
                    attacked = 1
                else:
                    attacked = 0
                sum += attacked
        else:
            print("ERROR")
            exit(-10)

        phi_t_x_N = sum

        term_a = (mi * (equilibrium['phi_a']**phi_t_x_N)) * ((1 - equilibrium['phi_a']) ** (equilibrium['N'] - phi_t_x_N))
        term_b = ((1-mi) * (equilibrium['phi_b']**phi_t_x_N)) * ((1 - equilibrium['phi_b']) ** (equilibrium['N'] - phi_t_x_N))

        mi = term_a / (term_a + term_b)

        equilibrium = gti.get_equilibrium(D_a, D_b, A_a, A_b, phi_a_max, phi_b_max, mi, d3, d4, N_r, N_max,
                                          all_branches=False)

        if equilibrium is None:
            print("Fatal error: No equilibrium found")
            return None, None

        equilibrium['current_type_of_attacker'] = attacker_type

        history_equilibrium.append(equilibrium)

    parameters = {
        "phi_a_max": phi_a_max,
        "phi_b_max": phi_b_max,
        "max_rounds": max_rounds,
        "N_r": N_r,
        "N_max": N_max,
        "A_a_1": A_a[0],
        "A_a_2": A_a[1],
        "A_a_3": A_a[2],
        "A_b_1": A_b[0],
        "A_b_2": A_b[1],
        "A_b_3": A_b[2],
        "D_a_1": D_a[0],
        "D_a_2": D_a[1],
        "D_b_1": D_b[0],
        "D_b_2": D_b[1],
        "d_3": d3,
        "d_4": d4,
        "type_of_the_real_attacker": type_of_the_real_attacker
    }

    return history_equilibrium, parameters
