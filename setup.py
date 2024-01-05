import os
import shutil
import distutils.extension
import distutils.core


env_path = 'BLENDER_USER_ADDON_PATH'

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

addon_path = os.environ.get(env_path, None)

if addon_path:

    if addon_path[:-1] == '/':
        addon_path = addon_path[:-1]

    if not addon_path.endswith(os.path.join('scripts', 'addons')):
        raise BaseException('Incorrect addons path')

    molecular_path = os.path.join(addon_path, 'molecular')

    if not os.path.exists(molecular_path):
        os.makedirs(molecular_path)

    core_name = 'core.cp310-win_amd64.pyd'
    core_path = molecular_path + os.sep + core_name
    shutil.copyfile(
        'build\\lib.win-amd64-3.10\\'+core_name,
        core_path
    )
    print('\n\n\tCore installed into:\n\n\t\t{}\n\n'.format(core_path))

else:
    print('\n' * 4)
    print('\tWarning:\n\n')
    print('\t\tMolecular core is not installed in Blender addons.')
    print('\t\tAdd an {} environment variable.'.format(env_path))
    example_addon_path = 'C:\\Users\\Admin\\AppData\\Roaming\\Blender Foundation\\Blender\\2.90\\scripts\\addons\\'
    print('\t\tFor example:')
    print('\t\t\t{}'.format(example_addon_path))
    print('\t\tOr copy the Molecular core file manually.')
    print('\n' * 4)
