from datetime import datetime


class ProductClass():

    def __init__(self, name):
        super().__init__()

        self._name = name #Column(String(255), nullable=False, unique=True)
        self._description = None #Column(LONGTEXT, nullable=False)
        self._active = None #Column(TINYINT(1), nullable=False)
        self._created = None #Column(DateTime, nullable=False)

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def description(self):
        return self._description
    
    @description.setter
    def description(self, value: str):
        self._description = value

    @property
    def active(self):
        return self._active
    
    @active.setter
    def active(self, value: bool):
        self._active = value

    @property
    def created(self):
        return self._created
    
    @created.setter
    def created(self, value):
        self._created = value
