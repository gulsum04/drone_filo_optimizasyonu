class Teslimat:
    def __init__(self, id, pos, weight, priority, time_window):
        self.id = id  # Teslimat kimliği
        self.pos = pos  # Hedef konum (x, y)
        self.weight = weight  # Ağırlık (kg)
        self.priority = priority  # Öncelik seviyesi (1–5)
        self.time_window = time_window  # Zaman penceresi (başlangıç, bitiş)
        self.assigned = False  # Bu teslimat bir drone'a atandı mı?

    def __lt__(self, other):
        return self.priority > other.priority
      

