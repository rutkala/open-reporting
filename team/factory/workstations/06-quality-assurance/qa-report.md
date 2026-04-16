# QA Report Component

## Produces
- QA Report (test results and evaluation)

## Internal DAG
See `dag/qa-report.yaml`

## Step Instructions

### Step 1: Test Case Generation
Generate test cases for the dashboard.

**Actions:**
- Create golden queries
- Define test scenarios
- Document expected results

**Output:** Test Cases

---

### Step 2: Data Verification
Verify data matches expectations.

**Actions:**
- Run queries against warehouse
- Compare to dashboard values
- Document discrepancies

**Output:** Data Verification

---

### Step 3: Edge Case Testing
Test edge cases and filter combinations.

**Actions:**
- Test extreme values
- Test filter combinations
- Test error handling

**Output:** Edge Case Results

---

### Step 4: Structural Break Check
Check for Polish structural breaks.

**Actions:**
- Verify 2004 EU accession handled
- Verify 2020 COVID period handled
- Verify other breaks documented

**Output:** Structural Break Analysis

---

### Step 5: Documentation
Document all test results.

**Actions:**
- Compile test report
- Document issues found
- Suggest fixes

**Output:** Draft QA Report

---

### Step 6: Finalize
Finalize the QA report.

**Actions:**
- Incorporate feedback
- Finalize report

**Output:** Final QA Report

---

## Input Requirements
- Dashboard Code

## Output
- QA Report