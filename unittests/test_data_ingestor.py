import unittest
from app import DataIngestor

class DataIngestorTest(unittest.TestCase):

    def setUp(self) -> None:
        self.data_ingestor = DataIngestor('./unittests/test_data.csv')
    
    def test_when_instantiated_then_data_is_read(self) -> None:
        read_entries = self.data_ingestor.get_entries()

        # Check the correct number of entries were read
        self.assertEqual(len(read_entries), 7)

        # Check that a specific entry has been read correctly
        specific_ohio_entry = filter(lambda entry: entry["LocationAbbr"] == "OH"
                           and entry["StratificationID1"] == "INC75PLUS"
                           and entry["YearStart"] == "2017",
                           read_entries)
        self.assertEqual(sum(1 for _ in specific_ohio_entry), 1)
