from datetime import datetime
from typing import Dict
from uuid import UUID


class Item:
    def __init__(self, id: UUID, name: str):
        pass

class Inventory:
    def __init__(self, user_id: UUID, created_at: datetime, updated_at: datetime):
        self.user_id = user_id
        self.created_at = created_at
        self.updated_at = updated_at
        self.items = []


    @property
    def items(self):
        return self.__items

    @items.setter
    def items(self, items: Dict[UUID, Item]):
        self.__items = items
    @property
    def user_id(self):
        return self.__user_id

    @user_id.setter
    def user_id(self, user_id: UUID):
        self.__user_id = user_id

    @property
    def created_at(self):
        return self.__created_at

    @created_at.setter
    def created_at(self, created_at: datetime):
        self.__created_at = created_at

    @property
    def updated_at(self):
        return self.__updated_at

    @updated_at.setter
    def updated_at(self, updated_at: datetime):
        self.__updated_at = updated_at

    def add_item(self, item_id: UUID, item_name: str):
        if not self.__has_slots_available():
            raise Exception('There are no more slots available in the inventory')

        new_item = Item(item_id, item_name)
        self.items[item_id] = new_item
        self.updated_at = datetime.now()

    def __has_slots_available(self):
        return len(self.items) < 50

    def drop_items(self, item_ids:[UUID]):
        self.items = {k:round(v) for k, v in item_ids}

    def __drop_single_item(self, item_id: UUID):
        if item_id in self.items:
            del self.items[item_id]

