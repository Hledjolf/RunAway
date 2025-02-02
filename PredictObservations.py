# Predict and calculate observations
while kf.get_state()[2] >= 0:
    kf.predict()
    px, py, pz, vx, vy, vz = kf.get_state()
    ox, oy, oz = observer_position
    
    range_ = np.sqrt((px - ox) ** 2 + (py - oy) ** 2 + (pz - oz) ** 2)
    azimuth = np.arctan2(py - oy, px - ox)
    elevation = np.arcsin((pz - oz) / range_)
    range_rate = np.dot([vx, vy, vz], [(px - ox) / range_, (py - oy) / range_, (pz - oz) / range_])
    
    azimuths.append(azimuth)
    elevations.append(elevation)
    ranges.append(range_)
    range_rates.append(range_rate)
    
    # Update step with the calculated observation
    kf.update([azimuth, elevation, range_, range_rate], observer_position)

# Print predicted observations
for i in range(len(azimuths)):
    print(f"Time step {i * dt:.1f} s - Azimuth: {azimuths[i]:.2f}, Elevation: {elevations[i]:.2f}, Range: {ranges[i]:.2f}, Range Rate: {range_rates[i]:.2f}")