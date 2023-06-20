from enum import Enum

# Enum Class for Algorithm type
Algorithm = Enum(
    'Algorithm',
    'STANDARD BAYES'
)

# Enum Class for Percept type
Percept = Enum(
    'Percept',
    'BORING DRONING SUCCESS'
)

# Enum Class for Risk type
Risk = Enum(
    'Risk',
    'BOOK FILIPPOS'
)

# Enum Class for Square state type
State = Enum(
    'State',
    'UNKNOWN SAFE VISITED BOOK FILIPPOS RISK'
)