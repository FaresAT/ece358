import numpy as np
import matplotlib.pyplot as plt

class MM1QueueSimulator:
    def __init__(self, lambda_, mu, T, observer_rate):
        self.lambda_ = lambda_
        self.mu = mu
        self.T = T
        self.queue = []
        self.current_time = 0
        self.next_arrival_time = np.random.exponential(1 / self.lambda_)
        self.next_departure_time = float('inf')
        self.next_observer_time = np.random.exponential(1 / observer_rate)
        self.Na = 0
        self.Nd = 0
        self.No = 0
        self.total_packets_observed = 0

    def process_arrival(self):
        self.Na += 1
        self.queue.append(self.current_time)
        if len(self.queue) == 1: # The queue was empty, so set the departure time
            self.next_departure_time = self.current_time + np.random.exponential(1 / self.mu)
        # Otherwise, don't, and set the next arrival time
        self.next_arrival_time = self.current_time + np.random.exponential(1 / self.lambda_)

    def process_departure(self):
        self.Nd += 1
        self.queue.pop(0)
        if self.queue:
            self.next_departure_time = self.current_time + np.random.exponential(1 / self.mu)
        else:
            self.next_departure_time = float('inf')

    def process_observer(self, observer_rate):
        self.No += 1
        self.total_packets_observed += len(self.queue)
        self.next_observer_time = self.current_time + np.random.exponential(1 / observer_rate)

    def simulate(self, observer_rate):
        while self.current_time < self.T:
            if self.next_arrival_time <= self.next_departure_time and self.next_arrival_time <= self.next_observer_time:
                self.current_time = self.next_arrival_time
                self.process_arrival()
            elif self.next_departure_time <= self.next_arrival_time and self.next_departure_time <= self.next_observer_time:
                self.current_time = self.next_departure_time
                self.process_departure()
            else:
                self.current_time = self.next_observer_time
                self.process_observer(observer_rate)

        EN = self.total_packets_observed / self.No
        PIDLE = (self.T - self.Nd / self.mu) / self.T
        return EN, PIDLE

# Parameters
L = 2000  # bits
C = 10**6  # bps
mu = C / L
T = 10000  # Total simulation time
rho_values = np.arange(0.5, 1.6, 0.1)
observer_rate = 5 * mu  # 5 times the service rate

EN_values = []

for rho in rho_values:
    lambda_ = rho * mu
    simulator = MM1QueueSimulator(lambda_, mu, T, observer_rate)
    EN, _ = simulator.simulate(observer_rate)
    
    EN_values.append(EN)

# Plot E[N]
plt.figure()
plt.plot(rho_values, EN_values, '-o', label='M/M/1')
plt.title('E[N] vs ρ for M/M/1 queue with Observers')
plt.xlabel('ρ')
plt.ylabel('E[N]')
plt.grid(True)
plt.legend()
plt.show()
