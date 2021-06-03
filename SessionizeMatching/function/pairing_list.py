class PairingsList:

    def __init__(self):
        self.listOfPairings = []
        self.listUnsuccessful = []
        self.unsuccessful = "unsuccessful"
        self.paired_without_preference = "N/A"
    
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

    def try_pair_later(self, user):
        self.listUnsuccessful.append(user)

    def set_pairing_as_unsuccessful(self, user):
        newPairing = {
            "users" : [user],
            "language": self.unsuccessful
        }
        self.listOfPairings.append(newPairing)
    
    def check_if_paired_previously(self, first_partner, second_partner):
        for pairing in self.listOfPairings:
            if first_partner in pairing["users"] and second_partner in pairing["users"]:
                return True
        return False
    

    def try_match_unsuccessful(self):
        to_be_paired = [self.listUnsuccessful[i:i + 2] for i in range(0, len(self.listUnsuccessful), 2)]
        for new_pairing in to_be_paired:
            if len(new_pairing) > 1:
                self.addPairing(new_pairing[0], new_pairing[1], self.paired_without_preference)
            else:
                self.set_pairing_as_unsuccessful(new_pairing[0])