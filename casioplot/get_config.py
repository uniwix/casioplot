import os
import tomllib
from typing import Any

THIS_DIR = os.path.abspath(os.path.dirname(__file__))


def _get_config_file(file_name: str) -> tuple[dict[str, Any] | str, str]:
    """Get the configuration file.

    This function searches for the configuration file in the following order:
    1. Absolute path.
    2. The current directory.
    3. The `~/.config/casioplot` directory.
    4. Environment variable `CASIOPLOT_CONF`.
    5. The directory of the package (default configuration files).
    6. The default configuration file.

    :param file_name: The name of the configuration file.
    :return: The configuration file path.
    """
    locations = (
        "",
        os.curdir,
        os.path.expanduser("~/.config/casioplot"),
        os.environ.get("CASIOPLOT_CONF"),
        THIS_DIR
    )
    for loc in locations:
        try:
            path = os.path.join(loc, file_name)
            with open(path, "rb") as source:
                return tomllib.load(source), os.path.dirname(path)
        except (IOError, TypeError):
            pass
    print(f"[Error] Config file {file_name} not found. Using default configuration.")
    with open(os.path.join(os.path.dirname(__file__), "default.toml"), "rb") as source:
        return tomllib.load(source), os.path.dirname(__file__)
