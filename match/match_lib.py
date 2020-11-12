
# A custom error to raise through matching if required
class MatchError(Exception):
    pass

# Contants to define types of questions
Q_YN = 10               # A yes-no question ("0" stands for "no", "1" stands for "yes")
Q_GT = 20               # A multiple choice one with every next option is better that the previous one, 
                      # e.g. "How good a you in C#"? (1-"never heard", 2-"a beginner", ... 5-"a C++ guru")
Q_EQ = 30           # Not used yet...

_questions = [         
    { 'id': 0, 'type': Q_YN, 'value': 1, 'weight': 0.75 },
    { 'id': 1, 'type': Q_GT, 'value': 0.75, 'weight': 1.0 },
    { 'id': 2, 'type': Q_EQ, 'value': 0.5, 'weight': 0.5 }
]

_answers = { 0: 1, 1: 0.5, 2: 0.4 }

_skill_questions = [
    { 'id': 0, 'type': Q_GT, 'skill_level': 0.5, 'wish_to_learn': 0.9, 'wish_to_engage': 0.9 },
    { 'id': 1, 'type': Q_GT, 'skill_level': 0.5, 'wish_to_learn': 0.9, 'wish_to_engage': 0.9 }
]

_skill_answers = {
    0: { 'skill_level': 0.5, 'wish_to_learn': 0.9, 'wish_to_engage': 0.5 },
    1: { 'skill_level': 0.6, 'wish_to_learn': 0.5, 'wish_to_engage': 1.0 }
}

# Matches a pair of one question and one answer
# Raises the "MatchError" custom exception if fails
def match_pair(q, a):
    if a < 0.0 or a > 1.0:  # If "a" value does not belong to [0, 1.0] range...
        raise MatchError
    if not 'weight' in q:   # If weight is not specified - make it "1.0"
        weight = 1.0
    else:
        weight = q['weight']

    if q['type'] == Q_YN:                       # A "yes-no" question
        return (q['value'] - a) * weight
    if q['type'] == Q_GT:                       # A "greater than" one
        diff = q['value'] - a
        if not (diff > 0):
            return 0
        return diff * weight
    if q['type'] == Q_EQ:                       # An "equal to" one
        return (q['value'] - a) * weight
    raise MatchError


# Matches an array-like of questions with a dictionary of answers
# "id" of a question matches the "key" of an answer, e.g. q = {'id': 1, ...} => a = { 1: {}, ... }
# Raises the "MatchError" custom exception if fails
# Input: "questions" - array-like; "anwsers" - dictionary; 
# "method" - matching method (by now it is a number to power the matching error up to)
def match_questions(questions, answers, method=2):
    if method < 1:
        raise MatchError
    matching_errors_sum = 0.0
    must_have_errors_sum = 0.0
    for q in questions:
        if not (q['id'] in answers):    # If there is no answer for a question...
            a = 0.0                     # ... making it 0
        else:
            a = answers[ q['id'] ]
                  
        e = match_pair(q, a)
        matching_errors_sum += e**method
        if not q['weight'] < 1.0:
            must_have_errors_sum += e**method 

    error = matching_errors_sum**(1.0/method) if matching_errors_sum > 0.0 else 0.0
    must_have_error = must_have_errors_sum**(1.0/method) if must_have_errors_sum > 0.0 else 0.0

    return { 
        'error': error, 
        'must_have_error': must_have_error 
    } 
# end of match_questions                    

# Matches an array-like of questions with a dictionary of answers
# "id" of a question matches the "key" of an answer, e.g. q = {'id': 1, ...} => a = { 1: {}, ... }
# Raises the "MatchError" custom exception if fails
# Input: "questions" - array-like; "anwsers" - dictionary; 
# "method" - matching method (by now it is a number to power the matching error up to)
def match_skills(skill_questions, skill_answers, method=2):
    if method < 1:
        raise MatchError
    skill_errors_sum = 0.0
    overskill_errors_sum = 0.0
    wish_to_learn_errors_sum = 0.0
    wish_to_engage_errors_sum = 0.0;
    for sq in skill_questions:
        id = sq['id']
        # Calculating skill error
        q = { 'type': Q_GT, 'value': sq['skill_level'] }
        a = skill_answers[id]['skill_level'] if id in skill_answers else 0.0
        error = match_pair(q, a)
        skill_errors_sum += error**method
        
        q['type'] = Q_EQ    # Calculating overskill
        error = match_pair(q, a)
        if error < 0:
            overskill_errors_sum += error**method

        # Calculating "wish to learn" error
        q = { 'type': Q_GT, 'value': sq['wish_to_learn'] }
        a = skill_answers[id]['wish_to_learn'] if id in skill_answers else 0.0
        error = match_pair(q, a)
        wish_to_learn_errors_sum += error**method

        # Calculating "wish_to_engage" error
        q = { 'type': Q_GT, 'value': sq['wish_to_engage'] }
        a = skill_answers[id]['wish_to_engage'] if id in skill_answers else 0.0
        error = match_pair(q, a)
        wish_to_engage_errors_sum += error**method

        skill_error = skill_errors_sum**(1.0/method) if skill_errors_sum > 0.0 else 0.0 
        overskill_error = overskill_errors_sum**(1.0/method) if overskill_errors_sum > 0.0 else 0.0 
        wtl_error = wish_to_learn_errors_sum**(1.0/method) if wish_to_learn_errors_sum > 0.0 else 0.0 
        wte_error = wish_to_engage_errors_sum**(1.0/method) if wish_to_engage_errors_sum > 0.0 else 0.0 

    return { 
        'skill_error': skill_error, 
        'overskill_error': overskill_error,
        'wish_to_learn_error': wtl_error, 
        'wish_to_engage_error': wte_error
    }
#end of match_skills

print(match_questions(_questions, _answers), "\n")
print(match_skills(_skill_questions, _skill_answers), "\n")

_users_answers = [
    { 'u_id': 1, 'q_id': 0, 'value': 1.0 }, 
    { 'u_id': 1, 'q_id': 1, 'value': 0.5 }, 
    { 'u_id': 1, 'q_id': 2, 'value': 0.4 },  
    { 'u_id': 2, 'q_id': 0, 'value': 0.5 }, 
    { 'u_id': 2, 'q_id': 1, 'value': 0.75 }, 
    { 'u_id': 2, 'q_id': 2, 'value': 0.25 }   
]

def match_users( questions, answers ):
    users_scoreboard = dict()
    answers_indexed_by_user = dict()
    for i in range(len(answers)):
        u_id = answers[i]['u_id']
        if not (u_id in answers_indexed_by_user):
            answers_indexed_by_user[u_id] = list()
        answers_indexed_by_user[u_id].append(i)

    for user_id in answers_indexed_by_user:
        answers_to_match = dict()
        for index in answers_indexed_by_user[user_id]:
            answers_to_match[ answers[index]['q_id'] ] = answers[index]['value']
        users_scoreboard[user_id] = match_questions(questions, answers_to_match)            
    return users_scoreboard

print(match_users(_questions, _users_answers), "\n")

_users_skills = [
    { 'u_id': 1, 'q_id':0, 'skill_level': 0.5, 'wish_to_learn': 0.9, 'wish_to_engage': 0.5 },
    { 'u_id': 1, 'q_id':1, 'skill_level': 0.6, 'wish_to_learn': 0.5, 'wish_to_engage': 1.0 },
    { 'u_id': 2, 'q_id':0, 'skill_level': 0.45, 'wish_to_learn': 0.75, 'wish_to_engage': 0.25 },
    { 'u_id': 2, 'q_id':1, 'skill_level': 0.6, 'wish_to_learn': 0.5, 'wish_to_engage': 1.0 }
]

# 0: { 'skill_level': 0.5, 'wish_to_learn': 0.9, 'wish_to_engage': 0.5 }
def match_users_by_skills( skill_questions, skill_answers ):
    users_scoreboard = dict()
    answers_indexed_by_user = dict()    # To have answers groupped by user
    for i in range(len(skill_answers)):
        u_id = skill_answers[i]['u_id']
        if not (u_id in answers_indexed_by_user):
            answers_indexed_by_user[u_id] = list()
        answers_indexed_by_user[u_id].append(i)

    for user_id in answers_indexed_by_user:
        answer_indexes = answers_indexed_by_user[user_id]
        user_answers = dict()
        for answer_index in answer_indexes:
            answer = skill_answers[ answer_index ]
            user_answers[ answer['q_id'] ] = answer
        users_scoreboard[user_id] = match_skills(skill_questions, user_answers)            
    
    return users_scoreboard

print(match_users_by_skills(_skill_questions, _users_skills), "\n")