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