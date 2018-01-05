class Processed:
    __instance = None

    @staticmethod
    def getInstance():
        if Processed.__instance == None:
            Processed()
        return Processed.__instance.already

    def __init__(self):
        if Processed.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Processed.__instance = self
            Processed.already = set()