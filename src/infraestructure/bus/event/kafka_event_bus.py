import json
import os

from kafka import KafkaAdminClient, KafkaClient
from kafka.admin import NewTopic

from src.domain.core.bus.event.domain_event import DomainEvent
from src.domain.core.bus.event.event_bus import EventBus
from src.infraestructure.bus.event.kafka_producer import KafkaProducer
from src.infraestructure.config.config import app_config


class KafkaEventBus(EventBus):
    def __init__(self, producer: KafkaProducer):
        self.__producer = producer

    def publish(self, events: [DomainEvent]) -> None:

        """
        client = KafkaClient(bootstrap_servers=app_config[os.getenv('ENV')].KAFKA_URI)

        future = client.cluster.request_update()
        client.poll(future=future)

        metadata = client.cluster

        if 'teams' not in metadata.topics():
            admin_client = KafkaAdminClient(
                bootstrap_servers=app_config[os.getenv('ENV')].KAFKA_URI,
                client_id='test'
            )

            topic_list = []
            topic_list.append(NewTopic(name="teams", num_partitions=1, replication_factor=1))
            admin_client.create_topics(new_topics=topic_list, validate_only=False)
        """

        print('publishing domain events...')
        for event in events:
            self.__producer.send(topic=event.topic, payload=event.to_json())

