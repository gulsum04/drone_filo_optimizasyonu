import math

def euclidean(p1, p2):
    """
    İki nokta arasındaki düz (öklidyen) mesafeyi hesaplar.
    """
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def distance_cost(p1, p2, weight, priority):
    """
    Maliyet fonksiyonu: distance × weight + (priority × 100 ceza)
    Öncelik: 1 (düşük) → az ceza, 5 (yüksek) → çok ceza
    """
    distance = euclidean(p1, p2)
    penalty = (6 - priority) * 100  # Önceliğe dayalı ters orantılı ceza
    return distance * weight + penalty
