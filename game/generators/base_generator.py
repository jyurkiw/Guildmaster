import csv
import yaml
import os
import pathlib


def load_dat(file_path: pathlib.Path, header_row: bool = False):
    """
    Load a file at file_path. This file must be either a csv or yaml file with the appropriate extension.

    :param file_path: The path to the data file. Can be either absolute or relative.
    :param header_row: Header row flag for csv files.
    :return: The data in the file as a python list (for csv files) or the yaml representation.
    """
    check_path = os.path.abspath(os.path.expanduser(str(file_path)))
    if not os.path.exists(check_path):
        raise FileExistsError(file_path)
    if not os.path.isfile(check_path):
        raise FileNotFoundError(file_path)
    if file_path.suffix not in {".csv", ".yaml"}:
        raise Exception("Expected a csv or yaml file extension.")

    data = None

    if file_path.suffix == ".csv":
        with open(check_path, "r", encoding="utf-8-sig") as f:
            if header_row:
                reader = csv.DictReader(f)
            else:
                reader = csv.reader(f)
            data = [row for row in reader]

    elif file_path.suffix == ".yaml":
        with open(check_path, "r") as f:
            data = yaml.safe_load(f)

    return data


class BaseFileGenerator(object):
    """A base generator class that automatically loads file data so it can be accessed."""

    def __init__(self, file_path, **kwargs):
        """
        Base file generator.

        Calls load_dat on the passed file_path.

        :keyword Arguments:
            * *header_row* (``bool``)
            header row flag for csv files
        """
        self.data_file = load_dat(
            pathlib.Path(file_path), header_row=kwargs.get("header_row", False)
        )

    def __next__(self):
        raise Exception("__next__ must be overloaded in all generators.")
