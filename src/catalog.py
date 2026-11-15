from collections.abc import Iterator

from src.detail import Detail
from src.errors import DuplicateIdError, ItemNotFoundError


class Catalog:

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
    def __contains__(self, id)->bool:
        return id in self.items
    def __iter__(self)->Iterator[Detail]:
        return iter(self.items.values())
    def find_by_category(self,category : str) -> list[Detail]:
        results = [] 
        category = category.casefold()
        for detail in self:
            if category == detail.category.casefold():
                results.append(detail)
        return results 
    def find_by_name(self,name :str) -> list[Detail]:
        results = [] 
        name = name.casefold()
        for detail in self:
            if name in detail.name.casefold():
                results.append(detail)
        return results 
    def replace_with(self, other: "Catalog")->None:
        self.items = other.items.copy()
        

            
        

            

    

