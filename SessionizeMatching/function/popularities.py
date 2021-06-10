from collections import OrderedDict

class Popularities:
    def __init__(self, users_preferences):
        self.language_popularities = {}
        self.user_popularities = {}
        self.define_language_popularity(users_preferences)
        self.define_user_popularities(users_preferences)

    def define_language_popularity(self, users_preferences):
        for user, preferences in users_preferences.items():
            for language in preferences:
                if language not in self.language_popularities:
                    self.language_popularities[language] = 0
                else:
                    self.language_popularities[language] +=  1

    def define_user_popularities(self, users_preferences):
        #doc string
        for user, preferences in users_preferences.items():
            popularity = 0
            for language_priority, language in enumerate(reversed(preferences)):
                language_priority += 1
                popularity += (self.language_popularities[language] * language_priority)
            self.user_popularities[user] = popularity
    
    def sort_user_popularities(self, numOfUsers):
        self.user_popularities = dict(sorted(self.user_popularities.items(), key=lambda item: item[1]))
        OrderedPopularities = OrderedDict(self.user_popularities)
        if numOfUsers < 4:
            most_popular = (list(OrderedPopularities)[-1])
            return most_popular
        return next(iter(self.user_popularities))
    
    def remove_from_user_popularities(self, toRemove):
        for user in toRemove:
            self.user_popularities.pop(user, None)