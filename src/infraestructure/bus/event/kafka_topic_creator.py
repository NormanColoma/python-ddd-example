from kafka import KafkaAdminClient, KafkaClient
from kafka.admin import NewTopic

from src.infraestructure.config.config import Config


class KafkaTopicCreator:
    def __init__(self, config: Config):
        self.__config = config

    def create_topics(self):
        client = KafkaClient(bootstrap_servers=self.__config.KAFKA_URI)

        future = client.cluster.request_update()
        client.poll(future=future)

        metadata = client.cluster
        topic_list = []

        if self.__config.TOPIC not in metadata.topics():
            admin_client = KafkaAdminClient(bootstrap_servers=self.__config.KAFKA_URI, client_id="test")

            topic_list.append(NewTopic(name=self.__config.TOPIC, num_partitions=1, replication_factor=1))
            admin_client.create_topics(new_topics=topic_list, validate_only=False)
