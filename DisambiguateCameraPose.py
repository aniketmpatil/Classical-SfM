from IPython import embed


def check_cheirality(C, R, X_list):
    max_points = 0

    C = C.reshape((3,1))

    r3 = R[:,2]
    r3 = r3.reshape((3,1))

    # embed()

    count_points = 0
    for X in X_list:
        X = X.reshape((3,1))

        check1 = X[2]
        check2 = r3.T @ (X - C)
        if(check1 > 0 and check2 > 0):
            count_points += 1
    
    return count_points

