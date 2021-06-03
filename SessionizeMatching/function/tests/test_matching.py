import sys

from SessionizeMatching.function import matching
from SessionizeMatching.function import popularities
from . import resources
#from SessionizeMatching.function.tests.resources import resources

def set_usersAndPreferences():
    usersAndPreferences = [
        {
            "user": "ben",
            "preferences": {
                    "pref1": "Java",
                    "pref2": "Kotlin",
                    "pref3": "Python"
            }
        },
        {
            "user": "joe",
            "preferences": {
                    "pref1": "Java",
                    "pref2": "Python",
                    "pref3": "Kotlin"
            }
        }, 
        {
            "user": "sarah",
            "preferences": {
                    "pref1": "Python",
                    "pref2": "Scala",
                    "pref3": "VB"
            }
        },
        {
            "user": "george",
            "preferences": {
                    "pref1": "C#",
                    "pref2": "Groovy",
                    "pref3": "Python"
            }
        },
        {
            "user": "andras",
            "preferences": {
                    "pref1": "Java",
                    "pref2": "Javascript",
                    "pref3": "Clojure"
            }
        },
        {
            "user": "mark",
            "preferences": {
                    "pref1": "Kotlin",
                    "pref2": "Scala",
                    "pref3": "Ruby"
            }
        },
        {
            "user": "cameron",
            "preferences": {
                    "pref1": "Javascript",
                    "pref2": "Ruby",
                    "pref3": "VB"
            }
        },
        {
            "user": "sophie",
            "preferences": {
                    "pref1": "Java",
                    "pref2": "Python",
                    "pref3": "Delphi"
            }
        }
    ]

    return usersAndPreferences

def test_reformat_input():
    original_format = [
        {
            "user": "sophie",
            "preferences": {
                    "pref1": "lang1",
                    "pref2": "lang2",
                    "pref3": "lang3"
            }
        },
        {
            "user": "george",
            "preferences": {
                    "pref1": "lang1",
                    "pref2": "lang2",
                    "pref3": "lang3"
            }
        }
    ]
    correct_format = {
        "sophie" : ["lang1", "lang2", "lang3"],
        "george" : ["lang1", "lang2", "lang3"]
    }
    returned_format = matching.reformat_input_for_function(original_format)
    assert correct_format == returned_format


def test_language_weightings():
    usersAndPreferences = set_usersAndPreferences()
    usersAndPreferences = matching.reformat_input_for_function(usersAndPreferences)
    popularities_class = popularities.Popularities(usersAndPreferences)
    language_popularities = popularities_class.language_popularities
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
    usersAndPreferences = matching.reformat_input_for_function(usersAndPreferences)
    popularities_class = popularities.Popularities(usersAndPreferences)
    user_popularities = popularities_class.user_popularities
    correct_popularities = {
        "ben" : 17, 
        "joe" : 19, 
        "sarah" : 15,
        "george" : 4,
        "andras" : 11,
        "mark" : 9,
        "cameron" : 6,
        "sophie" : 17,
    }
    assert correct_popularities == user_popularities


def test_minimal_pairing():
    usersAndPreferences = [
        {
            "user": "1",
            "preferences": {
                "pref1": "Java"
            }
        },
        {
            "user": "2",
            "preferences": {
                "pref1": "Java"
            }
        }
    ]
    pairings = matching.match({}, usersAndPreferences)
    correct_pairing = [
        {
            "users" : ["1", "2"],
            "language": "Java"
        }
    ]
    assert pairings == correct_pairing


def test_two_pairings():
    usersAndPreferences = [
        {
            "user": 1,
            "preferences": {
                    "pref1": "Java",
                    "pref2": "Python",
                    "pref3": "Kotlin"
            }
        },
        {
            "user": 2,
             "preferences": {
                    "pref1": "Java",
                    "pref2": "Python",
                    "pref3": "VB"
            }
        },
        {
            "user": 3,
             "preferences": {
                    "pref1": "Kotlin",
                    "pref2": "Clojure",
                    "pref3": "Python"
            }
        },
        {
            "user": 4,
             "preferences": {
                    "pref1": "Kotlin",
                    "pref2": "Java",
                    "pref3": "SocialLife"
            }
        },
    ]
    pairings = matching.match({}, usersAndPreferences)
    correct_pairing = [
        {
            "users" : [3, 4],
            "language": "Kotlin"
        },        
        {
            "users" : [2, 1],
            "language": "Java"
        }
    ]
    assert pairings == correct_pairing

def test_two_pairings_complex():
    usersAndPreferences = [
        {
            "user": 1,
            "preferences": {
                    "pref1": "Java",
                    "pref2": "Python",
                    "pref3": "Kotlin"
            }
        },
        {
            "user": 2,
             "preferences": {
                    "pref1": "Scala",
                    "pref2": "Groovy",
                    "pref3": "VB"
            }
        },
        {
            "user": 3,
             "preferences": {
                    "pref1": "Python",
                    "pref2": "Clojure",
                    "pref3": "Kotlin"
            }
        },
        {
            "user": 4,
             "preferences": {
                    "pref1": "Python",
                    "pref2": "Java",
                    "pref3": "VB"
            }
        },
    ]
    pairings = matching.match({}, usersAndPreferences)
    correct_pairing = [
        {
            "users" : [2, 4],
            "language": "VB"
        },
        {
            "users" : [3, 1],
            "language": "Python"
        }        
    ]
    assert pairings == correct_pairing

def test_acceptance_test():
    usersAndPreferences = set_usersAndPreferences()
    pairings = matching.match({}, usersAndPreferences)
    correct_Pairings = [
        {
            "users" : ["george", "sarah"],
            "language" : "Python"
        },
        {
            "users" : ["cameron", "andras"],
            "language" : "Javascript"
        },
        {
            "users" : ["mark", "ben"],
            "language" : "Kotlin"
        },
        {
            "users" : ["sophie","joe"],
            "language" : "Java"
        }
    ]
    assert pairings == correct_Pairings

def test_acceptance_test_second_week_1():
    previous_pairings = [
        {
            "users" : ["george", "sarah"],
            "language" : "Python"
        },
        {
            "users" : ["cameron", "andras"],
            "language" : "Javascript"
        },
        {
            "users" : ["mark", "ben"],
            "language" : "Kotlin"
        },
        {
            "users" : ["sophie","joe"],
            "language" : "Java"
        }
    ]
    usersAndPreferences = set_usersAndPreferences()
    pairings = matching.match(previous_pairings, usersAndPreferences)
    slightly_correct_pairings = [
        {
            "users" : ["george","sophie"], 
            "language" : "Python"
        },
        {
            "users" : ["mark", "joe"],
            "language"  : "Kotlin"
        },
        {
            "users" : ["andras", "ben"],
            "language" : "Java"
        },
        {
            "users" : ["cameron","sarah"],
            "language" : "N/A"
        }
    ]
    assert pairings == slightly_correct_pairings

def test_second_week_with_uneven_numbers():
    previous_pairings = [
        {
            "users" : ["george", "sarah"],
            "language" : "Python"
        },
        {
            "users" : ["cameron", "andras"],
            "language" : "Javascript"
        },
        {
            "users" : ["mark", "ben"],
            "language" : "Kotlin"
        },
        {
            "users" : ["sophie","joe"],
            "language" : "Java"
        }
    ]
    usersAndPreferences = set_usersAndPreferences()
    newTestUser = {
            "user": "Jake",
             "preferences": {
                    "pref1": "UnknownLanguage1",
                    "pref2": "UnknownLanguage2",
                    "pref3": "UnknownLanguage3"
            }
    }
    usersAndPreferences.append(newTestUser)
    pairings = matching.match(previous_pairings, usersAndPreferences)
    sub_optimal_pairings = [
        {
            "users" : ["george","sophie"], 
            "language" : "Python"
        },
        {
            "users" : ["mark", "joe"],
            "language"  : "Kotlin"
        },
        {
            "users" : ["andras", "ben"],
            "language" : "Java"
        },
        {
            "users" : ["Jake","cameron"],
            "language" : "N/A"
        },
        {
            "users" : ["sarah"],
            "language" : "unsuccessful"
        }
    ]
    assert pairings == sub_optimal_pairings




def run_all_tests():
    test_language_weightings()
    test_user_popularities()
    test_reformat_input()
    test_minimal_pairing()
    test_two_pairings()
    test_two_pairings_complex()
    test_acceptance_test()


if __name__ == "__main__":
    test_language_weightings()
    test_user_popularities()
    test_reformat_input()
    test_minimal_pairing()
    test_two_pairings()
    test_two_pairings_complex()
    test_acceptance_test()
    #test_acceptance_test_second_week_1()
    #test_acceptance_test_second_week()
    #print("Everything passed")