from .menu import MenuGenerator
from .user import User

class FriendList:
    def __init__(self) -> None:
        pass

    def show(self, listOfFriends: list[User]):
        if len(listOfFriends) == 0:
            print("Vous n'avez actuellement aucun ami")
            return

        menu = MenuGenerator("--- Choisir l'une des options suivantes pour l'ordre d'affichage:", [
            "Affichage normal",
            "Affichage par nom d'utilisateur",
            "Affichage par nom de famille",
            "Affichage par prénom"
        ])

        match menu.getChoice():
            case 1:
                self.__showNormal(listOfFriends)
            case 2:
                self.__showByUsername(listOfFriends)
            case 3:
                self.__showByLastName(listOfFriends)
            case 4:
                self.__showByFirstName(listOfFriends)

    def __showNormal(self, listOfFriends: list[User]):
        # Affichage sans tri
        self.__showList(listOfFriends)

    def __showByUsername(self, listOfFriends: list[User]):
        # Tri par nom d'utilisateur
        listOfFriends.sort(key=lambda x: x.username)
        self.__showList(listOfFriends)

    def __showByLastName(self, listOfFriends: list[User]):
        # TODO: Tri par nom de famille
        listOfFriends.sort(key=lambda x: x.lastName)
        self.__showList(listOfFriends)
        

    def __showByFirstName(self, listOfFriends: list[User]):
        # TODO: Tri par prénom
        listOfFriends.sort(key=lambda x: x.firstName)
        self.__showList(listOfFriends)

    def __showList(self, listOfFriends: list[User]):
        # Imprimer le nombre des amis
        print(f"------ Vous avez {len(listOfFriends)} amis actuellement -----\n")
        # Afficher la liste
        for friend in listOfFriends:
            print("#" * 50)
            print(f"### Nom d'utilisateur: {friend.username}")
            print(f"### Nom: {friend.lastName}")
            print(f"### Prénom: {friend.firstName}")
            print("#" * 50)
            print("")
        pass