- Clean code
- collect all inputs, then update movement
- we can use ratios if we separate it

TODO:
- fix speed:
    - either target to current
    - or current in q to be updated

The key idea: rotation has momentum

Instead of:
```python
self.rotation = desired_angle
```

you do:
```
self.angular_velocity += steering_force
self.rotation += self.angular_velocity * dt
```

This is the missing layer.

Minimal natural steering model (recommended)

Add one new variable to your boid:
```
self.angular_velocity = 0.0  # degrees per second
```

Quick tuning tips

- If boids “snap” → lower STEER_STRENGTH

- If boids “wobble” → increase ANGULAR_DAMPING

- If boids feel sluggish → raise STEER_STRENGTH

- If they spin → clamp angular velocity

```
   # math.atan2 returns radians, convert to degrees
        target_angle = degrees(atan2(avg_dy, avg_dx))

        # 2. Calculate the shortest turn (-180 to 180)
        diff = calc_angle_diff(target_angle, self.rotation)

def steer_away(self, list_of_boids, dt):
        avg_dx = 0
        avg_dy = 0
        for boid in list_of_boids:
            avg_dx = boid.position[0] - self.position[0]
            avg_dy = boid.position[1] - self.position[1]
```