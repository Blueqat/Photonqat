
import numpy as np
from .bosonicLadder import *
from .gateOps import *

class GATE():
    def __init__(self, obj):
        self.obj = obj

class Dgate(GATE):
    def __init__(self, obj, mode, alpha):
        self.obj = obj
        self.cutoff = self.obj.cutoff
        self.N = self.obj.N
        self.mode = mode
        self.alpha = alpha
        super().__init__(obj)

    def run(self, state):
        self.alpha = _paramCheck(self.alpha)
        return Displacement(state, self.mode, self.alpha, self.N, self.cutoff)

class BSgate(GATE):
    def __init__(self, obj, mode1, mode2, theta = np.pi / 4):
        self.obj = obj
        self.cutoff = self.obj.cutoff
        self.N = self.obj.N
        self.mode1 = mode1
        self.mode2 = mode2
        self.theta = theta
        super().__init__(obj)

    def run(self, state):
        self.theta = _paramCheck(self.theta)
        return Beamsplitter(state, self.mode1, self.mode2, self.theta, self.N, self.cutoff)

class Sgate(GATE):
    def __init__(self, obj, mode, r, phi = 0):
        self.obj = obj
        self.cutoff = self.obj.cutoff
        self.N = self.obj.N
        self.mode = mode
        self.r = r
        self.phi = phi
        super().__init__(obj)

    def run(self, state):
        self.r = _paramCheck(self.r)
        self.phi = _paramCheck(self.phi)
        return Squeeze(state, self.mode, self.r, self.phi, self.N, self.cutoff)

class Kgate(GATE):
    def __init__(self, obj, mode, chi):
        self.obj = obj
        self.cutoff = self.obj.cutoff
        self.N = self.obj.N
        self.mode = mode
        self.chi = chi
        super().__init__(obj)

    def run(self, state):
        self.chi = _paramCheck(self.chi)
        return KerrEffect(state, self.mode, self.chi, self.N, self.cutoff)

class MeasF(GATE):
    def __init__(self, obj, mode, post_select = None):
        self.obj = obj
        self.cutoff = self.obj.cutoff
        self.N = self.obj.N
        self.mode = mode
        self.post_select = post_select
        super().__init__(obj)

    def run(self, state):
        res, state = photonMeasurement(state, self.mode, self.post_select)
        self.obj.creg[self.mode][2] = res
        return state

def _paramCheck(param):
    if isinstance(param, CregReader):
        return param.read()
    else:
         return param

class CregReader():
    def __init__(self, reg, idx, var, scale):
        self.reg = reg
        self.idx = idx
        self.var = var
        self.scale = scale

    def read(self):
        if self.var == "x":
            v = 0
        elif self.var == "p":
            v = 1
        elif self.var == "n":
            v = 2
        else:
            raise ValueError('Creg keeps measurement results of "x" or "p".')
        return self.reg[self.idx][v] * self.scale