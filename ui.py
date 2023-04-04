import PySimpleGUI as sg

def create_question_layout(data, question, current_answers, question_pks):
    col1 = create_pickers(data, question_pks)

    col2 = [
        [sg.Text(f"Question PK {question['pk']}", font=("Helvetica", 12, "bold"))],
        [sg.Text("Priority")],
        [sg.Input(default_text=question['fields']['priority'], key="priority")],
        [sg.Text("Description")],
        [sg.Multiline(default_text=question['fields']['description'], size=(80,5), key="description")],
        [sg.Text("Likelihood")],
        [sg.Input(default_text=question['fields']['likelihood'], key="likelihood")],
        [sg.Text("Answers", font=("Helvetica", 12, "bold"))]
    ]

    i = 0

    for answer in data.get_answers_for_question(question['pk']):
        col_ans = []
        current_answers.append(answer)
        col_ans.append([sg.Text("Description")])
        col_ans.append([sg.Multiline(default_text=answer['fields']['description'], size=(80, 5), key=f"description_ans{i}")])

        j = 0
        for feedback in data.get_advisor_feedback_for_answer(answer['pk']):
            col = []
            col.append([sg.Text("Candidate")])
            col.append([sg.Input(default_text=feedback['fields']['candidate'], key=f"candidate_ans{i}_feedback_{j}")])
            col.append([sg.Text("Answer Feedback")])
            col.append([sg.Multiline(default_text=feedback['fields']['answer_feedback'], size=(80, 5), key=f"description_ans{i}_feedback_{j}")])
            col_ans.append([sg.Frame(f"Feedback PK {feedback['pk']}", col)])
            j += 1
        i += 1

        col2.append([sg.Frame(f"Answer PK {answer['pk']}", col_ans)])

    col2.append([sg.Button("Save Changes", key="Save Question")])

    layout = [[sg.Column(col1, vertical_alignment="t"), sg.Column(col2, scrollable=True, vertical_scroll_only=True, expand_x=True, expand_y=True, vertical_alignment="t")]]
    return layout

def create_state_layout(data, state, question_pks):
    col1 = create_pickers(data, question_pks)

    col2 = [
        [sg.Text(f"{state['fields']['name']} (PK {state['pk']})", font=("Helvetica", 12, "bold"))],
        [sg.Text("Electoral Votes")],
        [sg.Input(default_text=state['fields']['electoral_votes'], key="electoral_votes")],
        [sg.Text("Popular Votes")],
        [sg.Input(default_text=state['fields']['popular_votes'], key="popular_votes")],

    ]


    layout = [[sg.Column(col1, vertical_alignment="t"), sg.Column(col2, scrollable=True, vertical_scroll_only=True, expand_x=True, expand_y=True, vertical_alignment="t")]]
    return layout

def create_pickers(data, question_pks):
    state_pks = [f"{s['pk']} - {s['fields']['abbr']}" for s in data.states.values()]

    layout = [
    [sg.Text("Questions", font=("Helvetica", 12, "bold"))],
    [sg.Listbox(values=question_pks, size=(10, 20), expand_y=True, expand_x=True, key="question_picker", enable_events=True)],
    [sg.Text("States", font=("Helvetica", 12, "bold"))],
    [sg.Listbox(values=state_pks, size=(10, 20), expand_y=True, expand_x=True, key="state_picker", enable_events=True)]
    ]

    return layout