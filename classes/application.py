import imp
from datetime import date, datetime
from classes.postList import PostList
from classes.userFriend import UserFriend
from .databaseConnector import DatabaseConnector
from .user import User
from .menu import MenuGenerator
from .friendList import FriendList
from .post import Post
from .conversation import ConversationManager

class Application:
    def __init__(self, databaseConnector: DatabaseConnector) -> None:
        self.databaseConnector = databaseConnector
        self.user = None

    def connect(self):
        # Demander le nom d'utilisateur
        username = input("Entrer un nom d'utilisateur pour se connecter: ")
        user = self.databaseConnector.getUser(username)
        if user:
            self.user = user
            self._startSession()
        else:
            print("L'utilisateur n'est pas inscrit dans la plateforme")

    def signup(self):
        # Collection des informations
        username = input("Entrer votre nom d'utilisateur: ")

        # TODO: Valider que le nom d'utilisateur est unique
        existingUsers = self.databaseConnector.readUsers()
        existingUsernames = (x.username for x in existingUsers)
        # Compléter la validation ici
        if username in existingUsernames:
            print("Le nom d'utilisateur existe déjà !"+'\n')
            return
            
        # TODO: Demander le reste des informations de utilisateur pour l'inscrire
        firstName = input("Entrer votre prénom: ")
        lastName = input("Entrer votre nom: ")
        dateOfBirth = input("Entrer votre date de naissance (YYYY-MM-DD): ")

        # Ajouter l'utilisateur
        existingUsers.append(User(username, firstName, lastName, dateOfBirth))
        self.databaseConnector.writeUsers(existingUsers)
        print("Merci d'avoir choisi notre application, vous pouvez se connecter dès maintenant !")


    def _startSession(self):
        print(("-" * 10) + f"BIENVENUE {self.user.firstName} {self.user.lastName}")

        connected = True
        while connected:
            print(("-" * 70) + "> " + self.user.username)
            menu = MenuGenerator("Choisissez l'une des options suivantes", [
                "Mes ami",
                "Poster",
                "Voir le mur",
                "Mes conversations",
                "Se déconnecter"
            ])

            match menu.getChoice():
                case 1:
                    self._friends()
                case 2:
                    self._addPost()
                case 3:
                    self._seePosts()
                case 4:
                    self._seeConversations()
                case 5:
                    connected = False

    def _friends(self):
        # TODO: Faire la méthode _friends qui permet d'afficher le menu suivant:
        # Choisissez l'une des options suivantes
        # 1- Voir la liste des amis | qui appelle la méthode _friendsList
        # 2- Ajouter un ami | qui appelle la méthode _addFriend
        # 3- Supprimer un ami | qui appelle la méthode _deleteFriend
        # 4- Retourner | qui revient au menu précédent

        # Il faut absolument utiliser la classe MenuGenerator pour cela !
        print(("-" * 10) + "MES AMIS")
        # Le code à finir ici
        menu = MenuGenerator("Choisissez l'une des options suivantes", [
                "1- Voir la liste des amis",
                "2- Ajouter un ami",
                "3- Supprimer un ami ",
                "4- Retourner"
            ])
        match menu.getChoice():
            case 1:
                self._friendsList()
            case 2:
                self._addFriend()
            case 3:
                self._deleteFriend()
            case 4:
                self._startSession()
    
    def _friendsList(self):
        myFriendsDetails = self.databaseConnector.getUsers(self.user.friendsList)
        friendList = FriendList()
        friendList.show(myFriendsDetails)

    def _addFriend(self):
        print(("-" * 6) + "Ajouter un nouveau ami" + ("-" * 6))
        newFriendUsername = input("Entrer le nom d'utilisateur du nouveau ami: ")
        # Vérifier si l'utilisateur existe
        user = self.databaseConnector.getUser(newFriendUsername)
        if user:
            # Vérifier que l'utilisateur n'est pas deja un ami
            if not newFriendUsername in self.user.friendsList and newFriendUsername != self.user.username:
                # Ajouter dans la liste des amis
                friends = self.databaseConnector.readFriends()
                usernamesInFriendList = [x.username for x in friends]
                self.user.friendsList.append(newFriendUsername)
                if self.user.username in usernamesInFriendList:
                    friendsIndex = usernamesInFriendList.index(self.user.username)
                    friends[friendsIndex].friends = self.user.friendsList
                else:
                    friends.append(UserFriend(self.user.username, self.user.friendsList))

                # Add to the other user list
                if newFriendUsername in usernamesInFriendList:
                    otherIndex = usernamesInFriendList.index(newFriendUsername)
                    friends[otherIndex].friends.append(self.user.username)
                else:
                    friends.append(UserFriend(newFriendUsername, [self.user.username]))
                
                self.databaseConnector.writeFriends(friends)
                print(f"L'utilisateur {newFriendUsername} est maintenant votre ami !")
            else:
                print("L'utilisateur est déjà un ami avec vous !")
        else:
            print("L'utilisateur n'existe pas !")

    def _deleteFriend(self):
        # TODO: Implémenter la méthode supprimer un ami.
        # Il faut demander d'entrer un nom d'utilisateur
        # Si l'utilisateur est ami, l'enlever de la liste et affichier L'utilisateur [utilisateur] n'est plus votre ami
        # Sinon si l'utilisateur n'était pas un ami, afficher: L'utilisateur n'était pas votre ami !
        # Aide: Pour trouver l'indice de la liste d'amis, utiliser: friendsIndex = [x.username for x in friends].index(self.user.username)
        print(("-" * 6) + "Supprimer un ami" + ("-" * 6))
        # Compléter la méthode ici
        friend = input('Entrer le nom d\'utilisateur du ami à supprimer: ')
        friends = self.databaseConnector.readFriends()
        usernamesInFriendList = [x.username for x in friends]
        if friend in usernamesInFriendList:
            friendsIndex = usernamesInFriendList.index(self.user.username)
            friends[friendsIndex].friends.remove(friend)
            self.databaseConnector.writeFriends(friends)
            print(f"L'utilisateur {friend} n'est plus votre ami !")

    def _addPost(self):
        print(("-" * 6) + "Ajouter un nouveau post" + ("-" * 6))
        content = input("Entrer le contenu du post: ")
        # Demander à l'utilisateur d'entrer le poste tant qu'il est vide
        while content == "":
            print("Le contenu est vide !")
            content = input("Entrer le contenu du post: ")
        
        posts = self.databaseConnector.readPosts()
        posts.append(Post(self.user.username, content, datetime.now().isoformat()))
        self.databaseConnector.writePosts(posts)

    def _seePosts(self):
        myFriendsPosts = self.databaseConnector.getPosts(self.user.friendsList)
        postList = PostList()
        postList.show(myFriendsPosts)

    def _seeConversations(self):
        myConversations = self.databaseConnector.getConversations(self.user.username, self.user.friendsList)
        conversationManager = ConversationManager(self.databaseConnector)
        conversationManager.show(self.user, myConversations)