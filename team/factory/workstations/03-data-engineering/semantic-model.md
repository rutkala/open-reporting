# Semantic Model Component

## Produces
- Semantic Model (measures, dimensions, data model)

## Internal DAG
See `dag/semantic-model.yaml`

## Step Instructions

### Step 1: Raw Layer
Implement raw data layer.

**Actions:**
- Create raw tables
- Define fetched_at timestamps
- Verify data lands correctly

**Output:** Raw Tables

---

### Step 2: Silver Layer
Implement silver (cleaned/curated) layer.

**Actions:**
- Clean and deduplicate data
- Conform to schema
- Handle NULLs and duplicates

**Output:** Silver Tables

---

### Step 3: Gold Layer
Implement gold (aggregated/mart) layer.

**Actions:**
- Aggregate to required levels
- Calculate metrics
- Create materialized views

**Output:** Gold Tables

---

### Step 4: Semantic Layer
Implement semantic layer with measures and dimensions.

**Actions:**
- Define measures with format_type
- Define dimensions
- Link to KPIs from Requirements
- Apply Polish labels

**Output:** Semantic Model

---

### Step 5: Test
Test the semantic model.

**Actions:**
- Run test queries
- Verify totals match expectations
- Check aggregation correctness

**Output:** Test Results

---

### Step 6: Finalize
Finalize the semantic model.

**Actions:**
- Fix any issues
- Document model
- Mark as ready

**Output:** Final Semantic Model

---

## Input Requirements
- Architecture Design

## Output
- Semantic Model