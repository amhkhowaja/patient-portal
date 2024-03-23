"""Doctor module for Doctor model"""
class Doctor:
    """
    Doctor Model in the patients portal system.
    """

    def __init__(self, name):
        """
        Initializes a new instance of the Doctor class.

        Args:
            name (str): The name of the doctor.
        """
        self._name = name

    def get_name(self):
        """
        Returns the name of the doctor.

        Returns:
            str: The name of the doctor.
        """
        return self._name

    def set_name(self, name):
        """
        Sets the name of the doctor.

        Args:
            name (str): The name of the doctor.
        """
        self._name = name
