from random import choices, choice
from game.generators import BaseFileGenerator
import pathlib


class CurveRoller(BaseFileGenerator):
    def __init__(self, file_name, autocast=str):
        """A PRNG that rolls based on a pre-compiled table.
        """
        super(CurveRoller, self).__init__(file_name)
        self.random_values = list(self.data_file.keys())
        self.value_weights = list(self.data_file.values())
        del self.data_file

        self.autocast = autocast

    def __next__(self):
        return self.autocast(choices(self.random_values, self.value_weights, k=1)[0])


class RandomEntryRoller(BaseFileGenerator):
    def __init__(self, file_name, header_row=True):
        """A PRNG that returns a random entry from a data file.
            The roller expects the data file to be a list at the top level.

            :param header_row: boolean header_row flag. Default=True. For csv files.
        """
        super(RandomEntryRoller, self).__init__(file_name, header_row=header_row)
        fk = pathlib.Path(file_name)
        self.is_csv = fk.suffix == '.csv'

    def __next__(self):
        return choice(self.data_file)
