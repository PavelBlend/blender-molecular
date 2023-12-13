Blender Molecular
========================

This is molecular addon for `blender`. Inspired from the 2d simulator `Really` (1998) and `Lagoa Multiphysic` in `Softimage`.

Based on `Molecular Script` from [Pyroevil](https://github.com/Pyroevil/Blender-Molecular-Script).

The core has been rewritten from `Cython` to `C`.

### Build C Core:
Install `OpenMP`.

Run: ```python setup.py build```

### Install Addon:
Add an `BLENDER_USER_ADDON_PATH` environment variable that will reference the blender addons directory.

Run: ```python install.py```
