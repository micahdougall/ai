def marginalize(
        this_given_other: float, other: float, not_other_given_not_this: float
) -> float:
    return (
        this_given_other * other
        + ((1 - not_other_given_not_this) * (1 - other))
    )


def bayesian_probability(
        likelihood: float, prior: float, marginalization: float
) -> float:
    return likelihood * prior / marginalization


if __name__ == '__main__':
    iterations = 3
    b_given_a = 0.97
    a = .005
    not_a_given_not_b = .95
    for i in range(iterations):
        b = marginalize(b_given_a, a, not_a_given_not_b)
        a = bayesian_probability(b_given_a, a, b)
        print(f"Posterior: {a}")
