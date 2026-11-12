class CatalogError(Exception):
    pass 
class InvalidDetailError(CatalogError):
    pass 
class DuplicateIdError(CatalogError):
    pass 
class ItemNotFoundError(CatalogError):
    pass 