import matplotlib.pyplot as plt

def plot_routes(drones, deliveries, nfzs):
    """
    Drone rotalarını, teslimat noktalarını ve no-fly zone'ları matplotlib ile çizer.
    """
    fig, ax = plt.subplots()

    # Dronelar ve rotaları
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

    # No-fly zone'lar
    for nfz in nfzs:
        polygon = nfz.coordinates + [nfz.coordinates[0]]  # İlk noktaya dön
        px = [p[0] for p in polygon]
        py = [p[1] for p in polygon]
        ax.plot(px, py, color='red')

    ax.legend()
    plt.title("Drone Rotaları ve No-Fly Zone")
    plt.grid(True)
    plt.show()
