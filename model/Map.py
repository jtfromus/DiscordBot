# define map class
class Map:
    def __init__(self, name, url, description):
        self.name = name
        self.image_url = url
        self.description = description

    def get_name(self):
        return self.name

    def get_image_url(self):
        return self.image_url

    def get_description(self):
        return self.description

    def set_name(self, name):
        self.name = name

    def set_image_url(self, url):
        self.image_url = url

    def set_description(self, description):
        self.description = description
