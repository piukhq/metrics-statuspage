import argparse
import random
import time

import requests

api_key = "432537fe-12a0-4f9c-aa23-7964fb2053db"
page_id = "wx6qpqvzjkw1"


def rabbit_queue():
    metric_id = "lm78zp8xzyys"
    metric_name = "RabbitMQ Queue data"
    prometheus = "http://localhost:9090/api/v1/query"
    headers = {"Content-Type": "application/json"}
    params = {
        "query": 'sum(rate(rabbitmq_queue_messages_ack_total{kubernetes_cluster="prod0"}[2m])) * 120'
    }

    response = requests.get(prometheus, params, headers=headers)
    data = response.json()
    value = data["data"]["result"][0]["value"][1]
    ts = data["data"]["result"][0]["value"][0]

    post_metrics(value, ts, metric_id, page_id, metric_name)


def generate_rps():
    hermes_rpm = random.randint(98, 132)
    hermes_rpm_metric = "4qfyp4zp6fhp"
    hermes_rpm_name = "Hermes RPM"
    cluster_rps = random.randint(212, 282)
    cluster_rps_metric = "ylx0y4wxm07c"
    cluster_rps_name = "Cluster RPS"
    ts = int(time.time())
    post_metrics(hermes_rpm, ts, hermes_rpm_metric, page_id, hermes_rpm_name)
    post_metrics(cluster_rps, ts, cluster_rps_metric, page_id, cluster_rps_name)


# Used by functions to send data to Statuspage
def post_metrics(metric_value, ts, metric_id, page_id, metric_name):
    url = f"https://api.statuspage.io/v1/pages/{page_id}/metrics/{metric_id}/data"
    metric_name = metric_name
    data = {"data": {"timestamp": ts, "value": metric_value}}
    headers = {
        "Content-Type": "application/json",
        "Authorization": "OAuth " + api_key,
    }

    response = requests.post(url, headers=headers, json=data)
    print(metric_name, response.text)


def main():
    arg = argparse.ArgumentParser()
    arg.add_argument(
        "--rabbit",
        action="store_true",
        help="rabbitmq queue numbers data grab and push",
    )
    arg.add_argument(
        "--generate",
        action="store_true",
        help="generate the data for hermes RPM and cluster RPS amd push",
    )
    args = arg.parse_args()

    if args.rabbit:
        rabbit_queue()
    elif args.generate:
        generate_rps()


if __name__ == "__main__":
    main()
