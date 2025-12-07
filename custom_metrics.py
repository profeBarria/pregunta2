from prometheus_client import CollectorRegistry, Gauge, Counter, push_to_gateway
import random, time

PUSHGATEWAY_URL = "http://localhost:9091"
registry = CollectorRegistry()

# 1. Counter → Visitas acumuladas del día
visits_total = Counter(
    'store_visits_total',
    'Visitas acumuladas durante el día',
    registry=registry
)

# 2. Gauge → Visitas por cada hora (última hora)
visits_per_hour = Gauge(
    'store_visits_last_hour',
    'Visitas registradas en la última hora',
    registry=registry
)

while True:
    # Simulamos la cantidad de visitas de la última hora
    hourly_visits = random.randint(0, 1000)

    # Counter: acumulado total del día
    visits_total.inc(hourly_visits)

    # Gauge: visitas de la última hora
    visits_per_hour.set(hourly_visits)

    # Enviar al Pushgateway
    push_to_gateway(PUSHGATEWAY_URL, job='store_traffic_metrics', registry=registry)
    print(f"Métricas enviadas al Pushgateway — Visitas esta hora: {hourly_visits}")

    time.sleep(15)
