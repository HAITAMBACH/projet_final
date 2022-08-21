from asyncio.base_subprocess import ReadSubprocessPipeProto
from .user import User
from .post import Post
from .conversation import Conversation
from .conversation import ConversationMessage
from .userFriend import UserFriend

import json

class DatabaseConnector:
    def __init__(self, databaseFolder = "./database") -> None:
        self.databaseFolder = databaseFolder

    def getUser(self, username):
        users = self.readUsers()
        user = [x for x in users if x.username == username]
        if user:
            # remplir les informations de l'utilisateur et le retourner
            userFriend = self.getUserFriends(username)
            if userFriend:
                user[0].friendsList = userFriend[0].friends
            return user[0]
        
        return None

    def getUserFriends(self, username):
        userFriends = self.readFriends()
        return [x for x in userFriends if x.username == username]

    def getUsers(self, usernames, includeDetails = False) -> list[User]:
        users = [x for x in self.readUsers() if x.username in usernames]
        # Inclure les détails si demandé
        if includeDetails:
            for i in range(len(users)):
                users[i].friendsList = self.getUserFriends(users[i])

        return users

    def readUsers(self) -> list[User]:
        f = open(f"{self.databaseFolder}/users.json")
        data = json.load(f)
        f.close()
        users = []
        for jsonUser in data:
            users.append(User(jsonUser['username'], jsonUser['firstName'], jsonUser['lastName'], jsonUser['dateOfBirth']))
        
        return users

    def writeUsers(self, users: list[User]):
        with open(f"{self.databaseFolder}/users.json", "w") as f:
            json.dump(users, f, default=self._obj_dict)

    def readPosts(self) -> list[Post]:
        f = open(f"{self.databaseFolder}/posts.json")
        data = json.load(f)
        f.close()
        posts = []
        for jsonPost in data:
            posts.append(Post(jsonPost['username'], jsonPost['content'], jsonPost['postDate']))
        
        return posts

    def writePosts(self, posts: list[Post]):
        with open(f"{self.databaseFolder}/posts.json", "w") as f:
            json.dump(posts, f, default=self._obj_dict)

    def getPosts(self, usernames) -> list[Post]:
        posts = [x for x in self.readPosts() if x.username in usernames]
        return posts

    def readConversations(self) -> list[Conversation]:
        f = open(f"{self.databaseFolder}/conversations.json")
        data = json.load(f)
        f.close()
        conversations = []
        for jsonConversation in data:
            messages = []
            for message in jsonConversation["messages"]:
                messages.append(ConversationMessage(message["sender"], message["message"]))

            conversations.append(Conversation(jsonConversation['user1'], jsonConversation['user2'], messages))

        return conversations

    def getConversations(self, username, conversationUsernames) -> list[Conversation]:
        conversations = [x for x in self.readConversations() 
            if (x.user1 in conversationUsernames or x.user2 in conversationUsernames)
            and (x.user1 == username or x.user2 == username)]

        return conversations

    def writeConversations(self, conversations: list[Conversation]):
        with open(f"{self.databaseFolder}/conversations.json", "w") as f:
            json.dump(conversations, f, default=self._obj_dict)

    def readFriends(self) -> list[UserFriend]:
        # TODO: Compléter la méthode readFriends qui permet de lire le fichier friends.json
        # Inspirez vous des méthodes similaires dans ce fichier.
        f = open(f"{self.databaseFolder}/friends.json")
        data = json.load(f)
        f.close()
        friends = []
        for jsonFriend in data:
            friends.append(UserFriend(jsonFriend['username'], jsonFriend['friends']))
        return friends
        

    def writeFriends(self, friends: list[UserFriend]):
        # TODO: Compléter la méthode writeFriends. Inspirez vous des autres méthodes
        with open(f"{self.databaseFolder}/friends.json", "w") as f:
            json.dump(friends, f, default=self._obj_dict)

    def emptyFiles(self):
        # Vider le fichier friends.json
        with open(f"{self.databaseFolder}/friends.json", "w") as f:
            json.dump([], f)

        # Vider le fichier conversations.json
        with open(f"{self.databaseFolder}/conversations.json", "w") as f:
            json.dump([], f)

        # TODO: Vider le fichier posts.json
        with open(f"{self.databaseFolder}/posts.json", "w") as f:
            json.dump([], f)

        # TODO: Vider le fichier users.json
        with open(f"{self.databaseFolder}/users.json", "w") as f:
            json.dump([], f)

    def _obj_dict(self, obj):
        return obj.__dict__