from kafka import KafkaConsumer

from src.domain.core.bus.event.consumer import Consumer
from src.infraestructure.config.config import Config


class TeamCreatedConsumer(Consumer):
    def __init__(self, config: Config):
        super().__init__(config.TOPIC)
        self.__config = config

    def consume(self):
        kafka_consumer = KafkaConsumer(self.topic, bootstrap_servers=self.__config.KAFKA_URI)
        for msg in kafka_consumer:
            print(msg)
