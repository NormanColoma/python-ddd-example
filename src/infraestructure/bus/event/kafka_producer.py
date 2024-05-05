import json

from src.infraestructure.config.config import Config
from kafka import KafkaProducer as kafkaProducer

class KafkaProducer:
    def __init__(self, config: Config):
        self.__producer = kafkaProducer(bootstrap_servers=config.KAFKA_URI, value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    def send(self, topic: str, payload: dict):
        self.__producer.send(topic, payload)

