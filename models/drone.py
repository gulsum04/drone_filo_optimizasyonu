class Drone:
    def __init__(self, id, max_weight, battery, speed, start_pos):
        self.id = id
        self.max_weight = max_weight
        self.battery = battery
        self.speed = speed
        self.start_pos = start_pos
        self.current_pos = start_pos
        self.available = True
        self.route = []
        self.energy_used = 0
