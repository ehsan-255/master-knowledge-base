from pathlib import Path
from naming_enforcer import NamingEnforcerV2

# Test the enforcer directly
enforcer = NamingEnforcerV2()

# Scan active-project
scan_path = Path('../../../active-project')
print(f"Scanning: {scan_path.resolve()}")

violations = enforcer.scan_directory(scan_path)
print(f"Found {len(violations)} violations:")

for i, violation in enumerate(violations):
    print(f"{i+1}. {violation.path}")
    print(f"   Current: {violation.current_name}")
    print(f"   Suggested: {violation.suggested_name}")
    print(f"   Type: {violation.violation_type}")
    print(f"   Reason: {violation.reason}")
    print()

# Test building rename operations
print("Building rename operations...")
enforcer.build_rename_operations()
print(f"Built {len(enforcer.rename_operations)} rename operations:")

for i, op in enumerate(enforcer.rename_operations):
    print(f"{i+1}. {op.old_path} -> {op.new_path}")
    print(f"   Type: {op.violation_type}")
    print(f"   Content updates: {len(op.content_updates)}")
    print() 