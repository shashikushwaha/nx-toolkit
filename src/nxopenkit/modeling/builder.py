import NXOpen
from typing import List
from .base_builder import BaseBuilder

class Builder(BaseBuilder):
    def __init__(self):
        super().__init__()

    
    def commit(self) -> List[NXOpen.NXObject]:
        should_destroy = True
        try:
            self.builder.Commit()
            committed_objects: List[NXOpen.NXObject] = self.builder.GetCommittedObjects()
            if not committed_objects:
                raise ValueError("Non-associative NX Object not found")
            return committed_objects
        except NXOpen.NXException as error:
            self.undo_mark()
            should_destroy = False
            raise ValueError(error.Message) from error
        finally:
            if should_destroy:
                self.destroy()
