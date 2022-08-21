class MenuGenerator:
    def __init__(self, message, listOfChoices) -> None:
        self.message = message
        self.listOfChoices = listOfChoices

    def getChoice(self):
        self.showMenu()
        
        choiceString = input("Entrer un choix: ")
        while not choiceString.isnumeric() or int(choiceString) < 1 or int(choiceString) > len(self.listOfChoices):
            print("Le choix n'est pas dans la liste")
            choiceString = input("Entrer un choix: ")

        return int(choiceString)

    def showMenu(self):
        print(("*" * 10) + " " + self.message + " " + ("*" * 10))
        for i, choiceElement in enumerate(self.listOfChoices):
            print(f"{i + 1}- {choiceElement}")