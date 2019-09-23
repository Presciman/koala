"""
This module defines the quantum register based on PEPS.
"""

import numpy as np

from ..quantum_register import QuantumRegister
from ..backends import get_backend
from ..gates import tensorize
from .peps import PEPS


class PEPSQuantumRegister(QuantumRegister):
    def __init__(self, nrow, ncol, backend):
        self.backend = get_backend(backend)
        self.state = PEPS.zeros_state(nrow, ncol, self.backend)

    @property
    def nqubit(self):
        return self.state.nrow * self.state.ncol

    def apply_gate(self, gate):
        tensor = tensorize(self.backend, gate.name, *gate.parameters)
        postitons = [divmod(qubit, self.state.ncol) for qubit in gate.qubits]
        self.state.apply_operator(tensor, postitons)

    def apply_circuit(self, circuit):
        for gate in circuit.gates:
            self.apply_gate(gate)

    def amplitude(self, bits):
        if len(bits) != self.nqubit:
            raise ValueError('bits number and qubits number do not match')
        bits = np.array(bits).reshape(*self.state.shape)
        return self.state.get_amplitude(bits)

    def probability(self, bits):
        return np.abs(self.amplitude(bits))**2

    def peak(self, qubits, nsamples):
        self.state.peak(qubtis, nsamples)