
class create_assistant:
    def __init__(self, name):
        self.name = name
        self.memory = {'Name':self.name}
    def setMemory(self, key, txt):
        self.memory[key] = txt