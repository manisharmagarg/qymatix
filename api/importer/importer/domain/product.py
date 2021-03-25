from datetime import datetime


class Product():

    def __init__(self, name):
        super().__init__()

        self._name = name #Column(String(255), nullable=False, unique=True)
        self._product_type_id = None #Column(ForeignKey('product_type.id'), nullable=False, index=True)
        self._description = None #Column(LONGTEXT, nullable=False)
        self._active = None #Column(TINYINT(1), nullable=False)
        self._created = None #Column(DateTime, nullable=False)
        self._number = None #Column(String(255), nullable=False)
        self._serial = None #Column(String(255), nullable=False)
        self._product_type = None #relationship('ProductType')

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def product_type_id(self):
        return self._product_type_id
    
    @product_type_id.setter
    def product_type_id(self, value: int):
        self._product_type_id = value

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

    @property
    def number(self):
        return self._number
    
    @number.setter
    def number(self, value: str):
        self._number = value

    @property
    def serial(self):
        return self._serial
    
    @serial.setter
    def serial(self, value: str):
        self._serial = value
