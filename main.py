from classes.menu import MenuGenerator
from classes.user import User
from classes.databaseConnector import DatabaseConnector
from classes.application import Application

connector = DatabaseConnector("./classes/database")

folder = "./classes/database"

# Menu général et boucle de l'application
end = False
while not end:
    mainMenu = MenuGenerator("Bienvenue Au TeccSocial", [
        "Se connecter",
        "S'inscrire",
        "Réinitialiser les données", 
        "Quitter"
        ])
    
    match mainMenu.getChoice():
        case 1:
            application = Application(connector)
            application.connect()
        case 2:
            application = Application(connector)
            application.signup()
        case 3:
            databaseConnector = DatabaseConnector("./classes/database")
            databaseConnector.emptyFiles()
            print("Les fichiers sont supprimés !")
        case 4:
            print("Merci, à la prochaine")
            end = True