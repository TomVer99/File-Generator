import modules.generator_logging as GL
import modules.parser as P

import os

if __name__ == '__main__':

    this_folder = os.getcwd()
    module_folder = os.path.join(this_folder, 'modules')

# +----------------------------------------------------------------------+
# |                                                                      |
# |                           Validation phase                           |
# |                                                                      |
# +----------------------------------------------------------------------+

# +------------------------------------------------+
# |             scan for settings file             |
# +------------------------------------------------+

    settings_file = P.scan_for_settings_file(module_folder)

    if not settings_file:
        GL.log_error('(valid) gen.settings.xml not found')
        exit(1)
    else:
        GL.log_success('valid gen.settings.xml found')

# +------------------------------------------------+
# |             scan for source files              |
# +------------------------------------------------+

    source_files = P.scan_for_source_files(this_folder)

    if len(source_files) == 0:
        GL.log_error('no source files found')
        exit(1)

# +------------------------------------------------+
# |             validate source files              |
# +------------------------------------------------+

    valid_files = []
    files_type = []

    for index, file in enumerate(source_files):
        GL.log_notify('Found source file: ' + file)
        result = P.parse_source_file(this_folder, file)
        if result[0]:
            GL.log_success('Source file is valid')
            valid_files.append(file)
            files_type.append(result[1])
        else:
            GL.log_error('Source file is invalid: ' + result[1])

    if len(valid_files) == 0:
        GL.log_error('no valid source files found')
        exit(1)

# +----------------------------------------------------------------------+
# |                                                                      |
# |                           Generation phase                           |
# |                                                                      |
# +----------------------------------------------------------------------+


