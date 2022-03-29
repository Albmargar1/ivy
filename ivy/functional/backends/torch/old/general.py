"""
Collection of PyTorch general functions, wrapped to fit Ivy syntax and signature.
"""

# global
import ivy
import numpy as np
torch_scatter = None
import math as _math
import torch as torch
from operator import mul
from torch.types import Number
from functools import reduce as _reduce
from typing import List, Dict, Optional, Union


# local
from ivy.functional.ivy import default_dtype
from ivy.functional.ivy.device import default_device
from ivy.functional.backends.torch.device import dev_from_str, _callable_dev


# API #
# ----#



def dtype_bits(dtype_in):
    dtype_str = dtype_to_str(dtype_in)
    if 'bool' in dtype_str:
        return 1
    return int(dtype_str.replace('torch.', '').replace('uint', '').replace('int', '').replace('bfloat', '').replace(
        'float', ''))








def minimum(x, y):
    x_val = torch.tensor(x) if (isinstance(x, int) or isinstance(x, float)) else x
    y_val = torch.tensor(y) if (isinstance(y, int) or isinstance(y, float)) else y
    return torch.min(x_val, y_val)


def maximum(x, y):
    x_val = torch.tensor(x) if (isinstance(x, int) or isinstance(x, float)) else x
    y_val = torch.tensor(y) if (isinstance(y, int) or isinstance(y, float)) else y
    return torch.max(x_val, y_val)


def cast(x, dtype_in: str):
    dtype_val = dtype_from_str(dtype_in)
    return x.type(dtype_val)


astype = cast
















# noinspection PyShadowingNames
def identity(n: int, dtype: ivy.Dtype = 'float32', batch_shape: Optional[List[int]] = None,
             dev: Optional[str] = None):
    dev = default_device(dev)
    type_dict: Dict[str, torch.dtype] = {'int8': torch.int8,
            'int16': torch.int16,
            'int32': torch.int32,
            'int64': torch.int64,
            'uint8': torch.uint8,
            'bfloat16': torch.bfloat16,
            'float16': torch.float16,
            'float32': torch.float32,
            'float64': torch.float64,
            'bool': torch.bool}
    dtype_val: torch.dtype = type_dict[dtype]
    mat = torch.eye(n, n, dtype=dtype_val, device=dev_from_str(dev))
    if batch_shape is None:
        return mat
    else:
        reshape_dims = [1] * len(batch_shape) + [n, n]
        tile_dims = list(batch_shape) + [1, 1]
        res = torch.reshape(mat, reshape_dims).repeat(tile_dims)
        return res






def dtype(x, as_str=False):
    dt = x.dtype
    if as_str:
        return dtype_to_str(dt)
    return dt


def dtype_to_str(dtype_in):
    if isinstance(dtype_in, str):
        return dtype_in
    return {torch.int8: 'int8',
            torch.int16: 'int16',
            torch.int32: 'int32',
            torch.int64: 'int64',
            torch.uint8: 'uint8',
            torch.bfloat16: 'bfloat16',
            torch.float16: 'float16',
            torch.float32: 'float32',
            torch.float64: 'float64',
            torch.bool: 'bool'}[dtype_in]


def dtype_from_str(dtype_in: str) -> torch.dtype:
    if not isinstance(dtype_in, str):
        return dtype_in
    return {'int8': torch.int8,
            'int16': torch.int16,
            'int32': torch.int32,
            'int64': torch.int64,
            'uint8': torch.uint8,
            'bfloat16': torch.bfloat16,
            'float16': torch.float16,
            'float32': torch.float32,
            'float64': torch.float64,
            'bool': torch.bool}[dtype_in]


def compile(fn, dynamic=True, example_inputs=None, static_argnums=None, static_argnames=None):
    if dynamic:
        return torch.jit.script(fn)
    return torch.jit.trace(fn, example_inputs)


def current_framework_str():
    return 'torch'




