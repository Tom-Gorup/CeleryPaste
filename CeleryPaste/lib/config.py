__author__ = 'pyt'

from CeleryPaste.celeryctl import logger
from CeleryPaste.core import CeleryPaste_ROOT
import os
import ConfigParser

class Dictionary(dict):
    """custom dict."""
    def __getattr__(self, key):
        return self.get(key, None)

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

class Config:
    def __init__(self, cfg=os.path.join(CeleryPaste_ROOT, "db.cfg")):
        config = ConfigParser.ConfigParser()
        config.read(cfg)

        for section in config.sections():
            setattr(self, section, Dictionary())
            for name, raw_value in config.items(section):
                try:
                    value = config.getboolean(section, name)
                except ValueError:
                    try:
                        value = config.getint(section, name)
                    except ValueError:
                        value = config.get(section, name)

                setattr(getattr(self, section), name, value)

    def get(self, section):
        """Get option.
        @param section: section to fetch.
        @return: option value.
        """
        try:
            return getattr(self, section)
        except AttributeError as e:
            logger.error("Option %s is not found in configuration, error: %s" % (section, e))

