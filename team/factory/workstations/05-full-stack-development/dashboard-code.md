# Dashboard Code Component

## Produces
- Dashboard Code (assembled dashboard application)

## Internal DAG
See `dag/dashboard-code.yaml`

## Step Instructions

### Step 1: Environment Setup
Set up the dashboard environment.

**Actions:**
- Copy template folder
- Configure environment
- Set up dependencies

**Output:** Environment

---

### Step 2: Data Layer
Implement data layer to call warehouse.

**Actions:**
- Update data.py with warehouse queries
- Connect to semantic model
- Define data fetching functions

**Output:** Data Layer

---

### Step 3: Measure Integration
Integrate measures from semantic model.

**Actions:**
- Update measures.py
- Apply format_type from measures.md
- Apply Polish labels

**Output:** Measures

---

### Step 4: Layout Implementation
Implement the layout from UX/UI design.

**Actions:**
- Update app.py with layout
- Header, filters, topic groups, footer
- Apply Nordic theme

**Output:** Layout

---

### Step 5: Component Wiring
Wire up visual components.

**Actions:**
- Call chart functions from library
- Pass data and measures
- Connect filters to charts

**Output:** Wired Components

---

### Step 6: Local Verification
Verify the dashboard works.

**Actions:**
- Run the app
- Verify charts render
- Test filter interactions

**Output:** Verification Results

---

### Step 7: Finalize
Finalize the dashboard code.

**Actions:**
- Fix any issues
- Clean up code
- Mark as ready

**Output:** Final Dashboard Code

---

## Input Requirements
- UX/UI Design
- Semantic Model

## Output
- Dashboard Code