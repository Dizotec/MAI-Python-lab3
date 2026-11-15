from src.catalog import Catalog 
class CatalogTransaction():
    def __init__(self,catalog:Catalog):
        self.catalog = catalog
        self.snapshot = Catalog()
    def __enter__(self):
        self.snapshot.replace_with(self.catalog)
        return self.catalog
    def __exit__(self,exc_type,exc_value,traceback):
        if exc_type is not None:
            self.catalog.replace_with(self.snapshot)
        
        return False 

