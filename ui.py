import PySimpleGUI as sg

def create_question_layout(data, question, current_answers, question_pks):
    col1 = [
    [sg.Text("Questions", font=("Helvetica", 12, "bold"))],
    [sg.Listbox(values=question_pks, size=(10, 20), expand_y=True, expand_x=True, key="question_picker", enable_events=True)]
    ]

    col2 = [
        [sg.Text(f"Question PK {question['pk']}", font=("Helvetica", 12, "bold"))],
        [sg.Text("Priority")],
        [sg.Input(default_text=question['fields']['priority'], key="priority")],
        [sg.Text("Description")],
        [sg.Multiline(default_text=question['fields']['description'], size=(80,5), key="description")],
        [sg.Text("Likelihood")],
        [sg.Input(default_text=question['fields']['likelihood'], key="likelihood")]
    ]

    i = 0
    for answer in data.get_answers_for_question(question['pk']):
        current_answers.append(answer)
        col2.append([sg.Text(f"Answer PK {answer['pk']}", font=("Helvetica", 12, "bold"))])
        col2.append([sg.Text("Description")])
        col2.append([sg.Multiline(default_text=answer['fields']['description'], size=(80, 5), key=f"description_ans{i}")])
        i += 1

    col2.append([sg.Button("Save Changes", key="Save Question")])

    layout = [[sg.Column(col1, vertical_alignment="t"), sg.Column(col2)]]
    return layout