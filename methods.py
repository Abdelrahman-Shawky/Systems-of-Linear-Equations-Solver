import pprint
import numpy as np
import time
import sys
import scipy
import scipy.linalg


def selectMethod(method_name, entries, n, initial, tol=0.00001, max_iterations=50):
    if method_name == "Gaussian-Elimination":
        return gauss_elimination(entries,n)
    elif method_name == "Gauss-Seidel":
        return gauss_seidel(entries, n, tol, max_iterations, initial)
    elif method_name == "Gaussian-Jordan":
        return gauss_jordan(entries, n)
    elif method_name == "LU Decomposition":
        return LU_decomposition(entries, n)


def LU_decomposition(entries, n):
    print(entries)
    # Making numpy array of n x n+1 size and initializing
    # to zero for storing augmented matrix
    a = np.zeros((n, n + 1))
    # Making numpy array of n size and initializing
    # to zero for storing solution vector
    x = np.zeros(n)
    k = 0

    # Convert entries to input array
    for i in range(n):
        for j in range(n + 1):
            a[i][j] = float(entries[k])
            k += 1

    start_time = time.time()
    P, L, U = scipy.linalg.lu(a)
    pprint.pprint(a)
    pprint.pprint(P)
    pprint.pprint(L)
    pprint.pprint(U)

    for i in range(n-1, -1, -1):
        print(i)
        x[i] = U[i][n]
        if i == (n - 1):
            x[i] /= U[i][n-1]
        else:
            for k in range(n-1, i, -1):
                x[i] -= U[i][k] * x[k]
            x[i] /= U[i][i]
            print(x[i])

    execution_time = time.time() - start_time
    dictionary = dict()
    dictionary['execution_time'] = str(execution_time)
    dictionary['result'] = x


    pprint.pprint(x)
    return dictionary


def gauss_jordan(entries, n):
    print(entries)
    # Making numpy array of n x n+1 size and initializing
    # to zero for storing augmented matrix
    a = np.zeros((n, n + 1))
    # Making numpy array of n size and initializing
    # to zero for storing solution vector
    x = np.zeros(n)
    k = 0

    # Convert entries to input array
    for i in range(n):
        for j in range(n + 1):
            a[i][j] = float(entries[k])
            k += 1

    start_time = time.time()
    # Applying Gauss Jordan Elimination
    for i in range(n):
        if a[i][i] == 0.0:
            sys.exit('Divide by zero detected!')

        for j in range(n):
            if i != j:
                ratio = a[j][i] / a[i][i]

                for k in range(n + 1):
                    a[j][k] = a[j][k] - ratio * a[i][k]

    # Obtaining Solution
    for i in range(n):
        x[i] = a[i][n] / a[i][i]

    execution_time = time.time() - start_time
    dictionary = dict()
    dictionary['execution_time'] = str(execution_time)
    dictionary['result'] = x
    return dictionary


def gauss_seidel(entries, n, tol, max_iterations, initial):
    print(entries)
    # Making numpy array of n x n+1 size and initializing
    # to zero for storing augmented matrix
    a = np.zeros((n, n + 1))
    k = 0
    # Initial zeroes
    x0 = 0
    y0 = 0
    z0 = 0
    current = np.zeros(n)
    for i in range(n):
        current[i] = float(initial[i])
    errors = np.zeros(n)
    count = 1
    # Convert entries to input array
    for i in range(n):
        for j in range(n + 1):
            a[i][j] = float(entries[k])
            k += 1

    condition = True

    start_time = time.time()
    while condition:
        for i in range(n):
            if a[i][i] == 0.0:
                sys.exit('Divide by zero detected!')
            x1 = a[i][n]
            for j in range(n):
                if i == j:
                    continue
                x1 -= a[i][j]*current[j]
            x1 /= a[i][i]
            errors[i] = abs(current[i] - x1)
            current[i] = x1

        for i in range(n):
            if errors[i] < tol:
                condition = False

        count += 1
        if count == max_iterations:
            break

    x = np.zeros(n)
    # x[0] = x0
    # x[1] = y0
    # x[2] = z0

    execution_time = time.time() - start_time
    dictionary = dict()
    dictionary['execution_time'] = str(execution_time)
    dictionary['result'] = current
    return dictionary


def gauss_elimination(entries, n):
    print(entries)
    # Making numpy array of n x n+1 size and initializing
    # to zero for storing augmented matrix
    a = np.zeros((n, n + 1))
    # Making numpy array of n size and initializing
    # to zero for storing solution vector
    x = np.zeros(n)
    k = 0
    # Convert entries to input array
    for i in range(n):
        for j in range(n + 1):
                a[i][j] = float(entries[k])
                k += 1

    start_time = time.time()
    # Applying Gauss Elimination
    for i in range(n):
        if a[i][i] == 0.0:
            sys.exit('Divide by zero detected!')

        for j in range(i + 1, n):
            ratio = a[j][i] / a[i][i]

            for k in range(n + 1):
                a[j][k] = a[j][k] - ratio * a[i][k]

    # Back Substitution
    x[n - 1] = a[n - 1][n] / a[n - 1][n - 1]

    for i in range(n - 2, -1, -1):
        x[i] = a[i][n]

        for j in range(i + 1, n):
            x[i] = x[i] - a[i][j] * x[j]

        x[i] = x[i] / a[i][i]

    execution_time = time.time() - start_time
    dictionary = dict()
    dictionary['execution_time'] = str(execution_time)
    dictionary['result'] = x
    return dictionary


