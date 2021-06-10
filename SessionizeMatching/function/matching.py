#import pandas as pd
from SessionizeMatching.function.pairing_list import PairingsList
from SessionizeMatching.function.popularities import Popularities
from SessionizeMatching.function.optimal_state_run import OptimatStateRun


def match(prev_pairing, users_preferences):
    users_preferences = reformat_input_for_function(users_preferences)
    prev_pairing_object = prev_pairing_into_object(prev_pairing)

    popularities = Popularities(users_preferences)

    pairings = create_pairings(prev_pairing_object, popularities, users_preferences)
    optimal_pairings = OptimatStateRun(pairings, users_preferences)
    pairings = optimal_pairings.recalculate()

    return pairings.listOfPairings

def reformat_input_for_function(users_preferences):
    reformatted = {}
    for user in users_preferences:
        reformatted[user["user"]] = list(user["preferences"].values())
    return reformatted

def prev_pairing_into_object(prev_pairing):
    prev_pairing_object = PairingsList()
    for pairing in prev_pairing:
        prev_pairing_object.addPairing(pairing["users"][0], pairing["users"][1], pairing["language"])
    return prev_pairing_object

def create_pairings(prev_pairing_object, popularities, users_preferences):
    pairings = PairingsList()
    pairings = minimal_pairings_recursive(prev_pairing_object, popularities, users_preferences, pairings)
    #quality_of_pairing = calculate_quality_of_pairing(pairings.copy(), users_preferences, 0)
    return pairings
        

def minimal_pairings_recursive(prev_pairing, popularities, users_preferences, pairings):
    if not popularities.user_popularities:
        pairings.try_match_unsuccessful()
        return pairings
    #better to convert to a list of pairings as this will preserve the order and then go by first index
    least_popular_user = popularities.sort_user_popularities()
    preferences = users_preferences[least_popular_user]
    can_be_paired = False
    for preference in preferences:
        language_popularity = popularities.language_popularities[preference]
        if language_popularity:
            can_be_paired = True
            pairings_and_popularities = find_user_with_same_lang_pref(prev_pairing, users_preferences, popularities, preference, least_popular_user, pairings)
            restart_recursive_call(pairings_and_popularities, popularities, users_preferences, prev_pairing)
            return pairings
    if not can_be_paired:
        pairings_and_popularities = set_unsuccessful_partner_with_no_match(pairings, popularities, least_popular_user)
        restart_recursive_call(pairings_and_popularities, popularities, users_preferences, prev_pairing)
        return pairings

def restart_recursive_call(pairings_and_popularities, popularities, users_preferences, prev_pairing):
    popularities = pairings_and_popularities["popularities"]
    pairings = pairings_and_popularities["pairings"]
    minimal_pairings_recursive(prev_pairing, popularities, users_preferences, pairings)

def check_if_partner_is_suitable(first_partner, second_partner, prev_pairing):
    if (second_partner == first_partner) or prev_pairing.check_if_paired_previously(first_partner, second_partner):
        return False
    return True

def set_unsuccessful_partner_with_no_match(pairings, popularities, first_partner):
    pairings.try_pair_later(first_partner)
    popularities.remove_from_user_popularities([first_partner])
    return {"pairings" : pairings, "popularities": popularities}

def set_successful_partner_with_match(pairings, first_partner, potential_partner, preference, popularities):
    pairings.addPairing(first_partner, potential_partner, preference)
    popularities.remove_from_user_popularities([first_partner, potential_partner])
    return {"pairings" : pairings, "popularities": popularities}

def check_language_pairing_choice_is_correct(preference, preference_order, second_partner_preference, second_partner_preferences):
    if preference == second_partner_preference:
        if preference_order is None or preference_order > second_partner_preferences.index(preference):
            return True
    return False

def find_user_with_same_lang_pref(prev_pairing, users_preferences, popularities, preference, first_partner, pairings):
    preference_order = None
    potential_partner = first_partner
    for second_partner in popularities.user_popularities.keys():
        if check_if_partner_is_suitable(first_partner, second_partner, prev_pairing):
            second_partner_preferences = users_preferences[second_partner]
            for second_partner_preference in second_partner_preferences:
                if check_language_pairing_choice_is_correct(preference, preference_order, second_partner_preference, second_partner_preferences):
                    potential_partner = second_partner
                    preference_order = second_partner_preferences.index(preference)
    if first_partner == potential_partner:
        return set_unsuccessful_partner_with_no_match(pairings, popularities, first_partner)
    return set_successful_partner_with_match(pairings, first_partner, potential_partner, preference, popularities)

        


