import NXOpen
from typing import List

class TaggedObject:
    def __init__(self, tagged_object: NXOpen.TaggedObject):
        self.session = NXOpen.Session.GetSession()
        self.workPart = self.session.Parts.Work 
        self.tagged_object = tagged_object

    # def __eq__(self, other):
    #     if other is None:
    #         return False        
    #     if not hasattr(other, "tag"):
    #         return NotImplemented
    #     return self.tag == other.tag

    def __eq__(self, other):
        def get_tag(obj):
            return getattr(obj, "tag", getattr(obj, "Tag", None))        
        other_tag = get_tag(other)
        if other_tag is None:
            return NotImplemented
        return get_tag(self) == other_tag

    def __hash__(self):
        return hash(getattr(self, "tag", getattr(self, "Tag")))

    
    @property
    def to_nx(self) -> NXOpen.TaggedObject:
        return self.tagged_object

    @property
    def tag(self):
        return self.tagged_object.Tag

    @staticmethod
    def to_nx_all(objs : List["TaggedObject"]):
        return[obj.to_nx for obj in objs]
    