import copy
import csv

class DataIngestor:
    def __init__(self, csv_path: str):

        self._entries: list[dict] = []

        self._questions_best_is_min: list[str] = [
            'Percent of adults aged 18 years and older who have an overweight classification',
            'Percent of adults aged 18 years and older who have obesity',
            'Percent of adults who engage in no leisure-time physical activity',
            'Percent of adults who report consuming fruit less than one time daily',
            'Percent of adults who report consuming vegetables less than one time daily'
        ]

        self._questions_best_is_max: list[str] = [
            'Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)',
            'Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic physical activity and engage in muscle-strengthening activities on 2 or more days a week',
            'Percent of adults who achieve at least 300 minutes a week of moderate-intensity aerobic physical activity or 150 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)',
            'Percent of adults who engage in muscle-strengthening activities on 2 or more days a week',
        ]

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
