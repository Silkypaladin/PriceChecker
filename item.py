class Item(object):
    def __init__(self, name="", parameters="", price="", link=""):
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
        self.name = data["Name"]
        self.parameters = data["Parameters"]
        self.price = data["Price"]
        self.link = data["Link"]

    def __str__(self):
        info = f""" 
        Name: {self.name}
        Parameters: {", ".join(self.parameters)}
        Price: {self.price}
        Link: {self.link}
        """
        print(info)
        