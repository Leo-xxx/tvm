"""namespace of IR node builder make function

This namespace is used for developers. While you do not see any declarations.
The functions are automatically exported from C++ side via PackedFunc.

Each api is a PackedFunc that can be called in a positional argument manner.
You can use make function to build the IR node.
"""
from __future__ import absolute_import as _abs
from ._ffi.function import _init_api
from ._ffi.runtime_ctypes import TVMType


def range_by_min_extent(min_value, extent):
    """Construct a Range by min and extent.

    This constructs a range in [min_value, min_value + extent)

    Parameters
    ----------
    min_value : Expr
        The minimum value of the range.

    extent : Expr
        The extent of the range.

    Returns
    -------
    rng : Range
        The constructed range.
    """
    return _range_by_min_extent(min_value, extent)


def static_cast(dtype, expr):
    """Cast expr to dtype.

    If expr is scalar and dtype is a corresponding vector
    type, a Broadcast is generated. Otherwise it is a Cast.

    Parameters
    ----------
    dtype : str
        The target data type.

    expr : Expr
        The expression to be casted.

    Returns
    -------
    casted : Expr
        The casted expression.
    """
    target_type = TVMType(dtype)
    src_type = TVMType(expr.dtype)
    if target_type.type_code == src_type.type_code and src_type.bits == target_type.bits:
        if src_type.lanes == target_type.lanes:
            return expr
        if src_type.lanes == 1 and target_type.lanes > 1:
            return Broadcast(expr, target_type.lanes)
    return Cast(dtype, expr)


def node(type_key, **kwargs):
    """Make a new DSL node by its type key and fields

    Parameters
    ----------
    type_key : str
        The type key of the node.

    **kwargs : dict
        The fields of the node.

    Returns
    -------
    node : Node
        The corresponding DSL Node

    Note
    ----
    If the created node is instance of AttrsNode, then
    the creator function will also run bound checks and
    default value setup as supported by Attrs.

    Example
    -------
    The following code constructs a IntImm object

    .. code-block:: python

       x = tvm.make.node("IntImm", dtype="int32", value=10)
       assert isinstance(x, tvm.expr.IntImm)
       assert x.value == 10
    """
    args = [type_key]
    for k, v in kwargs.items():
        args += [k, v]
    return _Node(*args)


_init_api("tvm.make")
