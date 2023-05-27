import pddlpy

domain_problem = pddlpy.DomainProblem("domain.http", "problem.http")

domain_problem.initialstate()

print(list(domain_problem.operators()))

print(list(domain_problem.ground_operator("move")))
