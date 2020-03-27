import numpy as np
import tensorbackends

from .statevector import StateVector


def computational_zeros(nsite, *, backend='numpy'):
    backend = tensorbackends.get(backend)
    tensor = backend.zeros((2,)*nsite, dtype=complex)
    tensor[(0,)*nsite] = 1
    return StateVector(tensor, backend)


def computational_ones(nsite, *, backend='numpy'):
    backend = tensorbackends.get(backend)
    tensor = backend.zeros((2,)*nsite, dtype=complex)
    tensor[(1,)*nsite] = 1
    return StateVector(tensor, backend)


def computational_basis(nsite, bits, *, backend='numpy'):
    backend = tensorbackends.get(backend)
    bits = np.asarray(bits).reshape(nsite)
    tensor = backend.zeros((2,)*nsite, dtype=complex)
    tensor[tuple(bits)] = 1
    return StateVector(tensor, backend)

def random(nsite, *, backend='numpy'):
    backend = tensorbackends.get(backend)
    shape = (2,)*nsite
    tensor = backend.random.uniform(-1,1,shape) + 1j * backend.random.uniform(-1,1,shape)
    tensor /= backend.norm(tensor)
    return StateVector(tensor, backend)
