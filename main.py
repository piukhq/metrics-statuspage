import argparse
import logging
import random
import time

import requests
from pythonjsonlogger import jsonlogger

from settings import settings

logger = logging.getLogger()
logHandler = logging.StreamHandler()
logFmt = jsonlogger.JsonFormatter(timestamp=True)
logHandler.setFormatter(logFmt)
logger.addHandler(logHandler)


def rabbit_metrics() -> None:
    prom_ips = settings.prom_ips.split(",")
    headers = {"Content-Type": "application/json"}
    params = {"query": "sum(rate(rabbitmq_queue_messages_ack_total[2m])) * 120"}
    servers_available = len(prom_ips)
    for ip in prom_ips:
        logging_extras = {"prometheus_ip": ip}
        try:
            logging.warning("Attempting to get RabbitMQ Metrics", extra=logging_extras)
            r = requests.get(f"http://{ip}:9090/api/v1/query", params=params, headers=headers).json()
            break
        except Exception:
            servers_available -= 1
            if servers_available == 0:
                logging.warning("RabbitMQ Metric collection attempts exhausted, request failed", extra=logging_extras)
                return None
            else:
                logging.warning("RabbitMQ Metric collection failed, attempting next server", extra=logging_extras)
                continue
    data = {
        "name": "RabbitMQ Queue data",
        "id": "lm78zp8xzyys",
        "timestamp": int(float(r["data"]["result"][0]["value"][0])),
        "value": int(float(r["data"]["result"][0]["value"][1])),
    }
    logging.warning("Gathered RabbitMQ metrics successfully", extra={"data": data})
    post_to_stauspage(timestamp=data["timestamp"], value=data["value"], id=data["id"], name=data["name"])


def fake_metrics() -> None:
    data = {
        "hermes": {
            "name": "Hermes RPM",
            "id": "4qfyp4zp6fhp",
            "timestamp": int(time.time()),
            "value": random.randint(98, 132),
        },
        "cluster": {
            "name": "Cluster RPS",
            "id": "ylx0y4wxm07c",
            "timestamp": int(time.time()),
            "value": random.randint(212, 282),
        },
    }
    logging.warning("Generated fake data successfully", extra={"data": data})
    post_to_stauspage(
        timestamp=data["hermes"]["timestamp"],
        value=data["hermes"]["value"],
        id=data["hermes"]["id"],
        name=data["hermes"]["name"],
    )
    post_to_stauspage(
        timestamp=data["cluster"]["timestamp"],
        value=data["cluster"]["value"],
        id=data["cluster"]["id"],
        name=data["cluster"]["name"],
    )


def post_to_stauspage(timestamp: int, value: int, id: str, name: str) -> None:
    url = f"https://api.statuspage.io/v1/pages/{settings.sp_page_id}/metrics/{id}/data"
    data = {"data": {"timestamp": timestamp, "value": value}}
    headers = {
        "Content-Type": "application/json",
        "Authorization": "OAuth " + settings.sp_api_key,
    }

    for i in range(settings.retry_count):
        attempt = i + 1
        log_extras = {"retry_count": attempt, "retry_max": settings.retry_count, "metric_name": name}
        try:
            logging.warning("Sending Metric to Statuspage", extra=log_extras)
            requests.post(url, headers=headers, json=data).raise_for_status()
            break
        except Exception:
            if attempt < settings.retry_count:
                logging.warning("Retrying Sending Metric to Statuspage", extra=log_extras)
                continue
            else:
                logging.warning("Giving up Sending Metric to Statuspage")
                break


def main():
    arg = argparse.ArgumentParser()
    arg.add_argument(
        "--rabbit",
        action="store_true",
        help="Fetch total number of ack'd messages in RabbitMQ",
    )
    arg.add_argument(
        "--generate",
        action="store_true",
        help="Generate fake data for Hermes RPM and Cluster RPS",
    )
    args = arg.parse_args()

    if args.rabbit:
        rabbit_metrics()
    elif args.generate:
        fake_metrics()
    else:
        print("Run '--help' for more info")


if __name__ == "__main__":
    main()
