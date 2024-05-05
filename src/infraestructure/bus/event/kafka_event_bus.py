from src.domain.core.bus.event.domain_event import DomainEvent
from src.domain.core.bus.event.event_bus import EventBus
from src.infraestructure.bus.event.kafka_producer import KafkaProducer
from src.infraestructure.bus.event.kafka_topic_creator import KafkaTopicCreator


class KafkaEventBus(EventBus):
    def __init__(self, producer: KafkaProducer, topic_creator: KafkaTopicCreator):
        self.__producer = producer
        topic_creator.create_topics()

    def publish(self, events: [DomainEvent]) -> None:
        print('publishing domain events...')
        for event in events:
            self.__producer.send(topic=event.topic, payload=event.to_json())

