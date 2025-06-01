class Drone:
    def __init__(self, id, max_weight, battery, speed, start_pos):
        self.id = id  # Drone kimliği
        self.max_weight = max_weight  # Maksimum taşıma kapasitesi (kg)
        self.battery = battery  # Mevcut batarya (mAh)
        self.speed = speed  # Hız (m/s)
        self.start_pos = start_pos  # Başlangıç konumu (x, y)
        self.current_pos = start_pos  # Güncel konum
        self.route = []  # A* veya GA sonucu atanmış rota
        self.available = True  # Uygunluk durumu (şarjda mı?)
        self.energy_used = 0  # Toplam harcanan enerji
        self.available_at = 0  # Dakika bazlı: ne zamana kadar şarjda? (simülasyon zamanı ile karşılaştırılır)

    def reset(self):
        self.battery = 10000
        self.current_pos = self.start_pos
        self.route = []
        self.available_at = 0