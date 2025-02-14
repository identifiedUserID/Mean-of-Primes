import random
import math

def generate_prime(n):
    """
    Generates a random n-digit prime number.

    Args:
        n: The number of digits in the desired prime number.

    Returns:
        An n-digit prime number, or None if n is invalid.
    """
    if not (1 <= n <= 25):
        return None

    lower_bound = 10**(n - 1)
    upper_bound = 10**n - 1

    while True:
        num = random.randint(lower_bound, upper_bound)
        if is_prime(num):
            return num

def is_prime(num):
    """
    Checks if a number is prime.

    Args:
        num: The number to check.

    Returns:
        True if num is prime, False otherwise.
    """
    if num <= 1:
        return False
    if num <= 3:
        return True
    if num % 2 == 0 or num % 3 == 0:
        return False
    i = 5
    while i * i <= num:
        if num % i == 0 or num % (i + 2) == 0:
            return False
        i += 6
    return True

def represent_as_average_of_primes(prime, k):
    """
    Tries to represent a prime number as an average of k prime numbers (excluding the prime itself).

    Args:
        prime: The prime number to represent.
        k: The number of prime numbers to average (k > 1).

    Returns:
        A list of k prime numbers whose average is close to the prime number, or None if not found.
    """
    if k <= 1:
        print("k must be greater than 1.")
        return None

    # Calculate the target sum
    target_sum = prime * k

    max_attempts = 10000

    for _ in range(max_attempts):
        # Generate k-1 random prime numbers (excluding the prime itself)
        primes = []
        for _ in range(k - 1):
            while True:
                num = random.randint(2, int(target_sum/2))
                if is_prime(num) and num != prime:
                    primes.append(num)
                    break

        # Calculate the last prime number needed
        last_prime_needed = target_sum - sum(primes)

        if is_prime(last_prime_needed) and last_prime_needed != prime:
            primes.append(last_prime_needed)

            # Check if the average is close to the prime
            average = sum(primes) / k
            if math.isclose(average, prime, rel_tol=1e-09):
                return primes

    return None

def main():
    """
    Main function to interact with the user.
    """
    while True:
        try:
            n = int(input("Enter the desired number of digits for the prime number (1-25): "))
            if 1 <= n <= 25:
                break
            else:
                print("Invalid input. Please enter a number between 1 and 25.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

    prime = generate_prime(n)
    print(f"Generated {n}-digit prime number: {prime}")

    while True:
        try:
            k = int(input("Enter the number of primes to average (k > 1): "))
            if k > 1:
                break
            else:
                print("k must be greater than 1.")
        except ValueError:
            print("Invalid input. Please enter an integer greater than 1.")

    result = represent_as_average_of_primes(prime, k)
    if result:
        print(f"The prime number {prime} can be approximately represented as the average of these {k} prime numbers:")
        print(result)
        print(f"Their average is: {sum(result)/k}")
    else:
        print(f"Could not find {k} prime numbers (excluding {prime}) whose average is close to {prime}.")

if __name__ == "__main__":
    main()