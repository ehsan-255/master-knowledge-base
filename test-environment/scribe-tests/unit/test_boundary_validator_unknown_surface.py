import pytest
from tools.scribe.core.boundary_validator import BoundaryValidator, create_boundary_validator

def test_unknown_surface_raises():
    """Test that the sophisticated boundary validator handles unknown surfaces properly"""
    boundary_validator = create_boundary_validator()
    
    # The sophisticated system doesn't raise ValueError, it returns ValidationResult with errors
    result = boundary_validator.validate_l1_input({"test": "data"}, "unknown")
    
    # Should be invalid due to unknown surface/missing schema
    assert not result.valid
    assert len(result.errors) > 0
    assert "No schema found" in result.errors[0]