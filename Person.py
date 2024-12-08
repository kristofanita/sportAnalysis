class Person:
    measurements = list()

    def __int__(self, firstName, lastName, gender, dateOfBirth, height, weight, activityClass, maxHR, minHR):
        self.firstName = firstName
        self.lastName = lastName
        self.gender = gender
        self.dateOfBirth = dateOfBirth
        self.height = height
        self.weight = weight
        self.activityClass = activityClass
        self.maxHR = maxHR
        self.minHR = minHR
        self.measurements = list()

    def __init__(self):
        self.measurements = list()

    def print_person_info(self):
        print("firstName:", self.firstName, "lastName:", self.lastName, "gender:", self.gender, "date of birth:",
              self.dateOfBirth, "height:", self.height, "weight:", self.weight, "activityClass", self.activityClass)

    def add_measurement(self, m):
        self.measurements.append(m)

    def get_measurement(self):
        return self.measurements
