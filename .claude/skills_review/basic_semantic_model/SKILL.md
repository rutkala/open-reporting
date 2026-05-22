---
name: basic_semantic_model
description: "Semantic model artifact. Defines what a MetricFlow semantic model YAML is — entities, dimensions, and measures that expose warehouse data through a consistent analytical interface."
user-invocable: false
---

# Semantic Model

A semantic model is a MetricFlow YAML file that exposes warehouse data through
a consistent analytical interface — named measures, typed dimensions, and entities
with defined relationships.

Produced by: `/composite_build` (`data-engineer` agent, guided by `/basic_architecture`)
Consumed by: `/complex_dashboard` (via DuckDB queries through the semantic layer)

---

## Location

`products/warehouse/models/marts/{domain}/semantic_models/{model}.yml`

---

## Structure

Every semantic model YAML must contain:

```yaml
semantic_models:
  - name: {model_name}
    description: "{what this model represents}"
    model: ref('{dbt_model_name}')

    entities:
      - name: {entity_name}
        type: primary
        expr: {id_column}

    dimensions:
      - name: {dim_name}
        type: categorical | time
        expr: {column_or_expr}

    measures:
      - name: {measure_name}
        description: "{Polish label and what it measures}"
        agg: sum | average | count | count_distinct | min | max
        expr: {column_or_expr}
```

---

## Rules

- Measures on fact tables only — never on dimension tables
- Each measure must have a Polish label in its description
- `format_type` and unit declared for every numeric measure
- `agg: sum` for flow measures (revenue, employment change)
- `agg: average` for rate measures (unemployment rate, average wage)
- Time dimensions must use `type: time`

---

## Quality criteria

- [ ] `dbt sl list metrics` runs without errors
- [ ] Every measure has Polish label and unit in description
- [ ] No measures on dimension tables
- [ ] Aggregation type matches measure semantics (stock vs flow)

---

## Standards

- `team/standards/build/measures.md`
- `team/knowledge-base/business-analysis/kpi-indicator-design.md`
- Reviewed by: `measures-reviewer` agent
