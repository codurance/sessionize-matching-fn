#from matching import *
from . import matching


def set_usersAndPreferences():
    usersAndPreferences = {
        1 : ["Java", "Kotlin", "Python"],  #BEN
        2 : ["Java", "Python", "Kotlin"], #JOE
        3 : ["Python", "Scala", "VB"],    #Sarah
        4 : ["C#" , "Groovy", "Python"],    #George
        5 : ["Java", "Javascript", "Clojure"],    #Andras
        6 : ["Kotlin", "Scala", "Ruby"],    #Mark
        7 : ["Javascript", "Ruby", "VB"],    #Cameron
        8 : ["Java", "Python", "Delphi"],    #Sophie
    }
    return usersAndPreferences

# def test_reformat_input():
#     original_format = [
#         {
#             "user": "sophie",
#             "preferences": {
#                     "pref1": "lang1",
#                     "pref2": "lang2",
#                     "pref3": "lang3"
#             }
#         },
#         {
#             "user": "george",
#             "preferences": {
#                     "pref1": "lang1",
#                     "pref2": "lang2",
#                     "pref3": "lang3"
#             }
#         }
#     ]
#     correct_format = {
#         "sophie" : ["lang1", "lang2", "lang3"],
#         "george" : ["lang1", "lang2", "lang3"]
#     }
#     returned_format = reformat_input_for_function(original_format)
#     assert correct_format == returned_format


def test_language_weightings():
    usersAndPreferences = set_usersAndPreferences()
    language_popularities = matching.define_language_popularity(usersAndPreferences)
    correct_popularities = {
        "Java" : 3,
        "Kotlin" : 2,
        "Python" : 4,
        "Scala" :  1,
        "VB"  : 1,
        "C#"  : 0,
        "Groovy" : 0,
        "Javascript" : 1,
        "Clojure" : 0,
        "Ruby" : 1,
        "Delphi" : 0,
    }
    assert correct_popularities == language_popularities



def test_user_popularities():
    usersAndPreferences = set_usersAndPreferences()
    language_popularities = matching.define_language_popularity(usersAndPreferences)
    user_popularities = matching.define_user_popularities(usersAndPreferences, language_popularities)
    correct_popularities = {
        1 : 17,  #BEN
        2 : 19, #JOE
        3 : 15,    #Sarah
        4 : 4,    #George
        5 : 11,    #Andras
        6 : 9,    #Mark
        7 : 6,    #Cameron
        8 : 17,    #Sophie
    }
    assert correct_popularities == user_popularities


def test_minimal_pairing():
    usersAndPreferences = {1 : ["Java"], 2 : ["Java"]}
    pairings = matching.match({}, usersAndPreferences)
    correct_pairing = { 1 : {2 : "Java"} , 2 : {1 : "Java"} }
    assert pairings == correct_pairing


def test_two_pairings():
    usersAndPreferences = {1 : ["Java", "Python", "Kotlin"], 2 : ["Java", "Python", "VB"], 3: ["Kotlin", "Clojure", "Python"] , 4 : ["Kotlin", "Javascript", "SocialLife"]}
    pairings = matching.match({}, usersAndPreferences)
    correct_pairing = { 1 : {2 : "Java"} , 2 : {1 : "Java"}, 3 : {4 : "Kotlin"}, 4 : {3 : "Kotlin"} }
    assert pairings == correct_pairing

def test_two_pairings_complex():
    usersAndPreferences = {1 : ["Python", "Java", "Kotlin"], 2 : ["Scala", "Groovy", "VB"], 3: ["Python", "Clojure", "Kotlin"] , 4 : ["Python", "Java", "VB"]}
    pairings = matching.match({}, usersAndPreferences)
    correct_pairing = { 1 : {3 : "Python"} , 3 : {1 : "Python"}, 2 : {4 : "VB"}, 4 : {2 : "VB"} }
    assert pairings == correct_pairing

def test_acceptance_test():
    usersAndPreferences = set_usersAndPreferences()
    pairings = matching.match({}, usersAndPreferences)
    correct_Pairings = {
         7 : {5 : "Javascript"},  #Cam and Andras Javascript
         5 : {7 : "Javascript"},
         6 : {1 : "Kotlin"},  #Mark and Ben Kotlin
         1 : {6 : "Kotlin"},
         4 : {3 : "Python"}, #George and Sarah Python
         3 : {4 : "Python"},
         8 : {2 : "Java"},  #Sophie and Joe Java
         2 : {8 : "Java"}

    }
    assert pairings == correct_Pairings

def test_acceptance_test_second_week_1():
    previous_pairings = {
         7 : {5 : "Javascript"},  #Cam and Andras Javascript
         5 : {7 : "Javascript"},
         6 : {1 : "Kotlin"},  #Mark and Ben Kotlin
         1 : {6 : "Kotlin"},
         4 : {3 : "Python"}, #George and Sarah Python
         3 : {4 : "Python"},
         8 : {2 : "Java"},  #Sophie and Joe Java
         2 : {8 : "Java"}

    }
    usersAndPreferences = set_usersAndPreferences()
    pairings = matching.match(previous_pairings, usersAndPreferences)
    slightly_correct_pairings = {
        4: {8: 'Python'}, 
        8: {4: 'Python'}, 
        7: "unsuccessful",
        3: "unsuccessful",  
        6: {2: 'Kotlin'}, 
        2: {6: 'Kotlin'}, 
        5: {1: 'Java'}, 
        1: {5: 'Java'}        
     }
    assert pairings == slightly_correct_pairings



def test_acceptance_test_second_week():
    previous_pairings = {
         7 : {5 : "Javascript"},  #Cam and Andras Javascript
         5 : {7 : "Javascript"},
         6 : {1 : "Kotlin"},  #Mark and Ben Kotlin
         1 : {6 : "Kotlin"},
         4 : {3 : "Python"}, #George and Sarah Python
         3 : {4 : "Python"},
         8 : {2 : "Java"},  #Sophie and Joe Java
         2 : {8 : "Java"}

    }

    usersAndPreferences = matching.set_usersAndPreferences()
    pairings = matching.match(previous_pairings, usersAndPreferences)
    slightly_correct_pairings = {
        4: {8: 'Python'}, 
        8: {4: 'Python'}, 
        7: {3: 'Default'},
        3: {7: 'Default'},  
        6: {2: 'Kotlin'}, 
        2: {6: 'Kotlin'}, 
        5: {1: 'Java'}, 
        1: {5: 'Java'}        
     }
    assert pairings == slightly_correct_pairings

def run_all_tests():
    test_language_weightings()
    test_user_popularities()
    test_minimal_pairing()
    test_two_pairings()
    test_two_pairings_complex()
    test_acceptance_test()


if __name__ == "__main__":
    test_language_weightings()
    test_user_popularities()
    test_minimal_pairing()
    test_two_pairings()
    test_two_pairings_complex()
    test_acceptance_test()
    #test_acceptance_test_second_week_1()
    #test_acceptance_test_second_week()
    #print("Everything passed")