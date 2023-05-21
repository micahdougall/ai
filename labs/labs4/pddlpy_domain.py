import pddlpy

domain_problem = pddlpy.DomainProblem("domain.pddl", "problem.pddl")

domain_problem.initialstate()

print(list(domain_problem.operators()))

print(list(domain_problem.ground_operator("move")))
