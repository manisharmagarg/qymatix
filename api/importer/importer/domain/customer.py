
class Customer():
    
    def __init__(self, name):
        super().__init__()

        self._name = name #Column(String(255), nullable=False, unique=True)
        self._address = None #Column(String(255), nullable=False)
        self._postcode = None #Column(String(255), nullable=False)
        self._city = None #Column(String(255), nullable=False)
        self._country = None #Column(String(255), nullable=False)
        self._revenue = None #Column(Float(asdecimal=True), nullable=False)
        self._employees = None #Column(INTEGER(11), nullable=False)
        self._industry = None #Column(String(255), nullable=False)
        self._classification = None #Column(String(255), nullable=False)
        self._website = None #Column(Text, nullable=False)
        self._comment = None #Column(LONGTEXT, nullable=False)
        self._favorite = None #Column(TINYINT(1), nullable=False)
        self._telephone = None #Column(Text, nullable=False)
        self._customer_parent_id = None #Column(Text, nullable=False)

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def address(self):
        return self._address
    
    @address.setter
    def name(self, value: str):
        self._address = value

    @property
    def postcode(self):
        return self._postcode
    
    @postcode.setter
    def postcode(self, value: str):
        self._postcode = value

    @property
    def city(self):
        return self._city
    
    @city.setter
    def city(self, value: str):
        self._city = value

    @property
    def country(self):
        return self._country
    
    @country.setter
    def country(self, value: str):
        self._country = value

    @property
    def revenue(self):
        return self._revenue
    
    @revenue.setter
    def revenue(self, value: float):
        self._revenue = value

    @property
    def employees(self):
        return self._employees
    
    @employees.setter
    def employees(self, value: int):
        self._employees = value

    @property
    def industry (self):
        return self._industry
    
    @industry.setter
    def industry(self, value: str):
        self._industry = value

    @property
    def classification(self):
        return self._classification
    
    @classification.setter
    def classification(self, value: str):
        self._classification = value

    @property
    def website(self):
        return self._website
    
    @website.setter
    def website(self, value: str):
        self._website = value

    @property
    def comment(self):
        return self._comment
    
    @comment.setter
    def comment(self, value: str):
        self._comment = value

    @property
    def favorite(self):
        return self._favorite
    
    @favorite.setter
    def favorite(self, value: int):
        self._favorite = value

    @property
    def telephone(self):
        return self._telephone
    
    @telephone.setter
    def telephone(self, value: str):
        self._telephone = value

    @property
    def customer_parent_id(self):
        return self._customer_parent_id
    
    @customer_parent_id.setter
    def customer_parent_id(self, value: int):
        self._customer_parent_id = value
