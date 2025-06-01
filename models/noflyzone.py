class NoFlyZone:
    def __init__(self, id, coordinates, active_time):
        self.id = id  # No-fly bölge kimliği
        self.coordinates = coordinates  # Çokgen olarak koordinatlar [(x1, y1), (x2, y2), ...]
        self.active_time = active_time  # Aktif olduğu zaman aralığı (başlangıç, bitiş)
