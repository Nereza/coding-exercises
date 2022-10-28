
def calculate_fib_iterative(n):
    """
    Calculates the n-th Fibonacci number in an iterative way, by remembering the previous number and summing them up.
    :param n: the index of the requested number within the Fibonacci sequence
    :return: the requested Fibonacci number
    """
    if n < 0:
        raise ValueError('n must be a positive number')
    if n < 2:
        current_fib = n
    else:
        current_fib = 1
        previous_fib = 0
        for i in range(2, n+1):
            tmp = current_fib
            current_fib += previous_fib
            previous_fib = tmp
    print(f'Die Fibonacci-Zahl für {n} ist: {current_fib}')
    return current_fib


if __name__ == '__main__':
    for i in range(20):
        print(calculate_fib_iterative(i))
