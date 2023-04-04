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

    layout = [[sg.Column(col1, vertical_alignment="t"), sg.Column(col2, scrollable=True, vertical_scroll_only=True, expand_x=True,vertical_alignment="t")]]
    return layout