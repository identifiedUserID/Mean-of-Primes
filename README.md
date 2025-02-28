# Mean Relations Among Primes: A Novel Conjecture on Prime Averages

## Abstract

In this paper we explore a new, undiscovered concept in number theory, where **any prime number greater than 3** can be represented as the arithmetic mean of at least one pair of distinct prime numbers. Our conjecture extends the existing research of prime number relationships, offering a unique perspective on their distribution and connectivity. Initial examples provided across various prime magnitudes support the conjecture, with a thorough examination included for both smaller and significantly larger primes using computer algorithms..

## Introduction

Prime numbers, the building blocks of natural numbers, have been extensively studied for their inherent properties and the mysteries surrounding their distribution. Beyond classical results and conjectures such as the Goldbach Conjecture, researchers continuously seek new relationships and patterns among primes. Our paper proposes a new conjecture, which posits that any prime number greater than 3 serves as the arithmetic mean of at least one pair of distinct primes.

# Conjecture

For any prime number $p$ greater than 3, there exist at least two distinct prime numbers $p_1$ and $p_2$ such that:

$$
p = \frac{p_1 + p_2}{2}
$$

This formulation suggests a symmetric relationship around prime numbers, indicating a kind of "prime balance" that has not been previously documented in the literature.

# Detailed Examination and Examples

To illustrate and support the conjecture, various examples across different magnitudes of prime numbers are provided. In each case, we determine two distinct primes that sum to twice the target prime, thereby satisfying the condition:

$$
p_1 + p_2 = 2p
$$

## Small Primes

- **5**: Here, $2 \times 5 = 10$. The prime pair $(3, 7)$ satisfies $3 + 7 = 10$, so $5 = \frac{3 + 7}{2}$.
- **11**: For $2 \times 11 = 22$, the prime pair $(3, 19)$ satisfies $3 + 19 = 22$, hence $11 = \frac{3 + 19}{2}$.

## Medium-sized Primes

- **103**: With $2 \times 103 = 206$, the prime pair $(79, 127)$ satisfies $79 + 127 = 206$, yielding $103 = \frac{79 + 127}{2}$.

## Four-digit Prime

- **1,061**: Here, $2 \times 1,061 = 2,122$. The pair $(251, 1,871)$ satisfies $251 + 1,871 = 2,122$, resulting in $1,061 = \frac{251 + 1,871}{2}$.

## Five-digit Prime

- **30,011**: For $2 \times 30,011 = 60,022$, the prime pair $(22,511, 37,511)$ satisfies $22,511 + 37,511 = 60,022$, so $30,011 = \frac{22,511 + 37,511}{2}$.

These examples demonstrate the systematic process of identifying two prime numbers—one smaller and one larger than the target—whose sum is exactly twice the target prime. This method validates the conjecture across a wide range of prime magnitudes.

## Project Video

[![Watch the video](https://img.youtube.com/vi/LanqOKW7vic/0.jpg)](https://www.youtube.com/watch?v=LanqOKW7vic)

## Code Overview

The complete source code is available in the repository. Below are the main functions with explanations of their roles:

### 1. User Interaction: `main()`

The `main()` function handles user interaction and orchestrates the overall process. It performs the following tasks:
- **Input Validation:** Prompts the user for the desired number of digits for the prime and ensures the input is within the valid range (1–25).
- **Prime Generation:** Calls the prime generation function to obtain a random prime number of the specified digit length.
- **Averaging Primes:** Asks for the number of primes \( k \) to average and validates that \( k > 1 \).
- **Result Display:** Invokes the function to represent the generated prime as an average of \( k \) prime numbers, and then displays the result.

```python
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
```

### 2. Prime Generation and Checking

#### a. Prime Generation: `generate_prime(n)`

This function generates a random prime number with 
𝑛 n digits. It computes the appropriate lower and upper bounds for 𝑛 n-digit numbers and then randomly selects numbers within that range until a prime is found.

```python
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
```

#### b. Prime Checking `is_prime(num)`

This function determines if a given number is prime by checking for divisibility up to its square root. It efficiently eliminates non-prime candidates.

```python
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

```

### 3. Representing a Prime as an Average: `represent_as_average_of_primes(prime, k)`

This function attempts to express a given prime number as the average of 
𝑘
k prime numbers (excluding the prime itself). It calculates the target sum (i.e., 
𝑝
𝑟
𝑖
𝑚
𝑒
×
𝑘
prime×k) and then searches for 
𝑘
−
1
k−1 random primes. The final prime required to meet the target sum is computed and validated. If the set of primes meets the condition (their average is close to the target prime), the function returns the list of primes.

```python
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

```


