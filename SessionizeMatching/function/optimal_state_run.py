from SessionizeMatching.function.pairing_list import PairingsList

class OptimatStateRun:

    def __init__(self, pairings, users_preferences):
        self.pairings = pairings
        self.users_preferences = users_preferences
        self.pairings_success = {}
        quality = self.calculate_quality_of_pairing()
        print(quality)
        self.pairings_success[self.pairings] = quality

    
    def recalculate(self):
        for pairing in self.pairings.listOfPairings:
            print()
        return self.pairings


    def calculate_quality_of_pairing(self):
        quality = 0
        for pairing in self.pairings.listOfPairings:
            for user in pairing["users"]:
                language = pairing["language"]
                try: 
                    # print()
                    # print(user)
                    preferences = self.users_preferences[user]
                    # print("preferences: ")
                    # print(preferences)
                    # print("reversed:")
                    preferences.reverse()
                    # print(preferences)
                    # print(language)
                    # print("index:")
                    quality += preferences.index(language) + 1
                    # print(preferences.index(language) + 1)
                    # print()
                except: 
                    pass
        return quality

    
#TO BE INTRODUCED MVP 2
# def calculate_quality_of_pairing(pairings, users_preferences, quality):
#     if (bool(pairings)):
#         first_pair = next(iter(pairings))
#         print(first_pair) 
#         preferences = users_preferences[first_pair] #1[groovy, python c#]
#         print (preferences)
#     return quality
