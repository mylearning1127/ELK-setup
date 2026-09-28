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
