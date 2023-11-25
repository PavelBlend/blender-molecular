import os, shutil


env_path = 'BLENDER_USER_ADDON_PATH'
addon_folder = 'blender\\'


def install_addon():
    addon_path = os.environ.get(env_path, None)
    if addon_path:
        if addon_path[:-1] == '/':
            addon_path = addon_path[:-1]
        if not addon_path.endswith(os.path.join('scripts', 'addons')):
            raise BaseException('Incorrect addons path')
        molecular_path = os.path.join(addon_path, 'molecular')
        if not os.path.exists(molecular_path):
            os.makedirs(molecular_path)
        for file in os.listdir(molecular_path):
            module_name, extension = os.path.splitext(file)
            extension = extension.lower()
            if extension == '.py':
                os.remove(os.path.join(molecular_path, file))
        for file in os.listdir(addon_folder):
            if file == 'setup.py':
                continue
            module_name, extension = os.path.splitext(file)
            extension = extension.lower()
            if extension == '.py':
                shutil.copyfile(
                    os.path.join(addon_folder, file),
                    os.path.join(molecular_path, file)
                )
        print('\n\n\tAddon installed into:\n\n\t\t{}\n\n'.format(molecular_path))

    else:
        print('\n' * 4)
        print('\tWarning:\n\n')
        print('\t\tMolecular addon is not installed in Blender addons.')
        print('\t\tAdd an {} environment variable.'.format(env_path))
        example_addon_path = 'C:\\Users\\Admin\\AppData\\Roaming\\Blender Foundation\\Blender\\2.90\\scripts\\addons\\'
        print('\t\tFor example:')
        print('\t\t\t{}'.format(example_addon_path))
        print('\t\tOr copy the Molecular addon files manually.')
        print('\n' * 4)


install_addon()
input('Press Enter...')
