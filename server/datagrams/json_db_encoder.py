##
## File:    json_db_encoder.py
##
## Author:  Schuyler Martin <sam8050@rit.edu>
##
## Description: Python class that defines a basic JSON encoder to use when
##              storing Python data and objects. Objects serialize into their
##              dictionary attributes.
##

import json

# identifier used to check type of encoded object
TYPE_ID = "__type__"

class JSON_DB_Encoder(json.JSONEncoder):
    '''
    Extension of the JSON Encoder
    '''

    def default(self, obj):
        '''
        Override default JSON encoding function
        :param: obj Object to serialize
        :return: Serializable data type
        '''
        value = None
        # if we see a non-user defined class, use the default
        try:
            value = super().default(obj)
        # otherwise, serialize the dictionary of attributes
        # I tried finding a way to detect a "generic" class type or a user
        # defined class in Python3 but that proved to be to difficult
        except TypeError:
            value = {}
            # copy the dicionary values over so we can append type information
            value[TYPE_ID] = str(type(obj))
            for key, val in obj.__dict__.items():
                value[key] = val
        return value

    @staticmethod
    def dumps(obj):
        '''
        Static method that wraps the object to JSON string encoding process
        :param: obj Object to encode
        :return: JSON string encoded object
        '''
        return json.dumps(obj, cls=JSON_DB_Encoder)

#### MAIN       ####

def main():
    '''
    Test program for this class
    '''
    stu0 = Student("stu1234", "pass", "Student", "A")
    tut0 = Tutor("aic4242", "pass", "Alice", "in Chains", "SLI")
    print(stu0)
    print("------------------------------------------------------------------")
    print(JSON_DB_Encoder.dumps(stu0))
    print()
    print(tut0)
    print("------------------------------------------------------------------")
    print(JSON_DB_Encoder.dumps(tut0))

if __name__ == "__main__":
    # package only used for testing purposes
    from users.student import Student
    from users.tutor import Tutor
    main()
