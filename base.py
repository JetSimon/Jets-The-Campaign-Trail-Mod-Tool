import json
import os
import re

class TCTData:
    def __init__(self, questions, answers, issues, state_issue_scores, candidate_issue_score, running_mate_issue_score, candidate_state_multiplier, answer_score_global, answer_score_issue, answer_score_state, answer_feedback, states):
        self.questions = questions
        self.answers = answers
        self.issues = issues
        self.state_issue_scores = state_issue_scores
        self.candidate_issue_score = candidate_issue_score
        self.running_mate_issue_score = running_mate_issue_score
        self.candidate_state_multiplier = candidate_state_multiplier
        self.answer_score_global = answer_score_global
        self.answer_score_issue = answer_score_issue
        self.answer_score_state = answer_score_state
        self.answer_feedback = answer_feedback
        self.states = states

    def save_as_code_2(self, path):
        temp = None
        with open(os.path.join(path, "code2.txt"), "w") as f:
            f.write("campaignTrail_temp.questions_json = JSON.parse(\"")
            x = json.dumps(list(self.questions.values())).replace('"', "\\\"").replace("'", "\'").replace("â€™", "\'")
            f.write(x)
            f.write("\");\n")

            f.write("campaignTrail_temp.answers_json = JSON.parse(\"")
            x = json.dumps(list(self.answers.values())).replace('"', "\\\"").replace("'", "\'").replace("â€™", "\'")
            f.write(x)
            f.write("\");\n")

            f.write("campaignTrail_temp.states_json = JSON.parse(\"")
            x = json.dumps(list(self.states.values())).replace('"', "\\\"").replace("'", "\'")
            f.write(x)
            f.write("\");\n")

            f.write("campaignTrail_temp.issues_json = JSON.parse(\"")
            x = json.dumps(list(self.issues.values())).replace('"', "\\\"").replace("'", "\'").replace("â€™", "\'")
            f.write(x)
            f.write("\");\n")

            f.write("campaignTrail_temp.state_issue_score_json = JSON.parse(\"")
            x = json.dumps(list(self.state_issue_scores.values())).replace('"', "\\\"").replace("'", "\'")
            f.write(x)
            f.write("\");\n")

            f.write("campaignTrail_temp.candidate_issue_score_json = JSON.parse(\"")
            x = json.dumps(list(self.candidate_issue_score.values())).replace('"', "\\\"").replace("'", "\'")
            f.write(x)
            f.write("\");\n")

            f.write("campaignTrail_temp.running_mate_issue_score_json = JSON.parse(\"")
            x = json.dumps(list(self.running_mate_issue_score.values())).replace('"', "\\\"").replace("'", "\'")
            f.write(x)
            f.write("\");\n")

            f.write("campaignTrail_temp.candidate_state_multiplier_json = JSON.parse(\"")
            x = json.dumps(list(self.candidate_state_multiplier.values())).replace('"', "\\\"").replace("'", "\'")
            f.write(x)
            f.write("\");\n")

            f.write("campaignTrail_temp.answer_score_global_json = JSON.parse(\"")
            x = json.dumps(list(self.answer_score_global.values())).replace('"', "\\\"").replace("'", "\'")
            f.write(x)
            f.write("\");\n")

            f.write("campaignTrail_temp.answer_score_issue_json = JSON.parse(\"")
            x = json.dumps(list(self.answer_score_issue.values())).replace('"', "\\\"").replace("'", "\'")
            f.write(x)
            f.write("\");\n")

            f.write("campaignTrail_temp.answer_score_state_json = JSON.parse(\"")
            x = json.dumps(list(self.answer_score_state.values())).replace('"', "\\\"").replace("'", "\'")
            f.write(x)
            f.write("\");\n")

            f.write("campaignTrail_temp.answer_feedback_json = JSON.parse(\"")
            x = json.dumps(list(self.answer_feedback.values())).replace('"', "\\\"").replace("'", "\'")
            f.write(x)
            f.write("\");\n")

    def get_answers_for_question(self, pk):
        return [answer for answer in self.answers.values() if answer['fields']['question'] == pk]

    def get_advisor_feedback_for_answer(self, pk):
        return [feedback for feedback in self.answer_feedback.values() if feedback['fields']['answer'] == pk]

    def get_global_score_for_answer(self, pk):
        return [x for x in self.answer_score_global.values() if x['fields']['answer'] == pk]

    def get_state_score_for_answer(self, pk):
        return [x for x in self.answer_score_state.values() if x['fields']['answer'] == pk]

    def get_issue_score_for_answer(self, pk):
        return [x for x in self.answer_score_issue.values() if x['fields']['answer'] == pk]

    def get_issue_score_for_state(self, pk):
        return [x for x in self.state_issue_scores.values() if x['fields']['state'] == pk]
    
    def get_issue_score_for_candidate(self, pk):
        return [x for x in self.candidate_issue_score.values() if x['fields']['candidate'] == pk]
    
    def get_state_multiplier_for_candidate(self, pk):
        return [x for x in self.candidate_state_multiplier.values() if x['fields']['candidate'] == pk]

    def get_candidate_issue_score_for_issue(self, pk):
        return [x for x in self.candidate_issue_score.values() if x['fields']['issue'] == pk]

    def get_running_mate_issue_score_for_issue(self, pk):
        return [x for x in self.running_mate_issue_score.values() if x['fields']['issue'] == pk]

    def get_running_mate_issue_score_for_candidate(self, pk):
        return [x for x in self.running_mate_issue_score.values() if x['fields']['candidate'] == pk]

def extract_json(f, start, end):

    if(start not in f):
        print("ERROR: Start not in f")
        return None

    raw = f.strip().split(start)[1].split(end)[0].strip()

    if raw[0] == '"' or raw[0] == "'":
        raw = raw[1:]

    if raw[-1] == '"' or raw[-1] == "'":
        raw = raw[:len(raw)-1]

    res = json.loads(raw)

    if res == None:
        print("ERROR: Loading json was null, copied to clipboard")
        print(raw)

    return res

def load_data_from_file(file_name):

    if not os.path.exists(file_name):
        print("No data file exists, just making empty data")
        return TCTData({},{},{},{},{},{},{},{},{},{},{},{})

    questions = {}
    answers = {}
    states = {}
    feedbacks = {}

    answer_score_globals = {}
    answer_score_issues = {}
    answer_score_states = {}
    
    state_issue_scores = {}

    candidate_issue_scores = {}
    candidate_state_multipliers = {}
    running_mate_issue_scores = {}

    issues = {}

    raw_json = None
    with open(file_name, 'r') as f:
        raw_json = f.read()

    raw_json = raw_json.replace("\n", "")
    raw_json = re.sub(' +', ' ', raw_json)
    raw_json = raw_json.replace('\\"', '"')
    raw_json = raw_json.replace("\\'", "'")
    #raw_json = raw_json.replace("'", '"')

    states_json = extract_json(raw_json, "campaignTrail_temp.states_json = JSON.parse(", ");")
    for state in states_json:
        states[state["pk"]] = state

    questions_json = extract_json(raw_json, "campaignTrail_temp.questions_json = JSON.parse(", ");")
    for question in questions_json:
        question['fields']['description'] = question['fields']['description'].replace("â€™", "'").replace("â€”", "—")
        questions[question["pk"]] = question

    answers_json = extract_json(raw_json, "campaignTrail_temp.answers_json = JSON.parse(", ");")
    for answer in answers_json:
        answer['fields']['description'] = answer['fields']['description'].replace("â€™", "'").replace("â€”", "—")
        key = answer["pk"]
        answers[key] = answer

    answer_feedbacks_json = extract_json(raw_json, "campaignTrail_temp.answer_feedback_json = JSON.parse(", ");")
    for feedback in answer_feedbacks_json:
        feedback['fields']['answer_feedback'] = feedback['fields']['answer_feedback'].replace("â€™", "'").replace("â€”", "—")
        key = feedback['pk']
        feedbacks[key] = feedback

    answer_score_globals_json = extract_json(raw_json, "campaignTrail_temp.answer_score_global_json = JSON.parse(", ");")
    for x in answer_score_globals_json:
        key = x['pk']
        answer_score_globals[key] = x

    answer_score_issues_json = extract_json(raw_json, "campaignTrail_temp.answer_score_issue_json = JSON.parse(", ");")
    for x in answer_score_issues_json:
        key = x['pk']
        answer_score_issues[key] = x

    answer_score_states_json = extract_json(raw_json, "campaignTrail_temp.answer_score_state_json = JSON.parse(", ");")
    for x in answer_score_states_json:
        key = x['pk']
        answer_score_states[key] = x

    candidate_issue_scores_json = extract_json(raw_json, "campaignTrail_temp.candidate_issue_score_json = JSON.parse(", ");")
    for x in candidate_issue_scores_json:
        key = x['pk']
        candidate_issue_scores[key] = x

    candidate_state_multipliers_json = extract_json(raw_json, "campaignTrail_temp.candidate_state_multiplier_json = JSON.parse(", ");")
    for x in candidate_state_multipliers_json:
        key = x['pk']
        candidate_state_multipliers[key] = x

    running_mate_issue_scores_json = extract_json(raw_json, "campaignTrail_temp.running_mate_issue_score_json = JSON.parse(", ");")
    for x in running_mate_issue_scores_json:
        key = x['pk']
        running_mate_issue_scores[key] = x

    state_issue_scores_json = extract_json(raw_json, "campaignTrail_temp.state_issue_score_json = JSON.parse(", ");")
    for x in state_issue_scores_json:
        key = x['pk']
        state_issue_scores[key] = x

    issues_json = extract_json(raw_json, "campaignTrail_temp.issues_json = JSON.parse(", ");")
    for x in issues_json:
        key = x['pk']
        issues[key] = x

    data = TCTData(questions, answers, issues, state_issue_scores, candidate_issue_scores, running_mate_issue_scores, candidate_state_multipliers, answer_score_globals, answer_score_issues, answer_score_states, feedbacks, states)

    return data

def load_data(folder_name):
    questions = {}
    answers = {}
    states = {}
    feedbacks = {}

    answer_score_globals = {}
    answer_score_issues = {}
    answer_score_states = {}
    
    state_issue_scores = {}

    candidate_issue_scores = {}
    candidate_state_multipliers = {}
    running_mate_issue_scores = {}

    issues = {}
    
    f = open(os.path.join(folder_name, "states.json"))
    states_json = json.load(f)
    f.close()

    for state in states_json:
        states[state["pk"]] = state

    f = open(os.path.join(folder_name, "questions.json"))
    questions_json = json.load(f)
    f.close()

    for question in questions_json:
        questions[question["pk"]] = question

    f = open(os.path.join(folder_name, "answers.json"))
    answers_json = json.load(f)
    f.close()

    for answer in answers_json:
        key = answer["pk"]
        answers[key] = answer

    f = open(os.path.join(folder_name, "answerFeedback.json"))
    answer_feedbacks_json = json.load(f)

    for feedback in answer_feedbacks_json:
        key = feedback['pk']
        feedbacks[key] = feedback

    f.close()

    f = open(os.path.join(folder_name, "answerScoreGlobals.json"))
    answer_score_globals_json = json.load(f)
    for x in answer_score_globals_json:
        key = x['pk']
        answer_score_globals[key] = x
    f.close()

    f = open(os.path.join(folder_name, "answerScoreIssues.json"))
    answer_score_issues_json = json.load(f)
    for x in answer_score_issues_json:
        key = x['pk']
        answer_score_issues[key] = x
    f.close()

    f = open(os.path.join(folder_name, "answerScoreStates.json"))
    answer_score_states_json = json.load(f)
    for x in answer_score_states_json:
        key = x['pk']
        answer_score_states[key] = x
    f.close()

    f = open(os.path.join(folder_name, "candidateIssueScores.json"))
    candidate_issue_scores_json = json.load(f)
    for x in candidate_issue_scores_json:
        key = x['pk']
        candidate_issue_scores[key] = x
    f.close()

    f = open(os.path.join(folder_name, "candidateStateMultipliers.json"))
    candidate_state_multipliers_json = json.load(f)
    for x in candidate_state_multipliers_json:
        key = x['pk']
        candidate_state_multipliers[key] = x
    f.close()

    f = open(os.path.join(folder_name, "runningMateIssueScores.json"))
    running_mate_issue_scores_json = json.load(f)
    for x in running_mate_issue_scores_json:
        key = x['pk']
        running_mate_issue_scores[key] = x
    f.close()

    f = open(os.path.join(folder_name, "stateIssueScores.json"))
    state_issue_scores_json = json.load(f)
    for x in state_issue_scores_json:
        key = x['pk']
        state_issue_scores[key] = x
    f.close()

    f = open(os.path.join(folder_name, "issues.json"))
    issues_json = json.load(f)
    for x in issues_json:
        key = x['pk']
        issues[key] = x
    f.close()

    data = TCTData(questions, answers, issues, state_issue_scores, candidate_issue_scores, running_mate_issue_scores, candidate_state_multipliers, answer_score_globals, answer_score_issues, answer_score_states, feedbacks, states)

    return data
