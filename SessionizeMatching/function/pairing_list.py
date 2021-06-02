class PairingsList:

    def __init__(self):
        self.listOfPairings = []
    
    def addPairing(self, firstPartner, secondPartner, languageChoice):
        newPairing = {
            "users" : [firstPartner, secondPartner],
            "language": languageChoice
        }
        self.listOfPairings.append(newPairing)
    
    def check_if_user_is_unpaired(self, user):
        for pairing in self.listOfPairings:
            if user in pairing["users"]:
                return False
        return True
    
    def set_pairing_as_unsuccessful(self, user):
        newPairing = {
            "users" : [user],
            "language": "unsuccessful"
        }
        self.listOfPairings.append(newPairing)
    
    def check_if_paired_previously(self, first_partner, second_partner):
        for pairing in self.listOfPairings:
            if first_partner in pairing["users"] and second_partner in pairing["users"]:
                return True
        return False

    
    def return_list(self):
        return self.listOfPairings

