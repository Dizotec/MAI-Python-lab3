class CatalogError(Exception):
    pass 
class InvalidDetailError(CatalogError):
    pass 
class DuplicateIdError(CatalogError):
    pass 
class ItemNotFoundError(CatalogError):
    pass 
class UnsupportedFormatVersionError(CatalogError):
    pass 
class CorruptedFileError(CatalogError):
    pass 