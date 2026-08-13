# Учебный генератор событий.
# Пишет JSON в стандартный поток (его забирает Filebeat)
# и дублирует ту же строку в Logstash по TCP (порт 5000).

import json
import random
import socket
import time

LOGSTASH_HOST = "logstash"
LOGSTASH_PORT = 5000
EVENTS = ("login", "logout", "purchase", "error", "heartbeat")


def send_tcp(line):
    """Одна JSON-строка с переводом строки — формат json_lines в Logstash."""
    try:
        connection = socket.create_connection((LOGSTASH_HOST, LOGSTASH_PORT), timeout=3)
        connection.sendall((line + "\n").encode("utf-8"))
        connection.close()
    except OSError:
        # Logstash может быть ещё не готов; следующая итерация повторит попытку.
        pass


def main():
    while True:
        document = {
            "app": "dummy",
            "event": random.choice(EVENTS),
            "value": random.randint(1, 100),
            "message": "dummy event",
        }
        line = json.dumps(document, ensure_ascii=True)
        print(line, flush=True)
        send_tcp(line)
        time.sleep(2)


if __name__ == "__main__":
    main()
