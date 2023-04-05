from base import *
from ui import *
import PySimpleGUI as sg

global window
global data
global state
global can_pk
global issue
global current_mode
global current_answers
global layout
global question

sg.theme('SystemDefault')

data = load_data_from_file("default_code2.js")
current_answers = []
question = data.questions[min(data.questions.keys())] if len(data.questions) > 0 else None
state = None
can_pk = None
issue = None

layout = create_question_layout(data, question, current_answers)

# Create the window
window = sg.Window("Jet's TCT Mod Maker", layout, size=(1000,800), resizable=True)

current_mode = "QUESTION"

def save_current_workspace():
    try:
        if current_mode == "QUESTION":
            save_question()
        elif current_mode == "STATE":
            save_state()
        elif current_mode == "CAN":
            save_candidate()
        elif current_mode == "ISSUE":
            save_issue()
    except Exception as e:
        sg.popup_error_with_traceback(f'An error happened.  Here is the info:', e)

def save_state():
    pk = state['pk']
    data.states[pk]['fields']['electoral_votes'] = int(window['electoral_votes'].get())
    data.states[pk]['fields']['popular_votes'] = int(window['popular_votes'].get())

    i = 0
    for x in data.get_issue_score_for_state(pk):
        x_pk = x['pk']
        data.state_issue_scores[x_pk]['fields']['issue'] = int(window[f"issue_issue_{i}"].get())
        data.state_issue_scores[x_pk]['fields']['state_issue_score'] = float( window[f"issue_state_issue_score_{i}"].get())
        data.state_issue_scores[x_pk]['fields']['weight'] = float(window[f"issue_weight_{i}"].get())
        i += 1

def save_question():

    pk = question['pk']
    data.questions[pk]['fields']['description'] = window["description"].get()
    data.questions[pk]['fields']['priority'] = int(window["priority"].get())
    data.questions[pk]['fields']['likelihood'] = float(window["likelihood"].get())                 

    i = 0
    for answer in current_answers:
        ans_pk = answer['pk']
        data.answers[ans_pk]['fields']['description'] = window[f"description_ans{i}"].get()
        
        j = 0
        for feedback in data.get_advisor_feedback_for_answer(ans_pk):
            feedback_pk = feedback['pk']
            data.answer_feedback[feedback_pk]['fields']['candidate'] = int(window[f"candidate_ans{i}_feedback_{j}"].get())
            data.answer_feedback[feedback_pk]['fields']['answer_feedback'] = window[f"description_ans{i}_feedback_{j}"].get()
            j += 1

         # add global score
        j = 0
        for x in data.get_global_score_for_answer(answer['pk']):
            pk = x['pk']
            data.answer_score_global[pk]['fields']['candidate'] = int(window[f"ans{i}_global_score_candidate_{j}"].get())
            data.answer_score_global[pk]['fields']['affected_candidate'] = int(window[f"ans{i}_global_score_affected_candidate_{j}"].get())
            data.answer_score_global[pk]['fields']['global_multiplier'] = float(window[f"ans{i}_global_score_multiplier_{j}"].get())
            j += 1

        # add issue score
        j = 0
        for x in data.get_issue_score_for_answer(answer['pk']):
            pk = x['pk']
            data.answer_score_issue[pk]['fields']['issue'] = int(window[f"ans{i}_issue_score_issue_{j}"].get())
            data.answer_score_issue[pk]['fields']['issue_score'] = float(window[f"ans{i}_issue_score_issue_score_{j}"].get())
            data.answer_score_issue[pk]['fields']['issue_importance'] = float(window[f"ans{i}_issue_score_issue_importance_{j}"].get())
            j += 1

        # add state score
        j = 0
        for x in data.get_state_score_for_answer(answer['pk']):

            j += 1
        i += 1

def save_issue():
    pk = issue['pk']
    data.issues[pk]['fields']['name'] = window["issue_name"].get()
    data.issues[pk]['fields']['election'] = int(window["election"].get())

    for i in range(1, 8):
        data.issues[pk]['fields'][f'stance_{i}'] = window[f"stance_{i}"].get()

    i = 0
    for x in data.get_candidate_issue_score_for_issue(issue['pk']):
        
        data.candidate_issue_score[x['pk']]['fields']['candidate'] =  int(window[f"candidate_{i}"].get())
        data.candidate_issue_score[x['pk']]['fields']['issue_score'] = float(window[f"candidate_issue_score_{i}"].get())
        i += 1

    i = 0
    for x in data.get_running_mate_issue_score_for_issue(issue['pk']):
        data.running_mate_issue_score[x['pk']]['fields']['candidate'] =  int(window[f"running_mate_{i}"].get())
        data.running_mate_issue_score[x['pk']]['fields']['issue_score'] = float(window[f"running_mate_issue_score_{i}"].get())
        i += 1
    
def save_candidate():
    i = 0
    for x in data.get_state_multiplier_for_candidate(can_pk):
        data.candidate_state_multiplier[x['pk']]['fields']['state_multiplier'] = float(window[f"candidate_state_multiplier_{i}"].get())
        i += 1

def export_data(path):
    data.save_as_code_2(path)

def import_data(path):
    global window
    global data
    global state
    global can_pk
    global issue
    global current_mode
    global current_answers
    global layout
    global question

    data = load_data_from_file(path)
    current_answers = []
    question = data.questions[min(data.questions.keys())]
    state = None
    can_pk = None
    issue = None
    layout = create_question_layout(data, question, current_answers)
    new_window = sg.Window("Jet's TCT Mod Maker", layout, location=window.current_location(), size=window.size, resizable=True)
    window.close()
    window = new_window
    current_mode = "QUESTION"

# Create an event loop
while True:
    event, values = window.read()

    # End program if user closes window or
    # presses the OK button
    if event == "OK" or event == sg.WIN_CLOSED:
        break
    elif event == 'question_picker':
        save_current_workspace()
        current_answers = []
        new_question_pk = values['question_picker'][0]
        question = data.questions[new_question_pk]
        layout = create_question_layout(data, question, current_answers)
        new_window = sg.Window("Jet's TCT Mod Maker", layout, location=window.current_location(), size=window.size, resizable=True)
        window.close()
        window = new_window
        current_mode = "QUESTION"
    elif event == 'state_picker':
        save_current_workspace()
        new_state_pk = int(values['state_picker'][0].split(" -")[0])
        state = data.states[new_state_pk]
        layout = create_state_layout(data, state)
        new_window = sg.Window("Jet's TCT Mod Maker", layout, location=window.current_location(), size=window.size, resizable=True)
        window.close()
        window = new_window
        current_mode = "STATE"
    elif event == 'can_picker':
        save_current_workspace()
        can_pk = int(values['can_picker'][0])
        layout = create_candidate_layout(data, can_pk)
        new_window = sg.Window("Jet's TCT Mod Maker", layout, location=window.current_location(), size=window.size, resizable=True)
        window.close()
        window = new_window
        current_mode = "CAN"
    elif event == 'issue_picker':
        save_current_workspace()
        issue = data.issues[int(values['issue_picker'][0].split(" -")[0])]
        layout = create_issue_layout(data, issue)
        new_window = sg.Window("Jet's TCT Mod Maker", layout, location=window.current_location(), size=window.size, resizable=True)
        window.close()
        window = new_window
        current_mode = "ISSUE"
    elif event == "import2":
        import_data(values['import2'])
    elif event == "export2":
        print("export " + values['export2'])
        export_data(values['export2'])
    

window.close()