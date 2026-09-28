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

This section contains commonly used Elasticsearch queries for the `alerts` index.

---

## 1. Search All Documents

```http
GET alerts/_search
```

By default, Elasticsearch returns 10 documents.

---

## 2. Limit the Number of Results

```http
GET alerts/_search
{
  "size": 1
}
```

`size` controls how many documents Elasticsearch returns.

---

## 3. Select Specific Fields

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

`_source` allows you to return only the fields you need.

---

## 4. Term Query

`term` is used for **exact-value matching**.

Example: Find delayed flights.

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

---

# Bool Queries

The `bool` query is used to combine multiple conditions.

It provides:

* `must` → All conditions must match
* `should` → At least one condition should match
* `must_not` → Exclude matching documents
* `filter` → Filter documents without relevance scoring

---

## 5. Must

`must` means **all conditions must match**.

Example:

> Airline must be IndiGo **AND** status must be DELAYED.

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

Both conditions must be satisfied.

---

## 6. Should

`should` means **at least one condition should match**.

Example:

> Airline is IndiGo **OR** status is DELAYED.

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

A document matches if at least one of the conditions is satisfied.

---

## 7. Must Not

`must_not` is used to **exclude documents** that match the specified conditions.

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

This excludes documents matching the specified conditions.

> **Note:** Multiple conditions inside `must_not` exclude documents matching **any** of those conditions.

---

## 8. Filter

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

Filter queries do not calculate relevance scores, so matching documents normally have:

```text
"_score": 0
```

---

# Range Queries

`range` is used for numbers and dates.

### Range operators

| Operator | Meaning               |
| -------- | --------------------- |
| `gt`     | Greater than          |
| `gte`    | Greater than or equal |
| `lt`     | Less than             |
| `lte`    | Less than or equal    |

---

## 9. Number Range

Find flights delayed by more than 30 minutes.

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

## 10. Date Range

Find flights from today.

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

This query has two conditions:

```text
timestamp = today
AND
delay_minutes > 30
```

### Understanding `now/d`

`now/d` rounds the current time down to the beginning of today.

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

# Term vs Match vs Match Phrase

The query method depends mainly on the **field mapping**.

First, check the mapping:

```http
GET alerts/_mapping
```

---

## 11. Term Query

`term` is used for **exact-value matching**.

Example:

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

`status` is mapped as a `keyword`, so `term` is appropriate.

---

## 12. Match Query

`match` is used for **full-text searching** on `text` fields.

Example:

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

The search text is analyzed before searching.

---

## 13. Match Phrase Query

`match_phrase` is used when you want to search for a phrase in the same order.

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

---

# Field Mapping vs Query Type

The field mapping helps determine which query is appropriate.

| Field Type | Typical Queries         | Example         |
| ---------- | ----------------------- | --------------- |
| `text`     | `match`, `match_phrase` | `message`       |
| `keyword`  | `term`, `terms`         | `status`        |
| `integer`  | `range`, `term`         | `delay_minutes` |
| `date`     | `range`                 | `timestamp`     |

For the `alerts` index:

| Field              | Mapping   | Typical Query           |
| ------------------ | --------- | ----------------------- |
| `message`          | `text`    | `match`, `match_phrase` |
| `airline`          | `text`    | `match`                 |
| `airline.keyword`  | `keyword` | `term`, `terms`         |
| `status`           | `keyword` | `term`, `terms`         |
| `flight_id`        | `keyword` | `term`, `terms`         |
| `origin_code`      | `keyword` | `term`, `terms`         |
| `destination_code` | `keyword` | `term`, `terms`         |
| `delay_minutes`    | `integer` | `range`, `term`         |
| `passengers`       | `integer` | `range`, `term`         |
| `timestamp`        | `date`    | `range`                 |

### Quick Mental Model

```text
TEXT
 ├── match
 └── match_phrase

KEYWORD
 ├── term
 └── terms

NUMBER
 ├── range
 └── term

DATE
 └── range

MULTIPLE CONDITIONS
 └── bool
      ├── must
      ├── should
      ├── must_not
      └── filter
```

---

## 14. Complete Mapping

To see the mapping of the `alerts` index:

```http
GET alerts/_mapping
```

To check the mapping of a specific field:

```http
GET alerts/_mapping/field/message
```

```http
GET alerts/_mapping/field/status
```

```http
GET alerts/_mapping/field/airline
```

