from functools import wraps
import logging
import NXOpen


def builder_operation(func):

    @wraps(func)
    def wrapper(self, *args, **kwargs):

        try:
            return func(self, *args, **kwargs)

        except NXOpen.NXException:

            logger = logging.getLogger(self.__class__.__module__)

            logger.exception("%s.%s failed", self.__class__.__name__, func.__name__, )
            destroy = getattr(self, "destroy", None)
            if callable(destroy):
                destroy()

            raise
        
    return wrapper