from base import *
from ui import *
import PySimpleGUI as sg

sg.theme('SystemDefault')

data = load_data("json")
    
current_answers = []
question_pks = sorted(list(data.questions.keys()))
question = data.questions[question_pks[0]]

layout = create_question_layout(data, question, current_answers, question_pks)

# Create the window
window = sg.Window("Jet's TCT Mod Maker", layout, size=(1000,800))

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
        save_question()
        current_answers = []
        new_question_pk = values['question_picker'][0]
        question = data.questions[new_question_pk]
        layout = create_question_layout(data, question, current_answers, question_pks)
        new_window = sg.Window("Jet's TCT Mod Maker", layout, size=(1000,800))
        window.close()
        window = new_window
    elif event == "Save Question":
        save_question()

window.close()