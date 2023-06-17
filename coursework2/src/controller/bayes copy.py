
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


# if __name__ == '__main__':
#     iterations = 3
#     b_given_a = 0.97
#     a = .005
#     not_a_given_not_b = .95
#     for i in range(iterations):
#         b = marginalize(b_given_a, a, not_a_given_not_b)
#         a = bayesian_probability(b_given_a, a, b)
#         print(f"Posterior: {a}")


def bayes_probability(
        prior: float, 
        sensitivity: float,
        specificity_complement: float
) -> float:
    marginalised = (
        sensitivity * prior
        + ((1 - specificity_complement) * (1 - prior))
    )
    return sensitivity * prior / marginalised

# def bayes_probability(
#         known: float, 
#         unknown_given_known: float,
#         not_known_given_not_unknown: float
# ) -> float:
#     marginalised = (
#         unknown_given_known * known
#         + ((1 - not_known_given_not_unknown) * (1 - known))
#     )
#     return unknown_given_known * known / marginalised

import math


sq_prob_of_risk = .25

print(f"sq_prob_of_risk: {sq_prob_of_risk}")

sq_prob_not_risk = 1 - sq_prob_of_risk

sq_prob_no_percept = math.pow(sq_prob_not_risk, 3) # 3 adjacent squares
sq_prob_percept = 1 -  sq_prob_no_percept

print(f"sq_prob_percept: {sq_prob_percept}")

sq_prob_given_percept = 1/3
print(f"sq_prob_given_percept: {sq_prob_given_percept}")


posterior = bayes_probability(sq_prob_of_risk, sq_prob_given_percept, 0)
print(f"prob: {posterior}")


def naive_bayes(likelihood, prior, marginalisation):
    return likelihood * prior / marginalisation


sq_prob_of_risk = naive_bayes(1, sq_prob_of_risk, sq_prob_percept)
print(f"naive: {sq_prob_of_risk}")



sensitivity = 1
specificity = math.pow(sq_prob_not_risk, 3)
specificity_complement = 1 - specificity

sq_prob_of_risk = bayes_probability(sq_prob_of_risk, 1, specificity_complement)


