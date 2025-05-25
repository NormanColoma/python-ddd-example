import json

from kafka import KafkaProducer as kafkaProducer

from src.infraestructure.config.config import Config


class KafkaProducer:
    def __init__(self, config: Config):
        self.__producer = kafkaProducer(
            bootstrap_servers=config.KAFKA_URI, value_serializer=lambda v: json.dumps(v).encode("utf-8")
        )

    def send(self, topic: str, payload: dict):
        self.__producer.send(topic, payload)
