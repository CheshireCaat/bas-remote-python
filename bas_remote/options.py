from dataclasses import dataclass
from os import getcwd, path


@dataclass
class Options:
    """Class that contains client settings."""

    working_dir: str = path.join(getcwd(), 'data')
    """Location of the selected working folder."""

    script_name: str = ''
    """Name of the selected private script."""

    password: str = ''
    """Password from a user account with access to the script."""

    login: str = ''
    """Login from a user account with access to the script."""

    def __post_init__(self):
        if not self.working_dir:
            raise ValueError("Field 'working_dir' must be specified")
        if not self.script_name:
            raise ValueError("Field 'script_name' must be specified")
        self.working_dir = path.abspath(self.working_dir)


__all__ = ['Options']
