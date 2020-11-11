
# A custom error to raise through matching if required
class MatchError(Exception):
    pass

# Contants to define types of questions
Q_YN = 10               # A yes-no question ("0" stands for "no", "1" stands for "yes")
Q_GT = 20               # A multiple choice one with every next option is better that the previous one, 
                      # e.g. "How good a you in C#"? (1-"never heard", 2-"a beginner", ... 5-"a C++ guru")
Q_EQ = 30           # Not used yet...

questions = [         
    { 'id': 0, 'type': Q_YN, 'value': 1, 'weight': 0.75 },
    { 'id': 1, 'type': Q_GT, 'value': 0.75, 'weight': 1.0 },
    { 'id': 2, 'type': Q_EQ, 'value': 0.5, 'weight': 0.5 }
]

answers = {         
    0: { 'value': 1 },
    1: { 'value': 0.5 },
    2: { 'value': 0.4 }
}

skill_questions = [
    { 'id': 0, 'type': Q_GT, 'skill_level': 0.5, 'wish_to_learn': 0.9, 'wish_to_engage': 0.9 },
    { 'id': 1, 'type': Q_GT, 'skill_level': 0.5, 'wish_to_learn': 0.9, 'wish_to_engage': 0.9 }
]

skill_answers = {
    0: { 'skill_level': 0.5, 'wish_to_learn': 0.9, 'wish_to_engage': 0.5 }
}

# Matches a pair of one question and one answer
# Raises the "MatchError" custom exception if fails
def match_pair(q, a):
    if not 'weight' in q:
        weight = 1.0
    else:
        weight = q.weight

    if q['type'] == Q_YN:
        return (q.value - a.value) * weight
    if q['type'] == Q_GT:
        diff = q.value - a.value
        if not (diff > 0):
            return 0
        return diff * weight
    if q['type'] == Q_EQ:
        return abs(q.value - a.value) * weight
    raise MatchError


# Matches an array of questions with an array of answers, both arrays must be of the same size
# Raises the "MatchError" custom exception if fails
# Input: "questions" - array-like; "anwsers" - array-like; "method" - matching method (by now it is a number to power the matching error)
def match_questions(questions, answers, method=2):
    matching_errors_sum = 0.0
    weight1_matching_errors_sum = 0.0
    for q in questions:
        if not (q['id'] in answers):    # If there is no answer to a question...
            a = { 'value': 0.0 }
        else:
            a = answers[ a['id'] ]
                  
        matching_error = match_pair(q, a)
        matching_errors_sum += matching_error**method
        if not q.weight < 1.0:
            weight1_matching_errors_sum += matching_error 

    return matching_errors_sum, weight1_matching_errors_sum
                    

def match_skills(skill_questions, skill_answers, method=2):
    skill_matching_errors_sum = 0.0
    wish_to_learn_errors_sum = 0.0
    wish_to_engage_errors_sum = 0.0;
    for sq in skill_questions:
        q = { 'type': Q_GT, 'value': s['skill_level'] }
        id = q['id']
        a = s[id].skill_level if id in skill_answers else 0.0
        error = match_pair(q, a)
        skill_matching_errors_sum += error**method

        q = { 'type': Q_GT, 'value': s['wish_to_learn'] }
        id = q['id']
        a = s[id].wish_to_learn if id in skill_answers else 0.0
        error = match_pair(q, a)
        wish_to_learn_errors_sum += error**method

        q = { 'type': Q_GT, 'value': s['wish_to_engage'] }
        id = q['id']
        a = s[id].wish_to_engage if id in skill_answers else 0.0
        error = match_pair(q, a)
        wish_to_engage_errors_sum += error**method

    return skill_matching_errors_sum, wish_to_learn_errors_sum, wish_to_engage_errors_sum


