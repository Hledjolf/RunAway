import numpy as np

class KalmanFilter:
    def __init__(self, dt, process_noise, measurement_noise, initial_state, initial_covariance):
        self.dt = dt
        self.A = np.eye(6) + np.diag([dt] * 3, k=3)
        self.A[2, 5] = -0.5 * 9.8 * dt ** 2
        self.A[5, 5] = 1 - 9.8 * dt
        self.P = initial_covariance
        self.x = initial_state
        self.Q = process_noise
        self.R = measurement_noise

    def predict(self):
        self.x = np.dot(self.A, self.x)
        self.P = np.dot(np.dot(self.A, self.P), self.A.T) + self.Q

    def update(self, z, observer_position):
        # Calculate the observation matrix H based on the current state and observer position
        px, py, pz, vx, vy, vz = self.x
        ox, oy, oz = observer_position
        
        range_ = np.sqrt((px - ox) ** 2 + (py - oy) ** 2 + (pz - oz) ** 2)
        azimuth = np.arctan2(py - oy, px - ox)
        elevation = np.arcsin((pz - oz) / range_)
        
        H = np.zeros((4, 6))
        H[0, 0] = -(py - oy) / ((px - ox) ** 2 + (py - oy) ** 2)
        H[0, 1] = (px - ox) / ((px - ox) ** 2 + (py - oy) ** 2)
        H[1, 0] = -(pz - oz) * (px - ox) / (range_ ** 2 * np.sqrt((px - ox) ** 2 + (py - oy) ** 2))
        H[1, 1] = -(pz - oz) * (py - oy) / (range_ ** 2 * np.sqrt((px - ox) ** 2 + (py - oy) ** 2))
        H[1, 2] = np.sqrt((px - ox) ** 2 + (py - oy) ** 2) / range_ ** 2
        H[2, 0] = (px - ox) / range_
        H[2, 1] = (py - oy) / range_
        H[2, 2] = (pz - oz) / range_
        H[3, 3] = (px - ox) / range_
        H[3, 4] = (py - oy) / range_
        H[3, 5] = (pz - oz) / range_
        
        y = z - np.array([azimuth, elevation, range_, np.dot([vx, vy, vz], [(px - ox) / range_, (py - oy) / range_, (pz - oz) / range_])])
        S = np.dot(H, np.dot(self.P, H.T)) + self.R
        K = np.dot(np.dot(self.P, H.T), np.linalg.inv(S))
        self.x = self.x + np.dot(K, y)
        self.P = self.P - np.dot(K, np.dot(H, self.P))

    def get_state(self):
        return self.x

# Parameters
dt = 0.1  # time step
process_noise = np.diag([1, 1, 1, 1, 1, 1])
measurement_noise = np.diag([1, 1, 1, 1])
initial_state = np.array([0, 0, 0, 50, 50, 0])
initial_covariance = np.eye(6)

# Create Kalman filter instance
kf = KalmanFilter(dt, process_noise, measurement_noise, initial_state, initial_covariance)

# Simulate and update the Kalman Filter
observations = [
    # Add your observations here in the form of [azimuth, elevation, range, range_rate]
]
observer_position = np.array([10, 0, 0])

for z in observations:
    kf.predict()
    kf.update(z, observer_position)
    print("Updated state:", kf.get_state())