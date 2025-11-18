class Node(object):
    def __init__(self, pai=None, estado=None, v1=None,
                 anterior=None,  proximo=None):
        self.pai       = pai
        self.estado    = estado
        self.v1        = v1
        self.anterior  = anterior
        self.proximo   = proximo

