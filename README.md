# ELK-setup

| Field              | Mapping   | Typical query         | What you use it for                 |
| ------------------ | --------- | --------------------- | ----------------------------------- |
| `message`          | `text`    | `match`               | Search words                        |
| `message`          | `text`    | `match_phrase`        | Search an exact phrase/order        |
| `message`          | `text`    | `multi_match`         | Search multiple text fields         |
| `message`          | `text`    | `match_bool_prefix`   | Prefix-style text searching         |
| `airline`          | `text`    | `match`               | Search airline text                 |
| `airline`          | `text`    | `match_phrase`        | Search airline phrase               |
| `airline.keyword`  | `keyword` | `term`                | Exact airline                       |
| `airline.keyword`  | `keyword` | `terms`               | Match multiple airlines             |
| `airline.keyword`  | `keyword` | `prefix`              | Values starting with something      |
| `airline.keyword`  | `keyword` | `wildcard`            | Pattern matching                    |
| `airline.keyword`  | `keyword` | `regexp`              | Regular-expression matching         |
| `status`           | `keyword` | `term`                | Exact status                        |
| `status`           | `keyword` | `terms`               | Multiple statuses                   |
| `status`           | `keyword` | `exists`              | Check whether field exists          |
| `flight_id`        | `keyword` | `term`                | Exact flight ID                     |
| `flight_id`        | `keyword` | `terms`               | Multiple flight IDs                 |
| `flight_id`        | `keyword` | `prefix`              | Flight IDs beginning with something |
| `origin_code`      | `keyword` | `term`                | Exact airport code                  |
| `origin_code`      | `keyword` | `terms`               | Multiple origin airports            |
| `destination_code` | `keyword` | `term`                | Exact destination                   |
| `destination_code` | `keyword` | `terms`               | Multiple destinations               |
| `delay_minutes`    | `integer` | `range`               | Greater/less than a number          |
| `delay_minutes`    | `integer` | `term`                | Exact number                        |
| `delay_minutes`    | `integer` | `terms`               | Match specific numbers              |
| `passengers`       | `integer` | `range`               | Passenger count range               |
| `passengers`       | `integer` | `term`                | Exact passenger count               |
| `timestamp`        | `date`    | `range`               | Date/time range                     |
| `timestamp`        | `date`    | `term`                | Exact timestamp                     |
| Any field          | Any type  | `exists`              | Check field exists                  |
| Any field          | Any type  | `bool`                | Combine multiple conditions         |
| Any field          | Any type  | `bool.filter`         | Filtering without relevance scoring |
| Any field          | Any type  | `bool.must`           | Conditions that must match          |
| Any field          | Any type  | `bool.must_not`       | Exclude documents                   |
| Any field          | Any type  | `bool.should`         | OR-like conditions                  |
| Any field          | Any type  | `query_string`        | Advanced query syntax               |
| Any field          | Any type  | `simple_query_string` | Safer/simple query syntax           |


# Elasticsearch Query Examples

Practical Elasticsearch query examples using the `alerts` index.

---

## Table of Contents

* [1. Basic Search](#1-basic-search)
* [2. Size](#2-size)
* [3. Source Filtering](#3-source-filtering)
* [4. Term Query](#4-term-query)
* [5. Bool Query](#5-bool-query)

  * [Must](#must)
  * [Should](#should)
  * [Must Not](#must-not)
  * [Filter](#filter)
* [6. Range Query](#6-range-query)
* [7. Date Range](#7-date-range)
* [8. Term vs Match vs Match Phrase](#8-term-vs-match-vs-match-phrase)
* [9. Mapping](#9-mapping)
* [10. Sorting](#10-sorting)
* [11. Aggregations](#11-aggregations)

  * [Terms Aggregation](#terms-aggregation)
  * [Average](#average)
  * [Maximum](#maximum)
  * [Minimum](#minimum)
* [12. Real-World Query](#12-real-world-query)
* [13. Quick Reference](#13-quick-reference)

---

# 1. Basic Search

Search all documents from the `alerts` index.

```http
GET alerts/_search
```

By default, Elasticsearch returns **10 documents**.

---

# 2. Size

The `size` parameter controls how many documents Elasticsearch returns.

```http
GET alerts/_search
{
  "size": 1
}
```

For example:

```text
100 documents matched
        ↓
    size: 1
        ↓
1 document returned
```

Important:

```text
hits.total.value → Number of documents that matched
size             → Number of documents returned
```

Example:

```text
47 documents matched
20 documents returned
```

The response can therefore contain:

```text
hits.total.value = 47
hits.hits        = 20
```

---

# 3. Source Filtering

Use `_source` when you only want specific fields in the response.

```http
GET alerts/_search
{
  "_source": [
    "flight_id",
    "airline",
    "status"
  ]
}
```

Instead of returning the complete document, Elasticsearch returns only:

```text
flight_id
airline
status
```

---

# 4. Term Query

`term` is used for **exact-value matching**.

Example:

```http
GET alerts/_search
{
  "size": 100,
  "_source": [
    "airline"
  ],
  "query": {
    "term": {
      "status": "DELAYED"
    }
  }
}
```

This means:

> Find documents where `status` is exactly `DELAYED`.

`term` is commonly used with `keyword` fields.

---

# 5. Bool Query

The `bool` query allows multiple conditions to be combined.

It provides:

| Clause     | Meaning                             |
| ---------- | ----------------------------------- |
| `must`     | All conditions must match           |
| `should`   | At least one condition should match |
| `must_not` | Exclude matching documents          |
| `filter`   | Filter without relevance scoring    |

---

## Must

`must` means **all conditions must match**.

Example:

> Airline must be IndiGo AND status must be DELAYED.

```http
GET alerts/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "term": {
            "airline.keyword": "IndiGo"
          }
        },
        {
          "term": {
            "status": "DELAYED"
          }
        }
      ]
    }
  }
}
```

Logical representation:

```text
airline = IndiGo
       AND
status = DELAYED
```

---

## Should

`should` is used when documents should match **at least one condition**.

Example:

> Airline is IndiGo OR status is DELAYED.

```http
GET alerts/_search
{
  "query": {
    "bool": {
      "should": [
        {
          "term": {
            "airline.keyword": "IndiGo"
          }
        },
        {
          "term": {
            "status": "DELAYED"
          }
        }
      ]
    }
  }
}
```

Logical representation:

```text
airline = IndiGo
       OR
status = DELAYED
```

---

## Must Not

`must_not` is used to **exclude documents** matching the specified conditions.

```http
GET alerts/_search
{
  "query": {
    "bool": {
      "must_not": [
        {
          "term": {
            "airline.keyword": "IndiGo"
          }
        },
        {
          "term": {
            "status": "DELAYED"
          }
        }
      ]
    }
  }
}
```

This excludes documents that match either of the specified conditions.

Logical representation:

```text
NOT airline = IndiGo
AND
NOT status = DELAYED
```

---

## Filter

`filter` is used when you only need filtering and don't need relevance scoring.

```http
GET alerts/_search
{
  "query": {
    "bool": {
      "filter": [
        {
          "term": {
            "status": "DELAYED"
          }
        }
      ]
    }
  }
}
```

Filter queries normally return:

```text
_score = 0
```

because Elasticsearch does not calculate relevance scores for filter clauses.

### When to use filter

Use `filter` for structured conditions such as:

```text
status
airline
airport
delay_minutes
timestamp
```

Example:

```text
status = DELAYED
AND
airline = IndiGo
AND
delay > 30
```

---

# 6. Range Query

`range` is used to search values within a range.

### Range operators

| Operator | Meaning               |
| -------- | --------------------- |
| `gt`     | Greater than          |
| `gte`    | Greater than or equal |
| `lt`     | Less than             |
| `lte`    | Less than or equal    |

Example:

```http
GET alerts/_search
{
  "_source": [
    "timestamp"
  ],
  "query": {
    "range": {
      "delay_minutes": {
        "gt": 30
      }
    }
  }
}
```

This means:

```text
delay_minutes > 30
```

---

# 7. Date Range

You can also use `range` with date fields.

Example:

```http
GET alerts/_search
{
  "query": {
    "bool": {
      "filter": [
        {
          "range": {
            "timestamp": {
              "gte": "now/d",
              "lt": "now+1d/d"
            }
          }
        },
        {
          "range": {
            "delay_minutes": {
              "gt": 30
            }
          }
        }
      ]
    }
  }
}
```

This means:

```text
timestamp = today
AND
delay_minutes > 30
```

### Understanding `now/d`

`now` means the current date and time.

`/d` rounds the time down to the beginning of the day.

For example, if the current time is:

```text
28-09-2026 23:31
```

then:

```text
now/d
↓
28-09-2026 00:00
```

And:

```text
now+1d/d
↓
29-09-2026 00:00
```

Therefore:

```text
gte: now/d
lt:  now+1d/d
```

means:

```text
28-09-2026 00:00
        <= timestamp
        <
29-09-2026 00:00
```

---

# 8. Term vs Match vs Match Phrase

The query method depends on the **field mapping**.

---

## Term

`term` is used for exact-value matching.

```http
GET alerts/_search
{
  "query": {
    "term": {
      "status": "DELAYED"
    }
  }
}
```

`status` is a `keyword` field, so `term` is appropriate.

---

## Match

`match` is used for full-text searching on `text` fields.

```http
GET alerts/_search
{
  "query": {
    "match": {
      "message": "bad weather"
    }
  }
}
```

Elasticsearch analyzes the search text before searching.

---

## Match Phrase

`match_phrase` searches for words as a phrase in the same order.

```http
GET alerts/_search
{
  "query": {
    "match_phrase": {
      "message": "Flight AI1256 from Chennai to Bangalore is delayed by 228 minutes because of weather conditions"
    }
  }
}
```

### Quick comparison

```text
term
 ↓
Exact term/value

match
 ↓
Full-text search

match_phrase
 ↓
Full-text phrase search
```

---

# 9. Mapping

To see the mapping of the `alerts` index:

```http
GET alerts/_mapping
```

The mapping tells you the data type of each field.

For example:

```text
message          → text
airline          → text
airline.keyword  → keyword
status           → keyword
delay_minutes    → integer
timestamp        → date
```

The mapping helps determine which query type should be used.

### Field Mapping vs Query

| Field Type | Typical Query           | Example         |
| ---------- | ----------------------- | --------------- |
| `text`     | `match`, `match_phrase` | `message`       |
| `keyword`  | `term`, `terms`         | `status`        |
| `integer`  | `range`, `term`         | `delay_minutes` |
| `date`     | `range`                 | `timestamp`     |

---

# 10. Sorting

Use `sort` to control the order of returned documents.

---

## Ascending

`asc` means **oldest to newest** when sorting a date field.

```http
GET alerts/_search
{
  "sort": [
    {
      "timestamp": {
        "order": "asc"
      }
    }
  ]
}
```

Example:

```text
10:00
11:00
12:00
13:00
```

---

## Descending

`desc` means **newest to oldest** when sorting a date field.

```http
GET alerts/_search
{
  "sort": [
    {
      "timestamp": {
        "order": "desc"
      }
    }
  ]
}
```

Example:

```text
13:00
12:00
11:00
10:00
```

---

# 11. Aggregations

Aggregations are used when you want **statistics instead of individual documents**.

Think of it as:

```text
Search:
"Give me documents"

Aggregation:
"Give me statistics"
```

---

## Terms Aggregation

Count documents by airline.

```http
GET alerts/_search
{
  "size": 0,
  "aggs": {
    "airlines": {
      "terms": {
        "field": "airline.keyword"
      }
    }
  }
}
```

Example result conceptually:

```text
IndiGo             150
Air India          120
Emirates            90
Lufthansa           80
Qatar Airways       70
```

`size: 0` is used because we don't need individual documents. We only need the aggregation result.

---

## Average

Find the average delay.

```http
GET alerts/_search
{
  "size": 0,
  "aggs": {
    "average_delay": {
      "avg": {
        "field": "delay_minutes"
      }
    }
  }
}
```

Conceptually:

```text
Average delay = 47.3 minutes
```

---

## Maximum

Find the maximum delay.

```http
GET alerts/_search
{
  "size": 0,
  "aggs": {
    "maximum_delay": {
      "max": {
        "field": "delay_minutes"
      }
    }
  }
}
```

Conceptually:

```text
Maximum delay = 228 minutes
```

---

## Minimum

Find the minimum delay.

```http
GET alerts/_search
{
  "size": 0,
  "aggs": {
    "minimum_delay": {
      "min": {
        "field": "delay_minutes"
      }
    }
  }
}
``
```


```
GET alerts/_search
{
  "size": 1000,
  "_source": [
    "flight_id",
    "airline",
    "status",
    "delay_minutes",
    "timestamp"
  ],
  "query": {
    "bool": {
      "filter": [
        {
          "term": {
            "airline.keyword": "Air India"
          }
        },
        {
          "term": {
            "status": "DELAYED"
          }
        },
        {
          "range": {
            "delay_minutes": {
              "gt": 30
            }
          }
        },
        {
          "range": {
            "timestamp": {
              "gte": "now-24h",
              "lte": "now"
            }
          }
        }
      ]
    }
  },
  "sort": [
    {
      "timestamp": {
        "order": "desc"
      }
    }
  ]
}
```
