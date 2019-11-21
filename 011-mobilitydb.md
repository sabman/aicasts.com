
# Introduction

Why GeoTemporal matters
* https://www.youtube.com/watch?v=_t7jlFbpty4

# Concepts

## Data Types
- `timestamptz` (native to postgresql)
- `timestampset`
- `period`
- `periodset`

## Interesting Operators

```sql
-- Do the operands ever intersect?
SELECT tintersects(tgeompointseq '[Point(0 1),@2001-01-01, Point(3 1)@2001-01-04)', 
  geometry 'Polygon((1 0,1 2,2 2,2 0,1 0))')) &= true;
  
-- Does the operands always intersect?
SELECT tintersects(tgeompointseq '[Point(0 1)@2001-01-01, Point(3 1)@2001-01-04)',
  geometry 'Polygon((0 0,0 2,4 2,4 0,0 0))') @= true;
-- true
```

# Installation

# Testing

# Real World Application
