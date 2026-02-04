def calc_angle_diff(target_ang, current_ang):
    return (target_ang - current_ang + 180) % 360 - 180