# S-400 Air Defense Simulation
[THIS IS ONE OF MY FIRST PROJECTS]
A 3D real-time simulation of an S-400 air defense system engaging a randomly selected aircraft. The simulation models radar detection, tracking, missile guidance, countermeasures (jamming, signal loss, evasion), IFF (Identification Friend or Foe), aircraft retaliation, and defensive interception.

Built with Python using Matplotlib for 3D visualization and animation.

## Features

- Randomly selected target aircraft from a list of modern fighter jets (F-15, Su-27, F-18, Su-35, Su-57, F-35, F-22) and one civilian airliner (Boeing 777).
- Realistic (simplified) physics:
  - Aircraft acceleration based on altitude and maneuver type
  - Missile acceleration and fuel consumption
  - Turn rate limits (horizontal and vertical)
  - Waypoint-based flight path with automatic evasion when under attack
- Radar simulation:
  - Noise and accuracy degradation based on distance, time, altitude, and aircraft stealth
  - Electronic jamming effects
  - Intermittent signal loss (simulated ECM bursts)
  - Lock-on mechanics
- IFF system with probabilistic friend/foe identification based on aircraft type and side (Russia vs Ukraine)
- Interactive controls:
  - **FIRE MISSILE** button – launches an S-400 missile (up to 2 total)
  - **SELF DESTRUCT** button – destroys the active missile in flight
- Aircraft retaliation:
  - Military aircraft may launch a standoff missile against the S-400 battery
- S-400 defense:
  - Can launch up to 2 interceptors to shoot down incoming aircraft missiles (within ~200 km range)
- Real-time information panel showing:
  - Radar coordinates and tracking accuracy
  - Target speed estimate
  - IFF result
  - Lock status
  - Missile and interceptor positions, speeds, fuel
  - System status

## Aircraft Characteristics

Each aircraft has unique parameters affecting survivability:

| Aircraft               | Stealth | Jamming | Max Speed | Max Altitude | Maneuverability | ECM Duration |
|------------------------|---------|---------|-----------|--------------|-----------------|--------------|
| F-22                   | High    | Strong  | Very High | High         | High            | Long         |
| F-35                   | Very High| Very Strong | Medium   | Medium       | Good            | Very Long    |
| Su-57                  | High    | Strong  | High      | High         | Excellent       | Long         |
| F-15 / F-18            | Low     | Medium  | Medium-High | Medium     | Good            | Medium       |
| Su-27 / Su-35          | Very Low| Weak    | Medium-High | High       | Excellent       | Short        |
| Boeing 777 (Civilian)  | None    | None    | Low       | Low          | Poor            | None         |

[THE CODEBASE IS POLISHED WITH AI]

## Requirements

- Python 3.6+
- Matplotlib (`pip install matplotlib`)

## How to Run

1. Gather all the files in one project
2. Run 2D/3D Script
