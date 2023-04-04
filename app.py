from base import *
from ui import *
import PySimpleGUI as sg

sg.theme('SystemDefault')

data = load_data("json")
    
current_answers = []
question_pks = sorted(list(data.questions.keys()))
question = data.questions[question_pks[0]]
state = None

layout = create_question_layout(data, question, current_answers, question_pks)

# Create the window
window = sg.Window("Jet's TCT Mod Maker", layout, size=(1000,800), resizable=True)

current_mode = "QUESTION"

def save_current_workspace():
    if current_mode == "QUESTION":
        save_question()
    elif current_mode == "STATE":
        save_state()

def save_state():
    pk = state['pk']
    data.states[pk]['fields']['electoral_votes'] = int(window['electoral_votes'].get())
    data.states[pk]['fields']['popular_votes'] = int(window['popular_votes'].get())

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
        i += 1

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
        layout = create_question_layout(data, question, current_answers, question_pks)
        new_window = sg.Window("Jet's TCT Mod Maker", layout, size=(1000,800), location=window.current_location(), resizable=True)
        window.close()
        window = new_window
        current_mode = "QUESTION"
    elif event == 'state_picker':
        save_current_workspace()
        new_state_pk = int(values['state_picker'][0].split(" -")[0])
        state = data.states[new_state_pk]
        layout = create_state_layout(data, state, question_pks)
        new_window = sg.Window("Jet's TCT Mod Maker", layout, size=(1000,800), location=window.current_location(), resizable=True)
        window.close()
        window = new_window
        current_mode = "STATE"

window.close()