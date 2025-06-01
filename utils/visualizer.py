import matplotlib.pyplot as plt
from shapely.geometry import LineString, Polygon

def plot_routes(drones, deliveries, nfzs, show=False):
    """
    Drone rotalarını, teslimat noktalarını ve no-fly zone'ları matplotlib ile çizer.
    'show=True' verilirse plt.show() çağrılır.
    """
    fig, ax = plt.subplots()

    # Drone'ların başlangıç noktaları ve rotaları
    for drone in drones:
        x, y = drone.start_pos
        ax.scatter(x, y, color='blue', label=f"Drone {drone.id}" if drone.id == drones[0].id else "")
        if hasattr(drone, "route") and drone.route:
            rx = [p[0] for p in drone.route]
            ry = [p[1] for p in drone.route]
            ax.plot(rx, ry, linestyle='--', label=f"Rota {drone.id}")

    # Teslimat noktaları
    for d in deliveries:
        ax.scatter(d.pos[0], d.pos[1], color='green', marker='x')

    # No-fly zone çizimleri (poligon)
    for nfz in nfzs:
        polygon = nfz.coordinates + [nfz.coordinates[0]]
        px = [p[0] for p in polygon]
        py = [p[1] for p in polygon]
        ax.plot(px, py, color='red', linestyle='--', label=f"No-Fly Zone {nfz.id}" if nfz.id == 0 else "")

    ax.legend()
    plt.title("Drone Rotaları ve No-Fly Zone")
    plt.grid(True)

    if show:
        plt.show()


def plot_routes_debug(drones, deliveries, nfzs, show=False):
    """
    Drone → Teslimat arası tüm rotaları çizer.
    Kesişen rotalar kırmızı, geçerli rotalar gri renkte gösterilir.
    'show=True' verilirse plt.show() çağrılır.
    """
    fig, ax = plt.subplots()

    # No-fly zone'lar
    for nfz in nfzs:
        coords = nfz.coordinates + [nfz.coordinates[0]]
        px, py = zip(*coords)
        ax.fill(px, py, color='red', alpha=0.3)
        ax.plot(px, py, color='red', linestyle='--', label=f"No-Fly Zone {nfz.id}")

    # Drone'lar
    for drone in drones:
        x, y = drone.start_pos
        ax.scatter(x, y, color='blue', label=f"Drone {drone.id}" if drone.id == 0 else "")

    # Teslimat noktaları
    for delivery in deliveries:
        dx, dy = delivery.pos
        ax.scatter(dx, dy, color='green', marker='x')

    # Drone-teslimat rotaları
    for drone in drones:
        for delivery in deliveries:
            line = LineString([drone.start_pos, delivery.pos])
            kesiyor_mu = any(Polygon(nfz.coordinates).intersects(line) for nfz in nfzs)

            x, y = zip(drone.start_pos, delivery.pos)
            if kesiyor_mu:
                ax.plot(x, y, color='red', linestyle=':', linewidth=1.5, alpha=0.7)
            else:
                ax.plot(x, y, color='gray', linestyle='--', alpha=0.3)

    ax.set_title("🚧 Drone-Teslimat Rota Analizi (No-Fly Zone Çakışması)")
    ax.set_xlabel("X Koordinat")
    ax.set_ylabel("Y Koordinat")
    ax.grid(True)
    ax.legend()

    if show:
        plt.show()  