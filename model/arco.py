from dataclasses import dataclass
from model.Constructor import Constructor

@dataclass
class Arco:
    u : Constructor
    v : Constructor
    peso : int
