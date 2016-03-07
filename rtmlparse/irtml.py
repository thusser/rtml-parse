from zope.interface import Interface, Attribute


class ITemplate(Interface):
    """
    Templates for easier RTML access.
    """
    def __init__(element):
        """
        Initialize the template.
        """

    name = Attribute("Name of template")
    type = Attribute("Class of base element")
