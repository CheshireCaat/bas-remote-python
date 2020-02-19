from dataclasses import dataclass
from os import getcwd
from os import path


@dataclass
class Options:
    """Class that contains client settings.

    Attributes:
        workingDir (str): Location of the selected working folder.
        scriptName (str): Name of the selected private script.
        password (str): Password from a user account with access to the script.
        login (str): Login from a user account with access to the script.
    """

    workingDir: str = path.join(getcwd(), 'data')

    scriptName: str = ''

    password: str = ''

    login: str = ''

    def __post_init__(self):
        if not self.workingDir:
            msg = "Field 'workingDir' must be specified"
            raise ValueError(msg)
        if not self.scriptName:
            msg = "Field 'scriptName' must be specified"
            raise ValueError(msg)
