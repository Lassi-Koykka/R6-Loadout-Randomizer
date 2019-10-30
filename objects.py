import json

class Operator():
    def __init__(self, name, primaries, secondaries, gadgets):
        self.name = name  #string
        self.primaries = primaries  #Lista weaponeja
        self.secondaries = secondaries  #Lista weaponeja
        self.gadgets = gadgets  #lista
    def __repr__(self):
        return f'{self.name}: \n {self.primaries} \n {self.secondaries} \n {self.gadgets}'
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)  


class weapon():
    def __init__(self, name, attachments):
        self.name = name
        self.attachments = attachments  #lista listoja joista kaikista arvotaan yksi
    def __repr__(self):
        return self.name + " " + str(self.attachments)