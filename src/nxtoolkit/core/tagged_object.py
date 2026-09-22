import NXOpen


class TaggedObject:
    def __init__(self, nxOpenTaggedObject: NXOpen.TaggedObject):
        self.nxOpenTaggedObject = nxOpenTaggedObject

    @property
    def nx_object(self) -> NXOpen.NXObject:
        """Return the wrapped Siemens NX object."""
        return self.nxOpenTaggedObject

    @property
    def Tag(self):
        return self.nxOpenTaggedObject.Tag