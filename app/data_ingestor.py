import copy
import csv

class DataIngestor:
    def __init__(self, csv_path: str):

        self._entries: list[dict] = []
        self._read_entries_from_file(csv_path)

    def get_entries(self) -> list[dict[str, str]]:
        """
        Returns a list of all the entries read by the ingestor. 
        """
        return copy.deepcopy(self._entries)  # The list should be mutated as pleased.

    def _read_entries_from_file(self, csv_path: str) -> None:
        with open(csv_path, 'r') as f:
            dict_reader = csv.DictReader(f)
            self._entries.extend(list(dict_reader))
