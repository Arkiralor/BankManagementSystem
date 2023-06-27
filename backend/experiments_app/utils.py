from experiments_app import logger


def find_prime_numbers(lower_bound: int, upper_bound: int) -> None:
    logger.info(
        f"Finding prime numbers between {lower_bound} and {upper_bound}")
    for number in range(lower_bound, upper_bound + 1):
        if number > 1:
            for i in range(2, number//2):
                if (number % i) == 0:
                    break
            else:
                logger.info(f"Prime Number Found: {number}")
