import PySimpleGUI as sg

def create_question_layout(data, question, current_answers):
    col1 = create_pickers(data)

    if question == None:
        return [[sg.Column(col1)]]

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
        frame_ans = []
        current_answers.append(answer)
        frame_ans.append([sg.Text("Description")])
        frame_ans.append([sg.Multiline(default_text=answer['fields']['description'], size=(80, 5), key=f"description_ans{i}")])

        # add feedback
        j = 0
        for feedback in data.get_advisor_feedback_for_answer(answer['pk']):
            frame = []
            frame.append([sg.Text("Candidate")])
            frame.append([sg.Input(default_text=feedback['fields']['candidate'], key=f"candidate_ans{i}_feedback_{j}")])
            frame.append([sg.Text("Answer Feedback")])
            frame.append([sg.Multiline(default_text=feedback['fields']['answer_feedback'], size=(80, 5), key=f"description_ans{i}_feedback_{j}")])
            frame_ans.append([sg.Frame(f"Feedback PK {feedback['pk']}", frame)])
            j += 1

        # add global score
        j = 0
        for x in data.get_global_score_for_answer(answer['pk']):
            frame = []

            frame.append([sg.Text("Candidate PK")])
            frame.append([sg.Input(default_text=x['fields']['candidate'], key=f"ans{i}_global_score_candidate_{j}")])

            frame.append([sg.Text("Affected Candidate PK")])
            frame.append([sg.Input(default_text=x['fields']['affected_candidate'], key=f"ans{i}_global_score_affected_candidate_{j}")])

            frame.append([sg.Text("Global Multiplier")])
            frame.append([sg.Input(default_text=x['fields']['global_multiplier'], key=f"ans{i}_global_score_multiplier_{j}")])
            
            frame_ans.append([sg.Frame(f"Global Answer Score PK {x['pk']}", frame)])
            j += 1

        # add issue score
        j = 0
        for x in data.get_issue_score_for_answer(answer['pk']):
            frame = []

            frame.append([sg.Text("Issue PK")])
            frame.append([sg.Input(default_text=x['fields']['issue'], key=f"ans{i}_issue_score_issue_{j}")])

            frame.append([sg.Text("Issue Score")])
            frame.append([sg.Input(default_text=x['fields']['issue_score'], key=f"ans{i}_issue_score_issue_score_{j}")])

            frame.append([sg.Text("Issue Importance")])
            frame.append([sg.Input(default_text=x['fields']['issue_importance'], key=f"ans{i}_issue_score_issue_importance_{j}")])
            
            frame_ans.append([sg.Frame(f"Issue Answer Score PK {x['pk']}", frame)])
            j += 1

        # add state score
        j = 0
        for x in data.get_state_score_for_answer(answer['pk']):
            frame = []

            frame.append([sg.Text("State PK")])
            frame.append([sg.Input(default_text=x['fields']['state'], key=f"ans{i}_state_score_state_{j}")])

            frame.append([sg.Text("Candidate PK")])
            frame.append([sg.Input(default_text=x['fields']['candidate'], key=f"ans{i}_state_score_candidate_{j}")])

            frame.append([sg.Text("Affected Candidate PK")])
            frame.append([sg.Input(default_text=x['fields']['affected_candidate'], key=f"ans{i}_state_score_affected_candidate_{j}")])

            frame.append([sg.Text("State Multiplier")])
            frame.append([sg.Input(default_text=x['fields']['state_multiplier'], key=f"ans{i}_state_score_state_multiplier_{j}")])

            frame_ans.append([sg.Frame(f"Issue Answer Score PK {x['pk']}", frame)])
            j += 1

        i += 1

        col2.append([sg.Frame(f"Answer PK {answer['pk']}", frame_ans)])

    layout = [[sg.Column(col1, vertical_alignment="t"), sg.Column(col2, scrollable=True, vertical_scroll_only=True, expand_x=True, expand_y=True, vertical_alignment="t")]]
    return layout

def create_state_layout(data, state):
    col1 = create_pickers(data)

    col2 = [
        [sg.Text(f"{state['fields']['name']} (PK {state['pk']})", font=("Helvetica", 12, "bold"))],
        [sg.Text("Electoral Votes")],
        [sg.Input(default_text=state['fields']['electoral_votes'], key="electoral_votes")],
        [sg.Text("Popular Votes")],
        [sg.Input(default_text=state['fields']['popular_votes'], key="popular_votes")],
    ]

    i = 0
    for x in data.get_issue_score_for_state(state['pk']):

        frame = []

        frame.append([sg.Text("Issue PK")])
        frame.append([sg.Input(default_text=x['fields']['issue'], key=f"issue_issue_{i}")])

        frame.append([sg.Text("Candidate PK")])
        frame.append([sg.Input(default_text=x['fields']['state_issue_score'], key=f"issue_state_issue_score_{i}")])

        frame.append([sg.Text("Affected Candidate PK")])
        frame.append([sg.Input(default_text=x['fields']['weight'], key=f"issue_weight_{i}")])

        col2.append([sg.Frame(f"Statue Issue Score PK {x['pk']}", frame)])
        i += 1

    layout = [[sg.Column(col1, vertical_alignment="t"), sg.Column(col2, scrollable=True, vertical_scroll_only=True, expand_x=True, expand_y=True, vertical_alignment="t")]]
    return layout

def create_candidate_layout(data, candidate_pk):
    col1 = create_pickers(data)

    col2 = [
        [sg.Text(f"Candidate PK {candidate_pk}", font=("Helvetica", 12, "bold"))],
    ]

    candidate_state_multiplier_frame = []

    i = 0
    for x in data.get_state_multiplier_for_candidate(candidate_pk):

        frame = []

        state_name = data.states[x['fields']['state']]['fields']['name']

        frame.append([sg.Text(f"{state_name} Candidate State Multiplier", font=("Helvetica", 12, "bold"))])
        frame.append([sg.Input(default_text=x['fields']['state_multiplier'], key=f"candidate_state_multiplier_{i}")])

        candidate_state_multiplier_frame.append([sg.Frame(f"Candidate Issue Score PK {x['pk']}", frame)])
        i += 1

    col2.append([sg.Frame("Candidate State Multipliers", candidate_state_multiplier_frame)])

    layout = [[sg.Column(col1, vertical_alignment="t"), sg.Column(col2, vertical_scroll_only=True, scrollable=True, expand_x=True, expand_y=True, vertical_alignment="t")]]
    return layout

def create_issue_layout(data, issue):

    col1 = create_pickers(data)

    col2 = [
        [sg.Text(f"{issue['fields']['name']} (PK {issue['pk']})", font=("Helvetica", 12, "bold"))],
    ]

    frame = []

    frame.append([sg.Text("Issue Name", font=("Helvetica", 12, "bold"))])
    frame.append([sg.Input(default_text=issue['fields']['name'], key=f"issue_name")])

    for i in range(1, 8):
        frame.append([sg.Text(f"Stance {i}")])
        frame.append([sg.Input(default_text=issue['fields'][f'stance_{i}'], key=f"stance_{i}")])

    frame.append([sg.Text("Election")])
    frame.append([sg.Input(default_text=issue['fields']['election'], key=f"election")])

    col2.append([sg.Frame("Issue Settings", frame)])

    candidate_issue_score_frame = []

    i = 0
    for x in data.get_candidate_issue_score_for_issue(issue['pk']):
        frame = []

        frame.append([sg.Text("Candidate PK")])
        frame.append([sg.Input(default_text=x['fields']['candidate'], key=f"candidate_{i}")])

        frame.append([sg.Text("Issue Score")])
        frame.append([sg.Input(default_text=x['fields']['issue_score'], key=f"candidate_issue_score_{i}")])

        candidate_issue_score_frame.append([sg.Frame(f"Candidate Issue Score PK {x['pk']}", frame)])
        i += 1

    col2.append([sg.Frame("Candidate Issue Scores", candidate_issue_score_frame)])

    running_mate_issue_score_frame = []

    i = 0
    for x in data.get_running_mate_issue_score_for_issue(issue['pk']):
        frame = []

        frame.append([sg.Text("Candidate PK")])
        frame.append([sg.Input(default_text=x['fields']['candidate'], key=f"running_mate_{i}")])

        frame.append([sg.Text("Issue Score")])
        frame.append([sg.Input(default_text=x['fields']['issue_score'], key=f"running_mate_issue_score_{i}")])

        running_mate_issue_score_frame.append([sg.Frame(f"Running Mate Issue Score PK {x['pk']}", frame)])
        i += 1

    col2.append([sg.Frame("Running Mate Issue Scores", running_mate_issue_score_frame)])


    layout = [[sg.Column(col1, vertical_alignment="t"), sg.Column(col2, scrollable=True, vertical_scroll_only=True, expand_x=True, expand_y=True, vertical_alignment="t")]]
    return layout


def create_pickers(data):

    question_pks = sorted(list(data.questions.keys()))
    state_pks = [f"{s['pk']} - {s['fields']['abbr']}" for s in data.states.values()]
    candidate_pks = sorted(list(set([s['fields']['candidate'] for s in data.candidate_issue_score.values()])))
    issue_pks = [f"{s['pk']} - {s['fields']['name']}" for s in data.issues.values()]


    layout = [
    [sg.FolderBrowse(key="export2", button_text="Export Code 2", enable_events=True)],
    [sg.FileBrowse(key="import2", button_text="Import Code 2", enable_events=True)],
    [sg.Text("Questions", font=("Helvetica", 12, "bold"))],
    [sg.Listbox(values=question_pks, size=(10, 15), expand_y=True, expand_x=True, key="question_picker", enable_events=True)],
    [sg.Text("States", font=("Helvetica", 12, "bold"))],
    [sg.Listbox(values=state_pks, size=(10, 15), expand_y=True, expand_x=True, key="state_picker", enable_events=True)],
    [sg.Text("Issues", font=("Helvetica", 12, "bold"))],
    [sg.Listbox(values=issue_pks, size=(15, 5), expand_y=True, expand_x=True, key="issue_picker", enable_events=True)],
    [sg.Text("Candidates", font=("Helvetica", 12, "bold"))],
    [sg.Listbox(values=candidate_pks, size=(10, 5), expand_y=True, expand_x=True, key="can_picker", enable_events=True)]
    ]

    return layout