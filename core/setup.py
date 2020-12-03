import platform, os, shutil
from distutils.core import setup
from Cython.Distutils import build_ext, Extension
import Cython.Compiler.Options


INCLUDE = '#include '
INCLUDE_DIR = 'sources'
LIB_NAME = 'core'
CORE_PYX_FILE = 'core.pyx'
WHITE_SPACES = (' ', '\t')
core_file_name = 'main'
core_file_extension = 'pyx'
core_file_path = core_file_name + os.extsep + core_file_extension
cython_extension = 'pyx'
profiler = False
profiler_nogil = False
profiler_white_space_limit = 128
temp_files = ('core.pyx', )
env_path = 'BLENDER_USER_ADDON_PATH'


def install_core(root, file_name):
    addon_path = os.environ.get(env_path, None)
    if addon_path:
        if addon_path[:-1] == '/':
            addon_path = addon_path[:-1]
        if not addon_path.endswith(os.path.join('scripts', 'addons')):
            raise BaseException('Incorrect addons path')
        molecular_path = os.path.join(addon_path, 'molecular')
        if not os.path.exists(molecular_path):
            os.makedirs(molecular_path)
        input_core_path = os.path.join(root, file_name)
        output_core_file = os.path.join(molecular_path, file_name)
        shutil.copyfile(
            input_core_path,
            output_core_file
        )
        os.remove(input_core_path)
        print('\n\n\tMolecular Core installed into:\n\n\t\t{}\n\n'.format(output_core_file))
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


def remove_files():
    for root, dirs, files in os.walk('.'):
        for file in files:
            module_name, extension = os.path.splitext(file)
            extension = extension.lower()
            if not extension in ('.pyx', '.pyd', '.py', '.bat', '.md') or file in temp_files:
                src_file = os.path.join(root, file)
                os.remove(src_file)
            if extension == '.pyd':
                install_core(root, file)
    shutil.rmtree('build')


with open(core_file_path, 'r') as core_file:
    core_code = core_file.read()


def preprocessor(core_code):
    has_errors = False
    code = []
    use_profiler = False
    use_nogil = False
    is_nogil_function = False
    nogil_spaces_count = 0
    line_index = 0
    for line in core_code.splitlines():
        line_index += 1
        char_count = 0
        for char in line:
            if not char in WHITE_SPACES:
                char_count += 1
        if not char_count:
            continue
        space_count = 0
        for char in line:
            if char == ' ':
                space_count += 1
            else:
                break
        if "#PROFILER_START" in line:
            use_profiler = True
        elif "#PROFILER_END" in line:
            use_profiler = False
        if "#PROFILER_START_NOGIL" in line:
            use_profiler = True
            use_nogil = True
            is_nogil_function = True
            nogil_spaces_count = space_count
        elif "#PROFILER_END_NOGIL" in line:
            use_profiler = False
            use_nogil = False
            is_nogil_function = False
        if "with nogil:" in line and not is_nogil_function:
            use_nogil = True
            nogil_spaces_count = line.find('with nogil:')
        elif nogil_spaces_count == space_count:
            use_nogil = False
            nogil_spaces_count = 0
        elif "#PROFILER_END" in line:
            use_profiler = False
        if INCLUDE in line:
            white_spaces = line[0 : line.find(INCLUDE)]
            white_spaces_list = set(white_spaces)
            if len(white_spaces_list) > 2:
                print('! Error White Space')
                has_errors = True
            for white_space in white_spaces_list:
                if not white_space in WHITE_SPACES:
                    print('! Error Incorrect White Space')
                    has_errors = True
            if has_errors:
                continue
            module_name = line[line.find(INCLUDE) + len(INCLUDE) : ]
            module_path = INCLUDE_DIR + os.sep + module_name + os.extsep + cython_extension
            with open(module_path, 'r') as module_file:
                module_code = module_file.read()
                module_code = preprocessor(module_code)
                code.extend(module_code)
        else:
            if profiler and use_profiler:
                if not ('print' in line or 'printf' in line):
                    if (use_nogil or is_nogil_function):
                        print_code = 'printf("{} {}\\n")'.format('{:0>4}'.format(line_index), line)
                        if not profiler_nogil:
                            print_code = ''
                    else:
                        print_code = 'print("{1:0>4}: {0}")'
                    if space_count > profiler_white_space_limit:
                        print_code = ''
                    profiler_string = ' ' * space_count + print_code.format(line, line_index)
                    if not line[space_count : space_count + 4] in ('else', 'elif'):
                        if line[space_count : space_count + 1] != '#':
                            code.append(profiler_string)
            if line[space_count : space_count + 1] != '#' or '#cython:' in line:
                code.append(line)
    return code


code = preprocessor(core_code)
with open(CORE_PYX_FILE, 'w') as core_file:
    for line in code:
        core_file.write(line + '\n')

os_name = platform.architecture()[1]
Cython.Compiler.Options.annotate = True
source_dir = os.path.dirname(os.path.abspath(__file__))
addon_folder = os.path.join(os.path.dirname(source_dir), 'molecular')

if os_name == "WindowsPE":
    ext_module = Extension(
        LIB_NAME,
        [CORE_PYX_FILE, ],
        extra_compile_args=['/Ox','/openmp','/GT','/arch:SSE2','/fp:fast'],
        cython_directives={'language_level' : "3"}
    )
else:
    ext_module = Extension(
        LIB_NAME,
        [CORE_PYX_FILE, ],
        extra_compile_args=['-O3','-msse4.2','-ffast-math','-fno-builtin'],
        extra_link_args=['-lm'],
        cython_directives={'language_level' : "3"}
    )

try:
    setup(
        name='Molecular',
        cmdclass={'build_ext': build_ext},
        include_dirs=['.'],
        ext_modules=[ext_module, ]
    )
finally:
    remove_files()
