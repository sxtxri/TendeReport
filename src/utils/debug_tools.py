import os.path


def get_module_name(path: str) -> str:
    file_name = os.path.basename(path)

    file_name_without_ext, _ = os.path.splitext(file_name)

    return file_name_without_ext
