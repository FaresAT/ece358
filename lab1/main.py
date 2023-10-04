import numpy as np

# Lab 1
# M/M/1 and M/M/1/K Queue Simulation

lambda_gen = 75
max_variables = 1000

random_variables = np.random.exponential(lambda_gen, max_variables)

sample_mean = np.mean(random_variables)
sample_variance = np.var(random_variables)

print(sample_mean)
print(sample_variance)
