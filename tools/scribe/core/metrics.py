from prometheus_client import Counter, Gauge, start_http_server
import logging

logger = logging.getLogger(__name__)

events_processed_counter = Counter('scribe_events_processed', 'Total events processed')
events_failed_counter = Counter('scribe_events_failed', 'Total events failed')
queue_size_gauge = Gauge('scribe_queue_size', 'Current event queue size')

def start_metrics_server(port: int = 8000):
    try:
        start_http_server(port)
        logger.info(f"Prometheus metrics server started on port {port}")
    except Exception as e:
        logger.error(f"Failed to start metrics server: {e}") 