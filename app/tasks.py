from app import DataIngestor
from app.task_runner import Task


questions_best_is_min: list[str] = [
    'Percent of adults aged 18 years and older who have an overweight classification',
    'Percent of adults aged 18 years and older who have obesity',
    'Percent of adults who engage in no leisure-time physical activity',
    'Percent of adults who report consuming fruit less than one time daily',
    'Percent of adults who report consuming vegetables less than one time daily'
]

questions_best_is_max: list[str] = [
    'Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)',
    'Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic physical activity and engage in muscle-strengthening activities on 2 or more days a week',
    'Percent of adults who achieve at least 300 minutes a week of moderate-intensity aerobic physical activity or 150 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)',
    'Percent of adults who engage in muscle-strengthening activities on 2 or more days a week',
]


class BaseTask(Task):
    def __init__(self) -> None:
        super().__init__()

    def _compute_states_mean(self, data: list[dict], question: str) -> list[tuple[str, float]]:
        """
        Returns a list of tuples, consisting of the country's LocationDesc and its mean.
        """
        relevant_data = filter(lambda e: e["Question"] == question, data)

        # Maps LocationDesc to a tuple consisting of the sum of values and the number of values from all entries
        countries_scores_dict: dict[str, tuple[int, int]] = {}  

        for entry in relevant_data:
            location = entry["LocationDesc"]
            
            if entry["Data_Value"] == "" or entry["Data_Value"] is None:
                continue

            if location in countries_scores_dict:
                current_sum = countries_scores_dict[location][0]
                no_of_entries_for_location = countries_scores_dict[location][1]
                countries_scores_dict[location] = (current_sum + float(entry["Data_Value"]), no_of_entries_for_location+1)
            else:
                countries_scores_dict[location] = (float(entry["Data_Value"]), 1)

        # List of tuples consisting of LocationDesc and average data
        countries_averages = []

        for location, sum_no_tuple in countries_scores_dict.items():
            countries_averages.append((location, sum_no_tuple[0] / sum_no_tuple[1]))

        return countries_averages
    
    def _compute_state_mean(self, data: list[dict], question: str, state_location_desc: str) -> float:
        relevant_data = list(filter(lambda e: e["Question"] == question and e["LocationDesc"] == state_location_desc, data))

        no_of_entries = len(relevant_data)
        
        if no_of_entries == 0:
            return 0
        
        return sum(map(lambda e: float(e["Data_Value"]), relevant_data)) / no_of_entries
    
    def _compute_global_mean(self, data: list[dict], question: str) -> float:
        relevant_data = list(filter(lambda e: e["Question"] == question, data))
        no_of_entries = len(relevant_data)

        if no_of_entries == 0:
            return 0
        
        return sum(map(lambda e: float(e["Data_Value"]), relevant_data)) / no_of_entries

class Best5Task(BaseTask):
    def __init__(self, data_ingestor: DataIngestor, question: str) -> None:
        super().__init__()
        self._question = question
        self._data_ingestor = data_ingestor

    def run(self):
        all_data = self._data_ingestor.get_entries()
        countries_averages = self._compute_states_mean(all_data, self._question)
        should_reverse = self._question in questions_best_is_max
        countries_averages.sort(key=lambda e: e[1], reverse=should_reverse)

        final_result = {}
        for result in countries_averages[:5]:
            final_result[result[0]] = result[1]

        return final_result

class Worst5Task(BaseTask):
    def __init__(self, data_ingestor: DataIngestor, question: str) -> None:
        super().__init__()
        self._question = question
        self._data_ingestor = data_ingestor

    def run(self):
        all_data = self._data_ingestor.get_entries()
        countries_averages = self._compute_states_mean(all_data, self._question)
        should_reverse = self._question in questions_best_is_min
        countries_averages.sort(key=lambda e: e[1], reverse=should_reverse)

        final_result = {}
        for result in countries_averages[:5]:
            final_result[result[0]] = result[1]

        return final_result

class StatesMeanTask(BaseTask):
    def __init__(self, data_ingestor: DataIngestor, question: str) -> None:
        super().__init__()
        self._question = question
        self._data_ingestor = data_ingestor

    def run(self):
        all_data = self._data_ingestor.get_entries()
        countries_averages = self._compute_states_mean(all_data, self._question)

        #  Who writes an API where what should be values are keys??
        #  This should look like this instead: [{name: Romania, value: 10}], not like this: {Romania: 10}...
        final_result = {}
        for result in countries_averages:
            final_result[result[0]] = result[1]

        return final_result

class StateMeanTask(BaseTask):
    def __init__(self, data_ingestor: DataIngestor, question: str, state: str) -> None:
        super().__init__()
        self._question = question
        self._data_ingestor = data_ingestor
        self._state = state

    def run(self):
        all_data = self._data_ingestor.get_entries()
        return {
            self._state: self._compute_state_mean(all_data, self._question, self._state)
        }

class GlobalMeanTask(BaseTask):
    def __init__(self, data_ingestor: DataIngestor, question: str) -> None:
        super().__init__()
        self._question = question
        self._data_ingestor = data_ingestor

    def run(self):
        all_data = self._data_ingestor.get_entries()
        return {
            "global_mean": self._compute_global_mean(all_data, self._question)
        }

class DiffFromMeanTask(BaseTask):
    def __init__(self, data_ingestor: DataIngestor, question: str) -> None:
        super().__init__()
        self._question = question
        self._data_ingestor = data_ingestor

    def run(self):
        all_data = self._data_ingestor.get_entries()
        global_average = self._compute_global_mean(all_data, self._question)
        countries_averages = self._compute_states_mean(all_data, self._question)

        final_result = {}
        for result in countries_averages:
            final_result[result[0]] = global_average - result[1]

        return final_result
    
class StateDiffFromMeanTask(BaseTask):
    def __init__(self, data_ingestor: DataIngestor, question: str, state: str) -> None:
        super().__init__()
        self._question = question
        self._data_ingestor = data_ingestor
        self._state = state

    def run(self):
        all_data = self._data_ingestor.get_entries()
        global_average = self._compute_global_mean(all_data, self._question)
        state_average = self._compute_state_mean(all_data, self._question, self._state)

        return {
            self._state: global_average - state_average
        }
