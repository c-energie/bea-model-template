"""Your existing modelling code: the physics, as a plain function, with no BEA imports.

This stands in for the code your team already has. It is kept as it is - not rewritten for BEA,
not importing it - and the model class in ``model.py`` calls it. Replace this function with yours
(or import yours from wherever it lives), and keep BEA out of it.

The function has to broadcast over numpy arrays: a sampler evaluates many parameter sets at once.
If yours takes scalars only, wrap it with ``numpy.vectorize`` in ``model.py`` rather than change it.
"""


def heat_loss_power(htc, temp_int, temp_ext, offset):
    """Steady-state heating power, ``power = htc * (temp_int - temp_ext) + offset``.

    ``htc`` in W/K, the temperatures in degC, ``offset`` and the result in W.
    """
    return htc * (temp_int - temp_ext) + offset
