# Architecture Design Component

## Produces
- Architecture Design (data flow, schema, system design)

## Internal DAG
See `dag/architecture-design.yaml`

## Step Instructions

### Step 1: Analyze Requirements
Analyze the Requirements Document to understand what's needed.

**Actions:**
- Read Requirements Document
- Identify data requirements
- Identify functional requirements

**Output:** Requirements Analysis

---

### Step 2: Design Data Flow
Design the data flow from source to final product.

**Actions:**
- Map Raw → Curated → Gold flow
- Define data transformation steps
- Document data pipeline

**Output:** Data Flow Diagram

---

### Step 3: Define Schema
Define the database schema.

**Actions:**
- Define source tables
- Define curated tables
- Define gold mart tables
- Define primary keys and joins

**Output:** Schema Definition

---

### Step 4: Dependency Mapping
Map all dependencies between components.

**Actions:**
- List upstream dependencies
- List downstream dependencies
- Define integration points

**Output:** Dependency Map

---

### Step 5: Review
Review the architecture for completeness.

**Actions:**
- Verify data flow is complete
- Verify schema supports KPIs
- Check for circular dependencies

**Output:** Review Comments

---

### Step 6: Finalize
Finalize the architecture design.

**Actions:**
- Incorporate review feedback
- Finalize documentation

**Output:** Final Architecture Design

---

## Input Requirements
- Requirements Document

## Output
- Architecture Design