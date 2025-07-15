## Part I: Three-Layer Architecture

### 1.1 Layer 1: Strategic (The "Why")
**Purpose**: Provide situational awareness and identify the critical constraint to address

**Core Components**:
- **Wardley Mapping**: Visualize the value chain and evolutionary state of components
- **Theory of Constraints**: Identify the single bottleneck limiting system performance
- **Strategic Context Analysis**: Assess competitive landscape and strategic options

**Output**: `strategic_context` object defining the imperative and primary constraint (see [PDP Digital Twin](./02-pdp-digital-twin.md#21-semantic-data-model-json-ld))

### 1.2 Layer 2: Orchestration (The "How")
**Purpose**: Transform strategic intent into actionable, decomposed plans

**Core Components**:
- **The [5D Journey](./03-enhanced-5d-journey.md)**: DEFINE → DIAGNOSE → DESIGN → DEVELOP → DELIVER & LEARN
- **Cynefin-based routing**: Complexity-driven methodology selection
- **Recursive decomposition**: Fractal application of the entire framework

**Output**: Fully decomposed WBS tree with formal [BPMN/DMN specifications](./05-implementation-architecture.md#51-three-layer-system-architecture)

### 1.3 Layer 3: Execution (The "What")
**Purpose**: Implement the plan while maintaining antifragile adaptability

**Core Components**:
- **Domain-specific frameworks**: SOP, PRINCE2, Agile, Crisis Management
- **Value stream optimization**: Continuous waste elimination
- **Cybernetic control**: Real-time monitoring and adaptation (see [Implementation Architecture](./05-implementation-architecture.md))

**Output**: Delivered value with continuous telemetry feeding back to the [Digital Twin](./02-pdp-digital-twin.md) 