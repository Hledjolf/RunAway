import numpy as np
import csv
import sys

def main():
    # Parameters
    dt = 0.1  # time step
    initial_state = np.array([0, 0, 0, 50, 0, 50])

    # Observer positions
    observer_positions = [
        np.array([0, 250, 0]),
        np.array([250, 250, 0]),
        np.array([250, -250, 0])
    ]

    # Arrays for storing predicted observations for each observer
    all_azimuths = [[] for _ in observer_positions]
    all_elevations = [[] for _ in observer_positions]
    all_ranges = [[] for _ in observer_positions]
    all_range_rates = [[] for _ in observer_positions]

    # Initial state
    px, py, pz, vx, vy, vz = initial_state

    # Predict and calculate observations
    while pz >= 0:
        # Update state
        px += vx * dt
        py += vy * dt
        pz += vz * dt - 0.5 * 9.8 * dt ** 2
        vz -= 9.8 * dt

        for idx, observer_position in enumerate(observer_positions):
            ox, oy, oz = observer_position
            
            range_ = np.sqrt((px - ox) ** 2 + (py - oy) ** 2 + (pz - oz) ** 2)
            azimuth = np.arctan2(py - oy, px - ox)
            elevation = np.arcsin((pz - oz) / range_)
            range_rate = np.dot([vx, vy, vz], [(px - ox) / range_, (py - oy) / range_, (pz - oz) / range_])
            
            all_azimuths[idx].append(azimuth)
            all_elevations[idx].append(elevation)
            all_ranges[idx].append(range_)
            all_range_rates[idx].append(range_rate)

    # Save predicted observations to a CSV file
    with open('predicted_observations.csv', 'w', newline='') as csvfile:
        fieldnames = ['Observer', 'Time step (s)', 'Azimuth', 'Elevation', 'Range', 'Range Rate']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for idx, observer_position in enumerate(observer_positions):
            for i in range(len(all_azimuths[idx])):
                writer.writerow({
                    'Observer': f"Observer at position {observer_position}",
                    'Time step (s)': f"{i * dt:.1f}",
                    'Azimuth': f"{all_azimuths[idx][i]:.2f}",
                    'Elevation': f"{all_elevations[idx][i]:.2f}",
                    'Range': f"{all_ranges[idx][i]:.2f}",
                    'Range Rate': f"{all_range_rates[idx][i]:.2f}"
                })

if __name__ == "__main__":
    main()