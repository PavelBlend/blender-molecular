import shutil
from distutils.core import setup
from distutils.extension import Extension


module = Extension(
    'core',
    sources=['core\\main.c'],
    extra_compile_args=['/Ox', '/openmp', '/GT', '/fp:fast']
)

setup(
    name='Molecular Core',
    version='1.0',
    description='This is a core for molecular addon',
    ext_modules=[module]
)
shutil.copyfile(
    'build\\lib.win-amd64-cpython-310\\core.cp310-win_amd64.pyd',
    'C:\\Users\\Pavel\\AppData\\Roaming\\Blender Foundation\\Blender\\3.4\\scripts\\addons\\molecular\\core.cp310-win_amd64.pyd'
)
