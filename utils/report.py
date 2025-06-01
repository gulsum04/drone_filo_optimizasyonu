import csv

def save_delivery_report(assignments, drones, deliveries, filename='rapor.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Drone ID', 'Teslimat ID', 'Başlangıç',
            'Teslimat Noktası', 'Paket Ağırlığı', 'Öncelik', 'Zaman Aralığı'
        ])

        for drone_id, delivery_id in assignments:
            drone = next((d for d in drones if d.id == drone_id), None)
            delivery = next((d for d in deliveries if d.id == delivery_id), None)

            if drone and delivery:
                writer.writerow([
                    drone.id,
                    delivery.id,
                    drone.start_pos,
                    delivery.pos,
                    delivery.weight,
                    delivery.priority,
                    f"{delivery.time_window[0]} - {delivery.time_window[1]}" if delivery.time_window else "-"
                ])
