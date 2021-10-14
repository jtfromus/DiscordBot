# define map class
class Map:
    def __init__(self, name: str, url: str, description: str):
        self.name = name
        self.image_url = url
        self.description = description

    def get_name(self) -> str:
        return self.name

    def get_image_url(self) -> str:
        return self.image_url

    def get_description(self) -> str:
        return self.description

    def set_name(self, name) -> None:
        self.name = name

    def set_image_url(self, url) -> None:
        self.image_url = url

    def set_description(self, description) -> None:
        self.description = description
