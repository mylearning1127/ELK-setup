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



GET alerts/_search

GET alerts/_search
{
  "size": 1
}


GET alerts/_search
{
  "_source": [
    "flight_id",
    "airline",
    "status"
  ]
}


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

# Must => all condition should match
# Example, the total values is 15 where both condition matched

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


# Atleast any one condition should match
# Example, Here, total values is 213 because of should concept.
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

# must_not, exclude the condition
# Example, Here, total values is 614 because of must_not concept.
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


# Filter Used when you only need filtering and don't need relevance scoring.
# max_score value is 0
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

# gt  = greater than
# gte = greater than or equal
# lt  = less than
# lte = less than or equal
# GET alerts/_search
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

# now/d round of today't time to 00:00 and now+1d/d represents next day 00:00. for example the current time is 28-09-2026 23:31, so it assumes gte: 28-09-2026 00:00 & lte: 29-09-2026 00:00
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


# Difference between term & match
# TERM => Exact value matching
# match => Full-text search
# match_pharse =. full text search

# Based on mapping we have to finalise the method.
# Term can be used in keyword
# Match & Match_pharse can be used in text
# Range can be used in integer & Date

GET alerts/_mapping

GET alerts/_search
{
  "query": {
    "term": {
      "status": "DELAYED"
    }
  }
}


GET alerts/_search
{
  "query": {
    "match": {
      "message": "bad weather"
    }
  }
}

GET alerts/_search
{
  "query": {
    "match_phrase": {
      "message": "Flight AI1256 from Chennai to Bangalore is delayed by 228 minutes because of weather conditions"
    }
  }
}
