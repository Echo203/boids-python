# Boid implementation with Pygame and Python

## Requirements:
- Python 3.13 and up
- Pygame 2.6.1
- VcXsrv (if on WSL)

## Config
In const.py:

### Window size
```python
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
SCREEN_MARGIN = 100
```

### Ammount of boids
```python
AMMOUNT_OF_BOIDS = 50
```

### Algorithm factors
```python
ALIGNMENT_FACTOR = 1.0
COHESION_FACTOR = 0.8
SEPARATION_FACTOR = 1.5
```

### Vision settings
```python
BOID_FOV = 0.2
```
### Range for flock and for avoiding
```python
NEIGHBOUR_RANGE = 50
BOID_SEPARATION_DISTANCE = 20
```

### Turning settings
```python
BOID_ANGULAR_VELOCITY = 0
BOID_ANGULAR_DUMP = 0.8
BOID_STEER_FORCE = 50
```

### Boid properities
```python
BOID_ACC_RATE = 0.05
BOID_SLOW_RATE = 0.05
BOID_MAX_SPEED = 250
BOID_MIN_SPEED = 100
BOID_MAX_TURN_SPEED = 300
BOID_RADIUS = 10
```