from pathlib import Path
from naming_enforcer import IncludeManager

# Test the include manager directly
im = IncludeManager()
im.add_include_directory('../../../active-project')

print("Include patterns:", im.include_patterns)
print("Include directories:", im.include_directories)

# Test paths
test_paths = [
    Path('../../../active-project'),
    Path('../../../active-project/current-state.Md'),
    Path('../../../active-project/-active-project-organization-initiative-active'),
    Path('../../../active-project/-active-project-organization-initiative-active/README.md')
]

for path in test_paths:
    if path.exists():
        resolved = path.resolve()
        print(f'{path} -> {resolved}: {im.is_included(path)}')
    else:
        print(f'{path}: NOT FOUND') 