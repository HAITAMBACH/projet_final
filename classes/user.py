class User:
    def __init__(self, 
    username, 
    firstName, 
    lastName, 
    dateOfBirth = "2000-01-01",
    friendsList = []
    ) -> None:
        self.username = username
        self.firstName = firstName
        self.lastName = lastName
        self.dateOfBirth = dateOfBirth
        self.friendsList = friendsList

    def __eq__(self, other):
        return self.username == other.username \
            and self.firstName == other.firstName \
            and self.lastName == other.lastName \
            and self.dateOfBirth == other.dateOfBirth \
            and self.friendsList == other.friendsList