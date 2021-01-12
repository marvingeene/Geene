class Config:
    byConfigId = "SELECT id, description, value from config where id = ?";
    
    def __init__(self,  configId,  configDescription,  configValue):
        self.configId = configId
        self.description = configDescription
        self.setValue(configValue)
        
    def __repr__(self):
        return self.configId + ", " + self.description +", " + str(self.value) 
        
    def setValue(self,  configValue):
        self.value = configValue
        
    def setDescription(self,  configDescription):
        self.description = configDescription
    
    @staticmethod
    def asConfigValue(dict):
        return Config(dict["configId"],  dict["description"],  dict["value"])
        

