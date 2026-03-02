from datetime import datetime
#from zoneinfo import ZoneInfo

class Task:
    def __init__(self, name: str, priority = False, created_at=None): 
        self.name = name          # name of the task
        self.priority = priority  # priority of he task, True : high, False : low
        self.created_at = created_at or datetime.now()  # Task creation time


    def to_dict(self):
        """Converts the Task object to dictionary for storing in json"""  
        data = {}

        for key, value in self.__dict__.items():  
            if isinstance(value, datetime):
                data[key] = value.isoformat()  # searches for datetime object and converts it to string
            else:
                data[key] = value

        return data

    @classmethod
    def from_dict(cls, dictionary):
        data = dictionary.copy()

        if "created_at" in data:   
            data["created_at"] = datetime.fromisoformat(data["created_at"])  # Searches for the datetime string and converts it into datetime object

        return cls(**data)  # Creates an object with the attributes contained in the data dictionary and returns



    

    