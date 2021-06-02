#import pandas as pd
from SessionizeMatching.function.pairing_list import PairingsList


def match(prev_pairing, users_preferences):
    users_preferences = reformat_input_for_function(users_preferences)
    prev_pairing_object = prev_pairing_into_object(prev_pairing)

    language_popularities = define_language_popularity(users_preferences)
    user_popularities = define_user_popularities(users_preferences, language_popularities)

    pairings = create_pairings(prev_pairing_object, user_popularities, language_popularities, users_preferences)

    return pairings.return_list()

def reformat_input_for_function(users_preferences):
    reformatted = {}
    #dictionary comprehension - to research 
    for user in users_preferences:
        reformatted[user["user"]] = list(user["preferences"].values())
    return reformatted

def prev_pairing_into_object(prev_pairing):
    prev_pairing_object = PairingsList()
    for pairing in prev_pairing:
        prev_pairing_object.addPairing(pairing["users"][0], pairing["users"][1], pairing["language"])
    return prev_pairing_object

def create_pairings(prev_pairing_object, user_popularities, language_popularities, users_preferences):
    pairings = PairingsList()
    pairings = minimal_pairings_recursive(prev_pairing_object, user_popularities, language_popularities, users_preferences, pairings)
    #quality_of_pairing = calculate_quality_of_pairing(pairings.copy(), users_preferences, 0)
    return pairings


#TO BE INTRODUCED MVP 2
# def calculate_quality_of_pairing(pairings, users_preferences, quality):
#     if (bool(pairings)):
#         first_pair = next(iter(pairings))
#         print(first_pair) 
#         preferences = users_preferences[first_pair] #1[groovy, python c#]
#         print (preferences)
#     return quality

def define_language_popularity(users_preferences):
    language_popularity = {}
    for user, preferences in users_preferences.items():
        for language in preferences:
            if language not in language_popularity:
                language_popularity[language] = 0
            else:
                language_popularity[language] +=  1
    return language_popularity

def define_user_popularities(users_preferences, language_popularities):
    #doc string
    user_popularities = {}
    for user, preferences in users_preferences.items():
        popularity = 0
        for language_priority, language in enumerate(reversed(preferences)):
            language_priority += 1
            popularity += (language_popularities[language] * language_priority)
        user_popularities[user] = popularity
    return user_popularities


def minimal_pairings_recursive(prev_pairing, user_popularities, language_popularities, users_preferences, pairings):
    if not user_popularities:
        return pairings
    #better to convert to a list of pairings as this will preserve the order and then go by first index
    user_popularities = dict(sorted(user_popularities.items(), key=lambda item: item[1]))
    user = next(iter(user_popularities))
    preferences = users_preferences[user]
    for preference in preferences:
        language_popularity = language_popularities[preference]
        if language_popularity:
            pairings_and_popularities = find_user_with_same_lang_pref(prev_pairing, users_preferences, user_popularities, preference, user, pairings)
            user_popularities = pairings_and_popularities["user_popularities"]
            pairings = pairings_and_popularities["pairings"]
            minimal_pairings_recursive(prev_pairing, user_popularities, language_popularities, users_preferences, pairings)
            return pairings


def check_if_partner_is_suitable(first_partner, second_partner, prev_pairing):
    if (second_partner == first_partner):
        return False
    if prev_pairing.check_if_paired_previously(first_partner, second_partner):
        return False
    return True

def find_user_with_same_lang_pref(prev_pairing, users_preferences, user_popularities, preference, first_partner, pairings):
    preference_order = None
    potential_partner = first_partner
    for second_partner in user_popularities.keys():
        if check_if_partner_is_suitable(first_partner, second_partner, prev_pairing):
            preferences_second_partner = users_preferences[second_partner]
            for second_partner_preference in preferences_second_partner:
                if preference == second_partner_preference:
                    if preference_order is None or preference_order > preferences_second_partner.index(preference):
                        potential_partner = second_partner
                        preference_order = preferences_second_partner.index(preference)
    if first_partner == potential_partner:
        #This means there is noone who this person can be paired with on one of their language preferences
        pairings.set_pairing_as_unsuccessful(first_partner)
        user_popularities.pop(first_partner, None)
        return {"pairings" : pairings, "user_popularities": user_popularities}
    pairings.addPairing(first_partner, potential_partner, preference)
    #pairings = create_pairing(first_partner, potential_partner, preference, pairings)
    user_popularities.pop(first_partner, None)
    user_popularities.pop(potential_partner, None)
    return {"pairings" : pairings, "user_popularities": user_popularities}



# def minimal_pairings(user_popularities, language_popularities, users_preferences):
#     pairings = Pairings() 
#     user_popularities =  dict(sorted(user_popularities.items(), key=lambda item: item[1]))
#     for user in user_popularities.keys():
#             preferences = users_preferences[user]
#             for preference in preferences:
#                 if not pairings.check_if_user_is_unpaired(user):
#                     language_popularity = language_popularities[preference]
#                     if language_popularity != 0:
#                         pairings = find_user_with_same_lang_pref(users_preferences, user_popularities, preference, user, pairings)
#     return pairings
        

# def find_user_with_same_lang_pref_using_pandas(users_preferences, user_popularities, preference, first_partner):
#     df = pd.DataFrame.from_dict(users_preferences)
#     print("dataframe", df)
#     print("preference Find ", preference)
#     for second_partner in user_popularities.keys():
#         if second_partner != first_partner:
#             df_users_with_matching_pref = df.gt(preference)
#             # print("dataframe found: ",df_users_with_matching_pref)
#             # print("attempt2",df[df.eq(preference).any(1)])
#             print("attempt3", df.isin([preference]).any())
#             users_with_matching_pref = list(df_users_with_matching_pref.columns.values)

#             create_pairing(first_partner, second_partner, preference)

        


