from src.detail import Detail
from src.errors import DuplicateIdError, ItemNotFoundError
class Catalog():

    def __init__(self)->None:
        self.items: dict[str,Detail] = {}
    def add(self,item:Detail)-> None:
        if item.identifier in self.items:
            raise DuplicateIdError
        else:
            self.items[item.identifier] = item
    def get(self,id:str)->Detail    :
        if id in self.items:
            return self.items[id]
        else:
            raise ItemNotFoundError

    def remove(self,id:str )->None:
        if id in self.items:
            del self.items[id]
        else:
            raise ItemNotFoundError
    def __len__(self)->int:
        return len(self.items) 
    

