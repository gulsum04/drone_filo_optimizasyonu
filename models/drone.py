class Drone:
    def __init__(self, id, max_weight, battery, speed, start_pos):
        self.id = id  # Drone kimliği
        self.max_weight = max_weight  # Maksimum taşıma kapasitesi (kg)
        self.battery = battery  # Batarya kapasitesi (mAh)
        self.speed = speed  # Hız (m/s)
        self.start_pos = start_pos  # Başlangıç konumu (x, y)
        self.current_pos = start_pos  # Şu anki konumu
        self.route = []  # A* veya GA sonucu atanmış rota
        self.available = True  # Uygunluk durumu (CSP için)
        self.energy_used = 0  # Harcanan enerji (opsiyonel)
