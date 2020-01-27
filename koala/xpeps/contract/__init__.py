"""
This module wraps the PEPS contraction routines from https://github.com/HaoTy/PEPS
"""

import numpy as np

from . import peps


def to_statevector(grid):
    peps_obj = _create_peps(grid)
    result = peps_obj.contract().reshape(*[2]*grid.shape[0]*grid.shape[1])
    result = grid.backend.transpose(result, [i+j*grid.shape[0] for i, j in np.ndindex(*grid.shape)])
    return result

def to_value(grid):
    peps_obj = _create_scalar_peps(grid)
    return peps_obj.contract()

def inner(this, that):
    this = _create_peps(this)
    that = _create_peps(that)
    return this.inner(that).contract()


def create_env_cache(grid):
    peps_obj = _create_peps(grid).norm()
    _up, _down = {}, {}
    for i in range(peps_obj.shape[0]):
        _up[i] = peps_obj[:i].contract_to_MPS() if i != 0 else None
        _down[i] = peps_obj[i+1:].contract_to_MPS() if i != grid.shape[0] - 1 else None
    return _up, _down

def inner_with_env(this, that, env, up_idx, down_idx):
    this = _create_peps(this)
    that = _create_peps(that)
    inner = this.inner(that)
    up, down = env[0][up_idx], env[1][down_idx]
    if up is None and down is None:
        peps_obj = inner
    elif up is None:
        peps_obj = inner.concatenate(down)
    elif down is None:
        peps_obj = up.concatenate(inner)
    else:
        peps_obj = up.concatenate(inner).concatenate(down)
    return peps_obj.contract()


def _create_peps(state):
    grid = np.empty_like(state.sites)
    for idx, tsr in np.ndenumerate(state.sites):
        grid[idx] = tsr.copy()
    for idx, w in np.ndenumerate(state.horizontal_bonds):
        grid[idx] = state.backend.einsum('ijklx,l->ijklx', grid[idx], w)
    for idx, w in np.ndenumerate(state.vertical_bonds):
        grid[idx] = state.backend.einsum('ijklx,k->ijklx', grid[idx], w)
    return peps.PEPS(grid, backend=state.backend)

def _create_scalar_peps(state):
    grid = np.empty_like(state.sites)
    for idx, tsr in np.ndenumerate(state.sites):
        grid[idx] = tsr.copy()
    for idx, w in np.ndenumerate(state.horizontal_bonds):
        grid[idx] = state.backend.einsum('ijkl,l->ijkl', grid[idx], w)
    for idx, w in np.ndenumerate(state.vertical_bonds):
        grid[idx] = state.backend.einsum('ijkl,k->ijkl', grid[idx], w)
    return peps.PEPS(grid, backend=state.backend)