from shapely.geometry import LineString, Polygon
from models.noflyzone import NoFlyZone

def time_to_minutes(t: str) -> int:
    h, m = map(int, t.split(":"))
    return h * 60 + m

def is_delivery_time_valid(current_time: int, delivery) -> bool:
    start = time_to_minutes(delivery.time_window[0]) if isinstance(delivery.time_window[0], str) else delivery.time_window[0]
    end = time_to_minutes(delivery.time_window[1]) if isinstance(delivery.time_window[1], str) else delivery.time_window[1]
    return start <= current_time <= end

def intersects_noflyzone(start, end, nfz: NoFlyZone, current_time: int) -> bool:
    aktif_basla = time_to_minutes(nfz.active_time[0]) if isinstance(nfz.active_time[0], str) else nfz.active_time[0]
    aktif_bitis = time_to_minutes(nfz.active_time[1]) if isinstance(nfz.active_time[1], str) else nfz.active_time[1]

    if not (aktif_basla <= current_time <= aktif_bitis):
        return False

    path = LineString([start, end])
    polygon = Polygon(nfz.coordinates)
    return path.intersects(polygon)

def csp_assignments_multi(drones, deliveries, no_fly_zones, current_time="10:00"):
    """
    CSP mantığında, her teslimat için en uygun drone'u seçerek
    çoklu teslimat destekli basit ve verimli çözüm oluşturur.
    """
    print("📦 [CSP-MULTI] Çoklu teslimat eşlemesi başlatılıyor...")
    current_time = time_to_minutes(current_time) if isinstance(current_time, str) else current_time

    solution = {}
    drone_loads = {d.id: 0 for d in drones}  # iş yükü dengeleme

    for delivery in deliveries:
        if not is_delivery_time_valid(current_time, delivery):
            continue  # zaman aralığı dışında

        uygun_dronelar = []
        for drone in drones:
            if delivery.weight > drone.max_weight:
                continue
            yasak_var_mi = any(
                intersects_noflyzone(drone.start_pos, delivery.pos, nfz, current_time)
                for nfz in no_fly_zones
            )
            if yasak_var_mi:
                continue
            uygun_dronelar.append((drone.id, drone_loads[drone.id]))

        if not uygun_dronelar:
            print(f"⚠️ Teslimat {delivery.id} için uygun drone bulunamadı.")
            continue

        # En az yükteki drone'a ata
        uygun_dronelar.sort(key=lambda x: x[1])
        secilen_drone = uygun_dronelar[0][0]
        solution[delivery.id] = secilen_drone
        drone_loads[secilen_drone] += 1
      

    print(f"✅ Toplam eşleşen teslimat sayısı: {len(solution)} / {len(deliveries)}")
    return [solution]
