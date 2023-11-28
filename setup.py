import os
import shutil
import distutils


if os.path.exists('build'):
    shutil.rmtree('build')

module = distutils.extension.Extension(
    'core',
    sources=['core\\main.c'],
    extra_compile_args=['/Ox', '/openmp', '/GT', '/fp:fast']
)

distutils.core.setup(
    name='Molecular Core',
    version='1.0',
    description='This is a core for molecular addon',
    ext_modules=[module]
)
shutil.copyfile(
    'build\\lib.win-amd64-cpython-310\\core.cp310-win_amd64.pyd',
    'C:\\Users\\Pavel\\AppData\\Roaming\\Blender Foundation\\Blender\\3.4\\scripts\\addons\\molecular\\core.cp310-win_amd64.pyd'
)
