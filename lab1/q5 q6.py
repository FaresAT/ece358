import numpy as np
import matplotlib.pyplot as plt

class MM1KQueueSimulator:
    def __init__(self, lambda_, mu, T, K, observer_rate):
        self.lambda_ = lambda_
        self.mu = mu
        self.T = T
        self.K = K
        self.queue = []
        self.current_time = 0
        self.next_arrival_time = np.random.exponential(1 / self.lambda_)
        self.next_departure_time = float('inf')
        self.next_observer_time = np.random.exponential(1 / observer_rate)
        self.dropped_packets = 0
        self.Na = 0
        self.Nd = 0
        self.No = 0
        self.total_packets_observed = 0

    def process_arrival(self):
        self.Na += 1
        if len(self.queue) < self.K:
            self.queue.append(self.current_time)
            if len(self.queue) == 1:  # Empty queue, set the departure time normally
                self.next_departure_time = self.current_time + np.random.exponential(1 / self.mu)
        else:
            # Dropped packet case, no more space in buffer
            self.dropped_packets += 1

        self.next_arrival_time = self.current_time + np.random.exponential(1 / self.lambda_)

    def process_departure(self):
        self.Nd += 1
        self.queue.pop(0)  # Remove the packet from the queue
        if self.queue:  # Compute service time for next packet if required
            self.next_departure_time = self.current_time + np.random.exponential(1 / self.mu)
        else:
            self.next_departure_time = float('inf')

    def process_observer(self, observer_rate):
        self.No += 1
        self.total_packets_observed += len(self.queue)
        self.next_observer_time = self.current_time + np.random.exponential(1 / observer_rate)

    def simulate(self, observer_rate):
        while self.current_time < self.T:
            if min(self.next_arrival_time, self.next_departure_time, self.next_observer_time) == self.next_arrival_time:
                self.current_time = self.next_arrival_time
                self.process_arrival()
            elif min(self.next_arrival_time, self.next_departure_time, self.next_observer_time) == self.next_departure_time:
                self.current_time = self.next_departure_time
                self.process_departure()
            else:
                self.current_time = self.next_observer_time
                self.process_observer(observer_rate)

        # Generate performance metrics
        EN = self.total_packets_observed / self.No
        PLOSS = self.dropped_packets / self.Na
        return EN, PLOSS

# Parameters
L = 2000  # bits
C = 10**6  # bps
mu = C / L
T = 10000  # Total simulation time
rho_values = np.arange(0.5, 1.6, 0.1)
observer_rate = 5 * mu  # 5 times the service rate
K_values = [10, 25, 50]

EN_results = {K: [] for K in K_values}
PLOSS_results = {K: [] for K in K_values}

for K in K_values:
    for rho in rho_values:
        lambda_ = rho * mu
        simulator = MM1KQueueSimulator(lambda_, mu, T, K, observer_rate)
        EN, PLOSS = simulator.simulate(observer_rate)
        
        EN_results[K].append(EN)
        PLOSS_results[K].append(PLOSS)

# Plot E[N]
plt.figure()
for K in K_values:
    plt.plot(rho_values, EN_results[K], '-o', label=f"K={K}")
plt.title('E[N] vs ρ for M/M/1/K queue')
plt.xlabel('ρ')
plt.ylabel('E[N]')
plt.grid(True)
plt.legend()
plt.show()

# Plot PLOSS
plt.figure()
for K in K_values:
    plt.plot(rho_values, PLOSS_results[K], '-o', label=f"K={K}")
plt.title('PLOSS vs ρ for M/M/1/K queue')
plt.xlabel('ρ')
plt.ylabel('PLOSS')
plt.grid(True)
plt.legend()
plt.show()
