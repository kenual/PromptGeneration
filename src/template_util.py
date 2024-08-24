import os
from typing import AnyStr

def get_template_path(cwd, templates_file_name: str) -> AnyStr:
    return os.path.abspath(os.path.join(cwd, "../templates", templates_file_name))
