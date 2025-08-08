import asyncio
import json
from nats.aio.client import Client as NATS
from tools.scribe.core.logging_config import get_scribe_logger
from tools.scribe.core.boundary_validator import BoundaryValidator, create_boundary_validator, BoundaryType
from tools.scribe.core.telemetry import initialize_telemetry, get_telemetry_manager
from tools.scribe.core.dlq import write_dlq

logger = get_scribe_logger(__name__)

# Initialize sophisticated telemetry system
telemetry_manager = initialize_telemetry("scribe-nats-adapter")
boundary_validator = create_boundary_validator()

async def run_nats(url: str, subject: str):
    nc = NATS()
    await nc.connect(url)

    async def handler(msg):
        try:
            payload = json.loads(msg.data.decode("utf-8"))
        except Exception:
            payload = {"message_id": "", "subject": subject, "payload": {}, "ts": ""}
        # Use sophisticated boundary validation system
        with telemetry_manager.trace_boundary_call("inbound", "nats", subject, "message_received") as span:
            result = boundary_validator.validate_l1_input(payload, "nats")
            span.set_attribute("surface", "nats")
            span.set_attribute("subject", subject)
            span.set_attribute("valid", result.valid)
            span.set_attribute("error_count", len(result.errors))
            
            if not result.valid:
                telemetry_manager.action_failures_counter.add(1, {"surface": "nats", "reason": "validation"})
                write_dlq("nats", payload.get("message_id", ""), result.errors, {"subject": subject})
                logger.error("L1 validation failed; message dropped", 
                           subject=subject, errors=result.errors, component_id=result.component_id)
                return
            
            telemetry_manager.file_events_counter.add(1, {"surface": "nats"})
        # Proceed with normal processing via ports/adapters

    await nc.subscribe(subject, cb=handler)
    logger.info("NATS subscriber started", subject=subject)
    while True:
        await asyncio.sleep(3600)