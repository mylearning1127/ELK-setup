import os
import time
import random
import uuid
from datetime import datetime, timezone, timedelta

from elasticsearch import Elasticsearch


ES_URL = os.getenv(
    "ELASTICSEARCH_URL",
    "http://localhost:9200"
)

INDEX_NAME = "alerts"


AIRLINES = [
    "Air India",
    "IndiGo",
    "Emirates",
    "Lufthansa",
    "Qatar Airways",
    "Singapore Airlines",
    "British Airways"
]

AIRPORTS = [
    {
        "code": "MAA",
        "city": "Chennai"
    },
    {
        "code": "DEL",
        "city": "Delhi"
    },
    {
        "code": "BOM",
        "city": "Mumbai"
    },
    {
        "code": "BLR",
        "city": "Bangalore"
    },
    {
        "code": "HYD",
        "city": "Hyderabad"
    },
    {
        "code": "DXB",
        "city": "Dubai"
    },
    {
        "code": "LHR",
        "city": "London"
    },
    {
        "code": "FRA",
        "city": "Frankfurt"
    },
    {
        "code": "SIN",
        "city": "Singapore"
    },
    {
        "code": "DOH",
        "city": "Doha"
    }
]


STATUSES = [
    "ON_TIME",
    "DELAYED",
    "CANCELLED",
    "BOARDING",
    "DEPARTED",
    "LANDED"
]


DELAY_REASONS = [
    "Weather conditions",
    "Technical issue",
    "Air traffic congestion",
    "Late arrival of aircraft",
    "Crew availability",
    "Security check",
    "Ground handling delay"
]


def connect_to_elasticsearch():

    print(f"Connecting to Elasticsearch: {ES_URL}")

    while True:

        try:

            es = Elasticsearch(
                ES_URL,
                request_timeout=10
            )

            if es.ping():

                print("Connected to Elasticsearch")

                return es

        except Exception as e:

            print(f"Elasticsearch not ready: {e}")

        time.sleep(5)


def create_index(es):

    if es.indices.exists(index=INDEX_NAME):

        print(f"Index '{INDEX_NAME}' already exists")

        return

    mapping = {

        "mappings": {

            "properties": {

                "flight_id": {
                    "type": "keyword"
                },

                "airline": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword"
                        }
                    }
                },

                "flight_number": {
                    "type": "keyword"
                },

                "origin": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword"
                        }
                    }
                },

                "destination": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword"
                        }
                    }
                },

                "origin_code": {
                    "type": "keyword"
                },

                "destination_code": {
                    "type": "keyword"
                },

                "status": {
                    "type": "keyword"
                },

                "delay_minutes": {
                    "type": "integer"
                },

                "delay_reason": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword"
                        }
                    }
                },

                "passengers": {
                    "type": "integer"
                },

                "gate": {
                    "type": "keyword"
                },

                "timestamp": {
                    "type": "date"
                },

                "message": {
                    "type": "text"
                }

            }

        }

    }

    es.indices.create(
        index=INDEX_NAME,
        body=mapping
    )

    print(f"Created index '{INDEX_NAME}'")


def generate_flight():

    airline = random.choice(AIRLINES)

    origin = random.choice(AIRPORTS)

    destination = random.choice(
        [
            airport
            for airport in AIRPORTS
            if airport["code"] != origin["code"]
        ]
    )

    status = random.choice(STATUSES)

    delay_minutes = 0
    delay_reason = None

    if status == "DELAYED":

        delay_minutes = random.randint(5, 240)

        delay_reason = random.choice(
            DELAY_REASONS
        )

    flight_number = (
        random.choice(["AI", "6E", "EK", "LH", "QR", "SQ", "BA"])
        + str(random.randint(100, 9999))
    )

    flight_id = str(uuid.uuid4())

    passengers = random.randint(
        80,
        420
    )

    gate = (
        random.choice(
            ["A", "B", "C", "D"]
        )
        + str(random.randint(1, 30))
    )

    # Generate timestamps across the last 7 days
    timestamp = (
        datetime.now(timezone.utc)
        - timedelta(
            minutes=random.randint(
                0,
                7 * 24 * 60
            )
        )
    )

    timestamp_string = timestamp.isoformat()

    if status == "DELAYED":

        message = (
            f"Flight {flight_number} from "
            f"{origin['city']} to "
            f"{destination['city']} is delayed "
            f"by {delay_minutes} minutes "
            f"because of {delay_reason.lower()}."
        )

    elif status == "CANCELLED":

        message = (
            f"Flight {flight_number} from "
            f"{origin['city']} to "
            f"{destination['city']} has been cancelled."
        )

    elif status == "BOARDING":

        message = (
            f"Flight {flight_number} from "
            f"{origin['city']} to "
            f"{destination['city']} is now boarding "
            f"at gate {gate}."
        )

    else:

        message = (
            f"Flight {flight_number} from "
            f"{origin['city']} to "
            f"{destination['city']} "
            f"is currently {status.lower().replace('_', ' ')}."
        )

    return {

        "flight_id": flight_id,

        "airline": airline,

        "flight_number": flight_number,

        "origin": origin["city"],

        "destination": destination["city"],

        "origin_code": origin["code"],

        "destination_code": destination["code"],

        "status": status,

        "delay_minutes": delay_minutes,

        "delay_reason": delay_reason,

        "passengers": passengers,

        "gate": gate,

        "timestamp": timestamp_string,

        "message": message

    }


def main():

    es = connect_to_elasticsearch()

    create_index(es)

    print()
    print("========================================")
    print(" Flight Alert Producer Started")
    print("========================================")
    print()

    while True:

        try:

            flight = generate_flight()

            response = es.index(
                index=INDEX_NAME,
                document=flight
            )

            print(
                f"[{flight['timestamp']}] "
                f"{flight['flight_number']} | "
                f"{flight['airline']} | "
                f"{flight['origin_code']} -> "
                f"{flight['destination_code']} | "
                f"{flight['status']} | "
                f"delay={flight['delay_minutes']} min | "
                f"id={response['_id']}"
            )

            # Generate one document every 2 seconds
            time.sleep(2)

        except Exception as e:

            print(
                f"Error sending document: {e}"
            )

            time.sleep(5)


if __name__ == "__main__":

    main()
