import unittest

import numpy as np
from tensorbackends.utils import test_with_backend

from koala import Observable, statevector, Gate


@test_with_backend()
class TestStateVector(unittest.TestCase):
    def test_norm(self, backend):
        qstate = statevector.computational_zeros(6, backend=backend)
        qstate.apply_circuit([
            Gate('X', [], [0]),
            Gate('H', [], [1]),
            Gate('CX', [], [0,3]),
            Gate('CX', [], [1,4]),
            Gate('S', [], [1]),
        ])
        self.assertTrue(backend.isclose(qstate.norm(), 1))
        qstate *= 2
        self.assertTrue(backend.isclose(qstate.norm(), 2))
        qstate /= 2j
        self.assertTrue(backend.isclose(qstate.norm(), 1))

    def test_amplitude(self, backend):
        qstate = statevector.computational_zeros(6, backend=backend)
        qstate.apply_circuit([
            Gate('X', [], [0]),
            Gate('H', [], [1]),
            Gate('CX', [], [0,3]),
            Gate('CX', [], [1,4]),
            Gate('S', [], [1]),
        ])
        self.assertTrue(backend.isclose(qstate.amplitude([1,0,0,1,0,0]), 1/np.sqrt(2)))
        self.assertTrue(backend.isclose(qstate.amplitude([1,1,0,1,1,0]), 1j/np.sqrt(2)))

    def test_probablity(self, backend):
        qstate = statevector.computational_zeros(6, backend=backend)
        qstate.apply_circuit([
            Gate('X', [], [0]),
            Gate('H', [], [1]),
            Gate('CX', [], [0,3]),
            Gate('CX', [], [1,4]),
            Gate('S', [], [1]),
        ])
        self.assertTrue(backend.isclose(qstate.probability([1,0,0,1,0,0]), 1/2))
        self.assertTrue(backend.isclose(qstate.probability([1,1,0,1,1,0]), 1/2))

    def test_expectation(self, backend):
        qstate = statevector.computational_zeros(6, backend=backend)
        qstate.apply_circuit([
            Gate('X', [], [0]),
            Gate('CX', [], [0,3]),
            Gate('H', [], [2]),
        ])
        observable = 1.5 * Observable.sum([
            Observable.Z(0) * 2,
            Observable.Z(1),
            Observable.Z(2) * 2,
            Observable.Z(3),
        ])
        self.assertTrue(backend.isclose(qstate.expectation(observable), -3))

    def test_add(self, backend):
        psi = statevector.computational_zeros(6, backend=backend)
        phi = statevector.computational_ones(6, backend=backend)
        self.assertTrue(backend.isclose((psi + phi).norm(), np.sqrt(2)))

    def test_inner(self, backend):
        psi = statevector.computational_zeros(6, backend=backend)
        psi.apply_circuit([
            Gate('H', [], [0]),
            Gate('CX', [], [0,3]),
            Gate('H', [], [3]),
        ])
        phi = statevector.computational_zeros(6, backend=backend)
        self.assertTrue(backend.isclose(psi.inner(phi), 0.5))
