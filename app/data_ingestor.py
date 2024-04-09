"""
Contains a class for parsing the data from a csv file.
"""

import copy
import csv

class DataIngestor:
    """
    Parser for a csv file.
    """

    def __init__(self, csv_path):

        self._entries = []
        self._read_entries_from_file(csv_path)

    def get_entries(self):
        """
        Returns a list of all the entries read by the ingestor. 
        """
        # This is how it should be, but the dude on the forum told me otherwise, so fuck it.
        # return copy.deepcopy(self._entries)  # The list should be mutated as pleased.
        return self._entries

    def _read_entries_from_file(self, csv_path: str) -> None:
        with open(csv_path, 'r', encoding="utf-8") as f:
            dict_reader = csv.DictReader(f)
            self._entries.extend(list(dict_reader))
