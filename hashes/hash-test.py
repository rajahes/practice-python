import string
import random
import scipy
import matplotlib.pyplot as plt

# This script will test multiple hashes on strings to see if we get a uniform distribution


def load_words():
    words = {}
    exclude = set(string.punctuation + "\n")
    word_count = 0

    with open("tale-of-two-cities.txt", "r") as content:
        for line in content:
            line = line.replace("--", ' ')
            line_words = line.split(" ")
            for word in line_words:
                word = ''.join(ch for ch in word if ch not in exclude)

                # add to dict and keep track of times it occurs
                if word:
                    word = word.lower()
                    word_count += 1
                    if word in words:
                        words[word] += 1
                    else:
                        words[word] = 1

    return words


def is_prime(n):
    """
    Function which returns True if the integer n is prime. Tests integers
    d from two up to Dmax = scipy.sqrt(n), stopping if any are divisors of n
    (or, test if n is even and then test odd divisors). This is most naturally
    done using the "while" command,
      while n%d != 0 and d <= Dmax:
          d+=1		[or 2]
    What condition will d satisfy after the while loop if n is prime?
    """
    Dmax = scipy.sqrt(n)
    if n == 2:
        return True
    if n %2 == 0:
        return False
    d = 3
    while n % d != 0 and d <= Dmax:
        d += 2
    return d > Dmax


def first_prime_greater_than(min):
    """
    Returns a list of all prime numbers less than nMax.
    You can use isPrime to generate a list of primes using the nice
    Python feature of "List comprehensions". For example, the squares of the
    even numbers between seven and nineteen can be generated by
        [n**2 for n in scipy.arange(7,19) if isEven(n)]
    List comprehensions return a list using the elements generated by the
    "for" loop that satisfy the (optional) if expression.
    """

    for n in scipy.arange(min + 1, min * 2):
        if is_prime(n):
            return n

    return None


def randomhash(m):
    random.seed()
    return random.randint(0, m - 1)


def polyhash_prime(word, a, p, m):
    hash = 0
    for c in word:
        hash = (hash * a + ord(c)) % p

    return hash % m


def polyhash_noprime(word, a, m):
    hash = 0
    for c in word:
        hash = (hash * a + ord(c))

    return hash % m



def show_distribution(buckets, title):

    counts = {}
    for v in buckets:
        if v in counts.keys():
            counts[v] += 1
        else:
            counts[v] = 1

    plt.bar(counts.keys(), counts.values())
    plt.title(title)
    plt.xlabel("Bucket size")
    plt.ylabel("Buckets")
    plt.show()


def main():
    words = load_words()
    word_count = len(words)

    m = int(word_count / 2)  # hash table will be at load = 0.5

    # random

    buckets = [0] * m
    for w in words:
        hash = randomhash(m)
        buckets[hash] += 1

    show_distribution(buckets, "Bucket size distribution - Random insert")

    # polyhash

    # we want a prime to use in hash calculation
    # 10145 distinct words in the book
    prime = first_prime_greater_than(word_count)

    buckets = [0] * m
    for w in words:
        hash = polyhash_prime(w, 31, prime, m)
        buckets[hash] += 1

    show_distribution(buckets, "Bucket size distribution - PolyHash with prime")

    # polyhash, without prime

    buckets = [0] * m
    for w in words:
        hash = polyhash_noprime(w, 31, m)
        buckets[hash] += 1

    show_distribution(buckets, "Bucket size distribution - PolyHash, no prime")

if __name__ == "__main__":
    main()
