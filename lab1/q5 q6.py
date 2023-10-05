# import numpy as np
# import matplotlib.pyplot as plt

# class MM1KQueueSimulator:
#     def __init__(self, lambda_, mu, T, K):
#         self.lambda_ = lambda_
#         self.mu = mu
#         self.T = T
#         self.K = K
        
#         self.Na = 0
#         self.Nd = 0
#         self.No = 0
#         self.cumulative_packets = 0
#         self.total_idle_time = 0
#         self.dropped_packets = 0
        
#         self.current_time = 0
#         self.next_arrival_time = np.random.exponential(1 / self.lambda_)
#         self.next_departure_time = float('inf')
#         self.next_observer_time = np.random.exponential(1 / (5 * self.lambda_))
        
#         self.queue = []

#     def process_arrival(self):
#         self.Na += 1
#         if len(self.queue) < self.K:
#             if not self.queue:
#                 self.next_departure_time = self.current_time + np.random.exponential(1 / self.mu)
#             self.queue.append(self.current_time)
#         else:
#             self.dropped_packets += 1
#         self.next_arrival_time = self.current_time + np.random.exponential(1 / self.lambda_)

#     def process_departure(self):
#         self.Nd += 1
#         self.queue.pop(0)
#         if self.queue:
#             self.next_departure_time = self.current_time + np.random.exponential(1 / self.mu)
#         else:
#             self.next_departure_time = float('inf')

#     def process_observer(self):
#         self.No += 1
#         self.cumulative_packets += len(self.queue)
#         if not self.queue:
#             self.total_idle_time += np.random.exponential(1 / (5 * self.lambda_))
#         self.next_observer_time = self.current_time + np.random.exponential(1 / (5 * self.lambda_))

#     def simulate(self):
#         while self.current_time < self.T:
#             if self.next_arrival_time < min(self.next_departure_time, self.next_observer_time):
#                 self.current_time = self.next_arrival_time
#                 self.process_arrival()
#             elif self.next_departure_time < self.next_observer_time:
#                 self.current_time = self.next_departure_time
#                 self.process_departure()
#             else:
#                 self.current_time = self.next_observer_time
#                 self.process_observer()
        
#         EN = self.cumulative_packets / self.No
#         PIDLE = self.total_idle_time / self.T
        
#         return EN, PIDLE

# # L = 2000  # bits
# # C = 10**6  # bps
# # K = 10  # Buffer size
# # mu = C / L

# L = 2000  # bits
# C = 10**6  # bps
# mu = C / L

# rho_values = np.arange(0.5, 1.5, 0.1)
# K_values = [10, 25, 50]
# EN_results = {K: [] for K in K_values}
# PLOSS_results = {K: [] for K in K_values}

# for K in K_values:
#     for rho in rho_values:
#         lambda_ = rho * mu
#         simulator = MM1KQueueSimulator(lambda_, mu, 10000, K)
#         EN, _, PLOSS = simulator.simulate()
        
#         EN_results[K].append(EN)
#         PLOSS_results[K].append(PLOSS)

# # Plot E[N]
# plt.figure()
# for K in K_values:
#     plt.plot(rho_values, EN_results[K], '-o', label=f'K={K}')
# plt.title('E[N] vs ρ for M/M/1/K queue')
# plt.xlabel('ρ')
# plt.ylabel('E[N]')
# plt.legend()
# plt.grid(True)
# plt.show()

# rho_values = np.arange(0.25, 0.95, 0.1)
# EN_values = []
# PIDLE_values = []
# PLOSS_values = []

# for rho in rho_values:
#     lambda_ = rho * mu
#     simulator = MM1KQueueSimulator(lambda_, mu, 10000, K)
#     EN, PIDLE = simulator.simulate()
    
#     EN_values.append(EN)
#     PIDLE_values.append(PIDLE)
#     PLOSS_values.append(simulator.dropped_packets / simulator.Na)

import numpy as np
import matplotlib.pyplot as plt

class MM1KQueueSimulator:
    def __init__(self, lambda_, mu, T, K):
        self.lambda_ = lambda_
        self.mu = mu
        self.T = T
        self.K = K
        self.queue = []
        self.current_time = 0
        self.next_arrival_time = np.random.exponential(1 / self.lambda_)
        self.next_departure_time = float('inf')
        self.dropped_packets = 0
        self.Na = 0
        self.Nd = 0

    def process_arrival(self):
        self.Na += 1
        if len(self.queue) < self.K:
            self.queue.append(self.current_time)
            if len(self.queue) == 1:  # The queue was empty, so set the departure time
                self.next_departure_time = self.current_time + np.random.exponential(1 / self.mu)
        else:
            self.dropped_packets += 1

        self.next_arrival_time = self.current_time + np.random.exponential(1 / self.lambda_)

    def process_departure(self):
        self.Nd += 1
        self.queue.pop(0)  # Remove the packet from the queue
        if self.queue:  # Case where packets in the queue
            self.next_departure_time = self.current_time + np.random.exponential(1 / self.mu)
        else:
            self.next_departure_time = float('inf')

    def simulate(self):
        while self.current_time < self.T:
            if self.next_arrival_time <= self.next_departure_time:
                self.current_time = self.next_arrival_time
                self.process_arrival()
            else:
                self.current_time = self.next_departure_time
                self.process_departure()

        EN = len(self.queue)
        PIDLE = (self.T - self.Nd / self.mu) / self.T
        PLOSS = self.dropped_packets / self.Na
        return EN, PIDLE, PLOSS

# Parameters
L = 2000  # bits
C = 10**6  # bps
mu = C / L
T = 10000  # Total simulation time
rho_values = np.arange(0.5, 1.6, 0.1)  # 0.5 < rho < 1.5
K_values = [10, 25, 50]

EN_results = {K: [] for K in K_values}
PLOSS_results = {K: [] for K in K_values}

for K in K_values:
    for rho in rho_values:
        lambda_ = rho * mu
        simulator = MM1KQueueSimulator(lambda_, mu, T, K)
        EN, _, PLOSS = simulator.simulate()
        
        EN_results[K].append(EN)
        PLOSS_results[K].append(PLOSS)

# Plot E[N]
plt.figure()
for K in K_values:
    plt.plot(rho_values, EN_results[K], '-o', label=f"K={K}")
plt.title('E[N] vs ρ for M/M/1/K queue')
plt.xlabel('ρ')
plt.ylabel('E[N]')
plt.legend()
plt.grid(True)
plt.show()

# Plot PLOSS
plt.figure()
for K in K_values:
    plt.plot(rho_values, PLOSS_results[K], '-o', label=f"K={K}")
plt.title('PLOSS vs ρ for M/M/1/K queue')
plt.xlabel('ρ')
plt.ylabel('PLOSS')
plt.legend()
plt.grid(True)
plt.show()
