import persistent

class Character(persistent.Persistent):
    byCharacterId = "SELECT * from config where id = ?";
    byPlayerId = "SELECT * from config where playerId = ?";


    def __init__(self, id, characterName,  characterImagePath, description, playerId,  playthroughId):
        self.id = id
        self.name = characterName
        self.imagePath = characterImagePath
        self.description = description
        self.playerId = playerId
        self.playthroughId = playthroughId
    
    def setImagePath(self,  characterImagePath):
        self.imagePath = characterImagePath
    
    @staticmethod
    def asCharacter(tuple):
        return Character(tuple[0],  tuple[1],  tuple[2],  tuple[3],  tuple[4],  tuple[5])
