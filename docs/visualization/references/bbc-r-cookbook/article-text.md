# BBC Visual and Data Journalism cookbook for R graphics

BBC Visual and Data Journalism team

---

## Overview

At the BBC data team, we have developed an R package and an R cookbook to make the process of creating publication-ready graphics in our in-house style using R's ggplot2 library a more reproducible process, as well as making it easier for people new to R.

The bbplot package contains two core functions:
- `bbc_style()` — applies the BBC house style theme to any ggplot
- `finalise_plot()` — adds BBC logo, left-aligns title/subtitle, and saves to file

## How does the bbplot package work?

`bbc_style()` has no arguments and is added to the ggplot "chain" after you have created a plot. What it does is generally makes text size, font and colour, axis lines, axis text, margins and many other standard chart components into BBC style, which has been formulated based on recommendations and feedback from the design team.

Note that colours for lines in the case of a line chart or bars for a bar chart, do not come out of the box from the `bbc_style()` function, but need to be explicitly set in your other standard ggplot chart functions.

Important: if you want to make any additional theme changes of your own, you must call them after calling `bbc_style()`. Otherwise `bbc_style()` will override it.

## Colour conventions

Consistent colour usage throughout examples:
- Primary blue: `#1380A1`
- Gold/highlight: `#FAAB18`
- Dark grey text: `#333333`, `#555555`
- Light grey gridlines: `#cbcbcb`, `#dddddd`

## Baseline rule

A horizontal baseline at zero is applied to nearly every chart:

```r
geom_hline(yintercept = 0, size = 1, colour = "#333333")
```

This provides a visual anchor and clearly distinguishes positive from negative values.

## Typography

- Font family: Helvetica
- Left-alignment standard: `finalise_plot()` left-aligns the title and subtitle as is standard for BBC graphics
- Text alignment control via `hjust` and `vjust` arguments

## Axis and gridline guidance

Default theme: gridlines only on the y axis (no x gridlines by default).

To add x gridlines:
```r
panel.grid.major.x = element_line(...)
```

To remove y gridlines:
```r
panel.grid.major.y = element_blank()
```

## Chart types covered

The cookbook covers the following chart types with full R code:

- Line chart (single and multiple lines)
- Bar chart (single, stacked, grouped)
- Dumbbell chart
- Histogram
- Small multiples (facets)

## Key chart-specific rules

**All charts:** Apply `bbc_style()` last in the ggplot chain. Add a zero baseline with `geom_hline`.

**Line charts:** Set line colours explicitly using `scale_colour_manual()`. Minimise legend clutter by labelling lines directly when possible.

**Bar charts:** Left-align labels for horizontal bars. Sort by value where ranking is the story. Use `coord_flip()` for long category names.

**Small multiples:** Always use the same y-axis scale across panels to avoid misleading comparisons. Use `facet_wrap()` with `scales = "fixed"`.

**Stacked bars:** Provide total labels; individual segment labels are difficult to read.

## Save out your finished chart

The `finalise_plot()` function:
- Saves to a specified path
- Left-aligns title and subtitle (BBC standard)
- Adds BBC logo (or placeholder)
- Width/height specified in pixels

Axis text margin specifications by output height:
- 550px: top=5, bottom=10
- 650px: top=7, bottom=10
- 750px: top=10, bottom=10
- 850px: top=14, bottom=10

## Design philosophy

Not stated explicitly, but demonstrated through examples: high information density combined with clean, minimal styling. Colour is used sparingly — typically one or two accent colours per chart, the rest in grey. Annotations are used to tell the story directly on the chart rather than relying on the reader to interpret raw data.
