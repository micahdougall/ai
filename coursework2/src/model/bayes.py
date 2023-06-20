
def bayes_probability(
        prior: float, 
        specificity: float,
        sensitivity: float = 1  # Percept always occurs for positives
) -> float:
    """Calculates the Bayesian probability for a required posterior.

    Args:
        prior: the prior probability.
        specificity: the specificity - true negative rate.
        sensitivity: the sensitivity - true positive rate.

    Returns:
        the new probability (posterior).
    """
    if prior == 0:
        return 0
    else:
        marginalised = (
            sensitivity * prior
            + ((1 - specificity) * (1 - prior))
        )
        return sensitivity * prior / marginalised
