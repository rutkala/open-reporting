# Factory Blueprint Schema Specification

This document defines the mandatory structure for all product blueprints in `team/factory/products/*.yaml`. Every blueprint represents a deterministic assembly line for a specific product.

## 1. Global Product Metadata
Every blueprint must begin with the product's identity:
- `product`: (String) The human-readable name of the product.
- `id`: (String) The product ID (e.g., P15).
- `version`: (String) The version of the assembly process.

## 2. The Assembly Line (`assembly_line`)
A list of steps executed in sequential order. Each step represents a transition from one "Part" to the next.

### Step Structure
Each step must contain:
- `step`: (Integer) The sequence number (e.g., 10, 20).
- `workstation`: (String) The competency-based station (e.g., "Requirements", "Architecture").
- `part`: (String) The ID of the deliverable produced at this step (e.g., P14.1).
- `part_name`: (String) Human-readable name of the deliverable.
- `input`: (List) The IDs of the parts required as input for this step (e.g., [P14.1, P00.1]).
- `output`: (String) Clear description of the final artifact produced (e.g., "Python/Dash application code").
- `builder_instruction`: (String) Path to the assembly manual for the builder (e.g., `"team/factory/instructions/dashboard/step_10_builder.md"`).
- `evaluator_instruction`: (String) Path to the inspection protocol for the evaluator (e.g., `"team/factory/instructions/dashboard/step_10_evaluator.md"`).
- `builder`: (String) The specific agent role responsible for creation (e.g., `"biz-strategy-dev"`).
- `evaluator`: (String) The specific agent role responsible for quality control (e.g., `"biz-strategy-test"`).
- `standard`: (String) The path to the build/eval standard file (e.g., `"team/standards/build/requirements.md"`).
- `release_document`: (String) Path to the template checklist that must be completed as evidence of quality (e.g., `"team/factory/templates/dashboard/step_10_checklist.md"`).
- `dor`: (String) **Definition of Ready**. The condition that must be met in the `release_document` for the part to be considered "Ready" for the next workstation.

**Note: All string values in the YAML blueprints must be wrapped in double quotes (`" "`) for parsing consistency.**

## 3. State Tracking
The blueprint is read-only. The current state of the assembly (which parts are `pending` vs `ready`) must be tracked in a separate state file or the project's session memory.

## 4. Validation Rules
- No step can be executed until the `dor` of the preceding step is marked as `ready`.
- A part is marked `ready` only after the `evaluator` has provided a formal sign-off based on the `standard`.
