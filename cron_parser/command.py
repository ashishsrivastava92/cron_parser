
class Command:
    """
    Creates a command object, passed in the cli input string
    """
    def __init__(self, command):
        self.command = command

    @staticmethod
    def validate_command():
        pass