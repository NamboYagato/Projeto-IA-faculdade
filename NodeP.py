from Node import Node

class NodeP(Node):
    def __init__(self, pai=None, estado=None, v1=None,
                 anterior=None, proximo=None, v2=None):
        super().__init__(pai, estado, v1, anterior, proximo)
        self.v2 = v2
