import json
import os

class TCTData:
    def __init__(self, questions, answers, issues, state_issue_score, candidate_issue_score, running_mate_issue_score, candidate_state_multiplier, answer_score_global, answer_score_issue, answer_score_state, answer_feedback, states):
        self.questions = questions
        self.answers = answers
        self.issues = issues
        self.state_issue_score = state_issue_score
        self.candidate_issue_score = candidate_issue_score
        self.running_mate_issue_score = running_mate_issue_score
        self.candidate_state_multiplier = candidate_state_multiplier
        self.answer_score_global = answer_score_global
        self.answer_score_issue = answer_score_issue
        self.answer_score_state = answer_score_state
        self.answer_feedback = answer_feedback
        self.states = states

    def get_answers_for_question(self, pk):
        return [answer for answer in self.answers.values() if answer['fields']['question'] == pk]

    def get_advisor_feedback_for_answer(self, pk):
        return [feedback for feedback in self.answer_feedback if feedback['fields']['answer'] == pk]

def load_data(folder_name):
    questions = {}
    answers = {}
    states = {}

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
    f.close()

    f = open(os.path.join(folder_name, "answerScoreGlobals.json"))
    answer_score_globals_json = json.load(f)
    f.close()

    f = open(os.path.join(folder_name, "answerScoreIssues.json"))
    answer_score_issues_json = json.load(f)
    f.close()

    f = open(os.path.join(folder_name, "answerScoreStates.json"))
    answer_score_states_json = json.load(f)
    f.close()

    f = open(os.path.join(folder_name, "candidateIssueScores.json"))
    candidate_issue_scores_json = json.load(f)
    f.close()

    f = open(os.path.join(folder_name, "candidateStateMultipliers.json"))
    candidate_state_multipliers_json = json.load(f)
    f.close()

    f = open(os.path.join(folder_name, "issues.json"))
    issues_json = json.load(f)
    f.close()

    f = open(os.path.join(folder_name, "runningMateIssueScores.json"))
    running_mate_issue_scores_json = json.load(f)
    f.close()

    f = open(os.path.join(folder_name, "stateIssueScores.json"))
    state_issue_scores_json = json.load(f)
    f.close()

    data = TCTData(questions, answers, issues_json, state_issue_scores_json, candidate_issue_scores_json, running_mate_issue_scores_json, candidate_state_multipliers_json, answer_score_globals_json, answer_score_issues_json, answer_score_states_json, answer_feedbacks_json, states)

    return data
