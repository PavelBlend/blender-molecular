Blender Molecular
========================

This is molecular addon for `Blender`.

Inspired from the 2D simulator `Really` (1998) and `Lagoa Multiphysic` in `Softimage`.

Based on `Molecular Script` from [Pyroevil](https://github.com/Pyroevil/Blender-Molecular-Script).

The core has been rewritten from `Cython` to `C`.

## Install

Add an `BLENDER_USER_ADDON_PATH` environment variable that will reference the blender addons directory.

Install `OpenMP`.

### Build C Core:

```python setup.py build```

### Install Addon:

```python install.py```
