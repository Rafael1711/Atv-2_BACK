import json
import os
from django.conf import settings


class Instrument:
    JSON_FILE = os.path.join(settings.BASE_DIR, 'instruments_data.json')

    def __init__(self, id=None, name=None, category=None, price=None, description=None):
        self.id = id
        self.name = name
        self.category = category
        self.price = price
        self.description = description

    @classmethod
    def _load_data(cls):
        if not os.path.exists(cls.JSON_FILE):
            return []
        try:
            with open(cls.JSON_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except json.JSONDecodeError:
            return []

    @classmethod
    def _save_data(cls, data):
        with open(cls.JSON_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    @classmethod
    def get_all(cls):
        return cls._load_data()

    @classmethod
    def get_by_id(cls, id):
        instruments = cls._load_data()
        return next((i for i in instruments if i['id'] == id), None)

    @classmethod
    def create(cls, **kwargs):
        instruments = cls._load_data()
        new_id = max([i['id'] for i in instruments], default=0) + 1
        new_instrument = {
            'id': new_id,
            'name': kwargs.get('name'),
            'category': kwargs.get('category'),
            'price': kwargs.get('price'),
            'description': kwargs.get('description'),
        }
        instruments.append(new_instrument)
        cls._save_data(instruments)
        return new_instrument

    @classmethod
    def update(cls, id, **kwargs):
        instruments = cls._load_data()
        for i, instrument in enumerate(instruments):
            if instrument['id'] == id:
                instruments[i].update({
                    'name': kwargs.get('name', instrument['name']),
                    'category': kwargs.get('category', instrument['category']),
                    'price': kwargs.get('price', instrument['price']),
                    'description': kwargs.get('description', instrument['description']),
                })
                cls._save_data(instruments)
                return instruments[i]
        return None

    @classmethod
    def delete(cls, id):
        instruments = cls._load_data()
        instruments = [i for i in instruments if i['id'] != id]
        cls._save_data(instruments)
