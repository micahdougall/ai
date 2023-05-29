from dataclasses import dataclass


@dataclass
class Config(object):
    """Class to store configuration constants at runtime"""
    def __init__(self, config):
        for key, value in config.items():
            setattr(self, key, value)
            