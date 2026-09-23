import NXOpen


class TaggedObject:
    def __init__(self, tagged_object: NXOpen.TaggedObject):
        self.tagged_object = tagged_object

    @property
    def nx_object(self) -> NXOpen.TaggedObject:
        return self.tagged_object

    @property
    def tag(self):
        return self.tagged_object.Tag