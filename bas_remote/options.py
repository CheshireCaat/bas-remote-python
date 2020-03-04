from dataclasses import dataclass
from os.path import abspath, join
from os import getcwd


@dataclass
class Options:
    """Class that contains client settings.

    Attributes:
        working_dir (str):
            Location of the selected working folder.
        script_name (str):
            Name of the selected private script.
        password (str):
            Password from a user account with access to the script.
        login (str):
            Login from a user account with access to the script.
    """

    working_dir: str = join(getcwd(), 'data')

    script_name: str = ''

    password: str = ''

    login: str = ''

    def __post_init__(self):
        if not self.working_dir:
            raise ValueError("Field 'workingDir' must be specified")
        if not self.script_name:
            raise ValueError("Field 'scriptName' must be specified")
        self.working_dir = abspath(self.working_dir)


__all__ = ['Options']
