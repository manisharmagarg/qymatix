class Price():

    def __init__(self, value):
        super().__init__()

        if value < 0:
            raise ValueError("Price cannot be negative")