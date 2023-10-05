import numpy as np
import matplotlib.pyplot as plt

class MM1QueueSimulator:
    def __init__(self, lambda_, mu, T):
        # Required parameters
        self.lambda_ = lambda_
        self.mu = mu
        self.T = T
        
        # Counters
        self.Na = 0
        self.Nd = 0
        self.No = 0
        self.cumulative_packets = 0
        self.total_idle_time = 0
        
        # Initial event generation
        self.current_time = 0
        self.next_arrival_time = np.random.exponential(1 / self.lambda_)
        self.next_departure_time = float('inf')  # No departures initially
        self.next_observer_time = np.random.exponential(1 / (5 * self.lambda_))
        
        # The FIFO queue
        self.queue = []
        
    def process_arrival(self):
        self.Na += 1
        
        # If server is idle, compute departure time
        if not self.queue:
            self.next_departure_time = self.current_time + np.random.exponential(1 / self.mu)
            
        self.queue.append(self.current_time)
        
        # Schedule next arrival
        self.next_arrival_time = self.current_time + np.random.exponential(1 / self.lambda_)
        
    def process_departure(self):
        self.Nd += 1
        
        # Remove the packet from the queue and compute service time for next packet
        self.queue.pop(0)
        if self.queue:
            self.next_departure_time = self.current_time + np.random.exponential(1 / self.mu)
        else:
            self.next_departure_time = float('inf')
            
    def process_observer(self):
        self.No += 1
        self.cumulative_packets += len(self.queue)
        
        # Calculate idle time
        if not self.queue:
            self.total_idle_time += np.random.exponential(1 / (5 * self.lambda_))
            
        # Schedule next observer
        self.next_observer_time = self.current_time + np.random.exponential(1 / (5 * self.lambda_))
        
    def simulate(self):
        while self.current_time < self.T:
            if self.next_arrival_time < min(self.next_departure_time, self.next_observer_time):
                self.current_time = self.next_arrival_time
                self.process_arrival()
                
            elif self.next_departure_time < self.next_observer_time:
                self.current_time = self.next_departure_time
                self.process_departure()
                
            else:
                self.current_time = self.next_observer_time
                self.process_observer()
                
        # Compute performance metrics after simulation
        EN = self.cumulative_packets / self.No
        PIDLE = self.total_idle_time / self.T
        
        return EN, PIDLE

# Test the simulator
L = 2000  # bits
C = 10**6  # bps
mu = C / L
T = 10000  # Total simulation time

rho_values = np.arange(0.25, 0.95, 0.1)
EN_values = []
PIDLE_values = []

for rho in rho_values:
    lambda_ = rho * mu
    simulator = MM1QueueSimulator(lambda_, mu, T)
    EN, PIDLE = simulator.simulate()
    
    EN_values.append(EN)
    PIDLE_values.append(PIDLE)

# Plot E[N]
plt.figure()
plt.plot(rho_values, EN_values, '-o')
plt.title('E[N] vs ρ')
plt.xlabel('ρ')
plt.ylabel('E[N]')
plt.grid(True)
plt.show()

# Plot PIDLE
plt.figure()
plt.plot(rho_values, PIDLE_values, '-o')
plt.title('PIDLE vs ρ')
plt.xlabel('ρ')
plt.ylabel('PIDLE')
plt.grid(True)
plt.show()
