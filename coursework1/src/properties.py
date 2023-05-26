from dataclasses import dataclass

@dataclass
class Config(object):
    def __init__(self, config):
        for key, value in config.items():
            setattr(self, key, value)
            