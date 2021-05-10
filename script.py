from datetime import datetime
import json
from operator import itemgetter
from itertools import groupby


class DeserializerJSON:
    """Deserialize json to a Python object."""

    @staticmethod
    def read(filename):
        with open(filename, 'r') as fp:
            return json.load(fp)


class Parser:
    """Parsing and grouping obj by UserId."""

    @staticmethod
    def parse_obj(obj) -> tuple:
        obj.sort(key=itemgetter('userId'))
        for user_id, notes in groupby(obj, key=itemgetter('userId')):
            yield user_id, notes

    @staticmethod
    def validate_keys(notes) -> list:
        """
        Dictionary validation using existing keys
        """
        existing_keys = {'userId', 'id', 'title', 'completed'}
        user_id, note = notes
        validate_notes = [item for item in note if not existing_keys.symmetric_difference(item.keys())]
        validate_notes = [user_id, validate_notes]
        return validate_notes

    @staticmethod
    def grouping_by_complete(obj_with_validate_keys) -> list:
        completed_tasks = []
        uncompleted_tasks = []
        user_id, notes = obj_with_validate_keys
        for item in notes:
            if item['completed']:
                completed_tasks.append(item)
            uncompleted_tasks.append(item)
        object_to_report = [user_id, {'uncompleted_tasks': uncompleted_tasks,
                                      'completed_tasks': completed_tasks}]
        return object_to_report


class Report:
    @staticmethod
    def report_maker(obj) -> None:
        user_id, notes = obj
        completed_tasks = [item['title'] for item in notes['completed_tasks'][0:50]]
        uncompleted_tasks = [item['title'] for item in notes['uncompleted_tasks'][0:50]]
        completed_tasks = '\n'.join(completed_tasks)
        uncompleted_tasks = '\n'.join(uncompleted_tasks)
        format_name = f"{user_id}_{datetime.now().strftime('20%y-%m-%d')}T{datetime.now().strftime('%H-%M')}.txt"
        with open(format_name, 'w') as fp:
            fp.write(f"Employer №{user_id}\n"
                     f"{datetime.now().strftime('20%y-%m-%d')}T{datetime.now().strftime('%H-%M')}\n"
                     f"Not completed:\n"
                     f" {uncompleted_tasks}\n")
            fp.write(f"Completed:\n {completed_tasks}\n")


def main():
    employees = 'employees.json'
    des_json = DeserializerJSON()
    data = des_json.read(employees)
    parser_ = Parser.parse_obj(data)
    for item in parser_:
        validate_item = Parser.validate_keys(item)
        to_report = Parser.grouping_by_complete(validate_item)
        Report.report_maker(to_report)


if __name__ == '__main__':
    main()
