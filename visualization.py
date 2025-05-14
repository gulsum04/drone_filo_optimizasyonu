import matplotlib.pyplot as plt

def draw_combined_routes(drone, deliveries, astar_route, ga_route, zones,
                         astar_info="", ga_info=""):
    fig, axs = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle("Drone Rotaları Karşılaştırması", fontsize=14)

    routes = [
        ("📍 A* Rotası", astar_route, astar_info, axs[0]),
        ("📍 Genetik Algoritma Rotası", ga_route, ga_info, axs[1])
    ]

    for title, route, info, ax in routes:
        ax.set_title(title)
        # 🚫 No-fly zone çizimi
        for zone in zones:
            x = [p[0] for p in zone.coordinates] + [zone.coordinates[0][0]]
            y = [p[1] for p in zone.coordinates] + [zone.coordinates[0][1]]
            ax.fill(x, y, 'red', alpha=0.3)
            ax.plot(x, y, 'r--')

        # 🔵 Rota çizimi
        x_path = [drone.start_pos[0]]
        y_path = [drone.start_pos[1]]
        delivery_map = {d.id: d for d in deliveries}

        for i, did in enumerate(route):
            d = delivery_map[did]
            x_path.append(d.pos[0])
            y_path.append(d.pos[1])
            ax.plot(d.pos[0], d.pos[1], 'bo')
            ax.text(d.pos[0], d.pos[1], str(i + 1), fontsize=9)

        ax.plot(x_path, y_path, 'k-o')
        ax.plot(drone.start_pos[0], drone.start_pos[1], 'go', label="Başlangıç")
        ax.grid(True)
        ax.axis("equal")
        ax.legend()
        # ℹ️ Alt bilgi kutusu
        ax.text(0.5, -0.15, info, transform=ax.transAxes,
                fontsize=10, ha='center',
                bbox={"facecolor": "lightgray", "alpha": 0.5, "pad": 6})

    plt.tight_layout()
    plt.show()
