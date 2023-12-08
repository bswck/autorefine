from abc import ABCMeta


class Tool:
    pass


class Auditor(Tool, metaclass=ABCMeta):
    pass


class Linter(Tool, metaclass=ABCMeta):
    pass


class ChangeLogger(Tool, metaclass=ABCMeta):
    pass


class VersionControlSystem(Tool, metaclass=ABCMeta):
    pass


class FixViewer(Tool, metaclass=ABCMeta):
    pass


class Deployer(Tool, metaclass=ABCMeta):
    pass


class TypeChecker(Tool, metaclass=ABCMeta):
    pass
