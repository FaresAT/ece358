import numpy as np

lambda_gen = 75
max_variables = 1000

expected_mean = 1/lambda_gen
expected_variance = 1/(lambda_gen**2)

random_variables = np.random.exponential(1/lambda_gen, max_variables)

actual_mean = np.mean(random_variables)
actual_variance = np.var(random_variables)

tolerance = 0.05
if abs(actual_mean - expected_mean) < tolerance*expected_mean and abs(actual_variance - expected_variance) < tolerance*expected_variance:
    print("works correctly, values are within a 5 percent range of whats expected")
else:
    print("doesn't work correctly, values are not within a 5 percent range of whats expected")

