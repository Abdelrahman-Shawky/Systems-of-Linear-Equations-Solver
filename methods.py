import numpy as np
import sys


def selectMethod(method_name, entries, n, tol=0.00001, max_iterations=50):
    if method_name == "Gaussian-Elimination":
        return gauss_elimination(entries,n)
    elif method_name == "Gauss-Seidel":
        return gauss_seidel(entries, n, tol, max_iterations)
    elif method_name == "Gaussian-Jordan":
        return gauss_jordan(entries, n)


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

    return x



def gauss_seidel(entries, n, tol, max_iterations):
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
    errors = np.zeros(n)
    count = 1
    # Convert entries to input array
    for i in range(n):
        for j in range(n + 1):
            a[i][j] = float(entries[k])
            k += 1

    condition = True

    while condition:
        # x1 = (a[0][n] - a[0][1]*y0 - a[0][2]*z0)/a[0][0]
        # y1 = (a[1][n] - a[1][0]*x1 - a[1][2]*z0)/a[1][1]
        # z1 = (a[2][n] - a[2][0]*x1 - a[2][1]*y1)/a[2][2]

        for i in range(n):
            x1 = a[i][n]
            for j in range(n):
                if i == j:
                    continue
                x1 -= a[i][j]*current[j]
            x1 /= a[i][i]
            errors[i] = abs(current[i] - x1)
            current[i] = x1


        print('%d\t%0.4f\t%0.4f\t%0.4f\n' % (count, current[0], current[1], current[2]))
        # e1 = abs(x0 - x1)
        # e2 = abs(y0 - y1)
        # e3 = abs(z0 - z1)

        for i in range(n):
            if errors[i] < tol:
                condition = False

        count += 1
        # x0 = x1
        # y0 = y1
        # z0 = z1

        if count == max_iterations:
            break
        # condition = e1 > tol and e2 > tol and e3 > tol

    x = np.zeros(n)
    x[0] = x0
    x[1] = y0
    x[2] = z0
    return current



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

    return x


