from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from tools.scribe.core.boundary_validator import BoundaryValidator, create_boundary_validator, BoundaryType
from tools.scribe.core.logging_config import get_scribe_logger
from tools.scribe.core.telemetry import initialize_telemetry, get_telemetry_manager

logger = get_scribe_logger(__name__)

# Initialize sophisticated telemetry system
telemetry_manager = initialize_telemetry("scribe-http-adapter")
boundary_validator = create_boundary_validator()

class L1ValidationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            body = await request.json()
        except Exception:
            body = {}
        # Use sophisticated boundary validation system
        with telemetry_manager.trace_boundary_call("inbound", "http", request.url.path, "request_received") as span:
            payload = {
                "request_id": request.headers.get("x-request-id", ""),
                "route": request.url.path,
                "body": body,
                "ts": request.headers.get("x-request-ts", "")
            }
            
            result = boundary_validator.validate_l1_input(payload, "http")
            span.set_attribute("surface", "http")
            span.set_attribute("route", request.url.path)
            span.set_attribute("valid", result.valid)
            span.set_attribute("error_count", len(result.errors))
            
            if not result.valid:
                telemetry_manager.action_failures_counter.add(1, {"surface": "http", "reason": "validation"})
                logger.error("L1 validation failed; request rejected", 
                           route=request.url.path, errors=result.errors, component_id=result.component_id)
                return Response(status_code=400, content=b'{"error":"invalid"}', media_type="application/json")
            
            telemetry_manager.file_events_counter.add(1, {"surface": "http"})
        return await call_next(request)