class Item(object):
    def __init__(self, name, parameters, price, link):
        self.name = name
        self.parameters = parameters
        self.price = price
        self.link = link

    def format_to_json(self):
        return {
            "Name": self.name,
            "Parameters": self.parameters,
            "Price": self.price,
            "Link": self.link
        }
    def get_from_json(self, data):
        self.name = data["name"]
        self.parameters = data["parameters"]
        self.price = data["price"]
        self.link = data["link"]
    def __str__(self):
        info = f""" 
        Name: {self.name}
        Parameters: {", ".join(self.parameters)}
        Price: {self.price}
        Link: {self.link}
        """
        print(info)
        