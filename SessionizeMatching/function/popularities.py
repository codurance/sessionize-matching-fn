from collections import OrderedDict

class Popularities:
    def __init__(self, users_preferences):
        self.language_popularities = {}
        self.user_popularities = {}
        self.flag = False

        self.define_language_popularity(users_preferences)
        self.define_user_popularities(users_preferences)

    def define_language_popularity(self, users_preferences):
        """ This function returns ggg it also sets a flag which is then later used to decide whether 
        to return the least popular user to match first or the most popular user. If there are not many matchable
        languages in the database then we start with the most popular"""
        numOfMatchableLanguages = 0
        for user, preferences in users_preferences.items():
            for language in preferences:
                if language not in self.language_popularities:
                    self.language_popularities[language] = 0
                else:
                    numOfMatchableLanguages += 1
                    self.language_popularities[language] +=  1
        if numOfMatchableLanguages < 3 or len(users_preferences.keys()) < 4:
            self.flag = True

    def define_user_popularities(self, users_preferences):
        """ Once the """
        for user, preferences in users_preferences.items():
            popularity = 0
            for language_priority, language in enumerate(reversed(preferences)):
                language_priority += 1
                popularity += (self.language_popularities[language] * language_priority)
            self.user_popularities[user] = popularity
    
    def sort_user_popularities(self):
        self.user_popularities = dict(sorted(self.user_popularities.items(), key=lambda item: item[1]))
        OrderedPopularities = OrderedDict(self.user_popularities)
        if self.flag:
            most_popular = (list(OrderedPopularities)[-1])
            return most_popular
        least_popular = next(iter(self.user_popularities))
        return least_popular

    def remove_from_user_popularities(self, toRemove):
        for user in toRemove:
            self.user_popularities.pop(user, None)