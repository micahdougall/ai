def bayes_probability(
        prior: float, 
        specificity: float,
        sensitivity: float = 1 # Percept always occurs for positives
) -> float:
    marginalised = (
        sensitivity * prior
        + ((1 - specificity) * (1 - prior))
    )
    return sensitivity * prior / marginalised
