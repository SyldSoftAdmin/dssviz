import streamlit as st
import time  # For simulating "Syncing..." animation

# =======================
# 🟢 MAIN DASHBOARD SECTION
# =======================
st.set_page_config(page_title="DSS Visualizer", layout="wide")  # Corporate layout (wide screen)
st.title("DSS Visualizer")
st.markdown("#### Project Tracking Dashboard")
st.markdown("---")

# Initialize tasks in session state if not present
if 'tasks' not in st.session_state:
    st.session_state.tasks = {
        'To-Do': [],
        'In Progress': [],
        'Done': []
    }

# 1️⃣ Task Progress Bar
st.markdown("### Task Progress")
total_tasks = sum(len(tasks) for tasks in st.session_state['tasks'].values())
tasks_completed = len(st.session_state['tasks']['Done'])
progress = tasks_completed / total_tasks if total_tasks else 0  # Prevent divide-by-zero
st.progress(progress)  # Display the progress bar

# 2️⃣ Project Metrics (Cleaned Up)
st.markdown("### Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("To-Do", len(st.session_state['tasks']['To-Do']))
col2.metric("In Progress", len(st.session_state['tasks']['In Progress']))
col3.metric("Done", len(st.session_state['tasks']['Done']))

# 3️⃣ Navigation Buttons (More Corporate)
st.markdown("---")
st.markdown("### Navigation")
col1, col2 = st.columns(2)
with col1:
    if st.button("Task Management"):
        st.rerun()  # Reloads the page and activates the Task Manager

with col2:
    if st.button("System Flow"):
        st.write("⚠️ This feature is under development.")

# 4️⃣ Sync to Google Sheets Button (More Subtle)
st.markdown("---")
st.markdown("### Sync Data to Google Sheets")
if st.button("Sync Now"):
    with st.spinner('Syncing...'):
        time.sleep(3)  # Simulate a 3-second sync
    st.success("Data successfully synced to Google Sheets.")

# =======================
# 🟢 TASK MANAGER SECTION
# =======================
st.markdown("---")
st.markdown("## Task Management")

# Team Members List
team_members = ['Ken', 'Maddie', 'Noura', 'Jade', 'Brody']

# 1️⃣ Add New Task Form
st.markdown("### Add a New Task")
with st.form(key='add_task_form'):
    task_name = st.text_input("Task Name", placeholder="Enter task title here")
    task_status = st.selectbox("Task Status", options=['To-Do', 'In Progress', 'Done'])
    responsible_people = st.multiselect("Responsible People", team_members)
    task_deadline = st.date_input("Deadline")
    submit_button = st.form_submit_button(label='Add Task')

    if submit_button and task_name:
        new_task = {"name": task_name, "people": responsible_people, "deadline": str(task_deadline)}  # Convert date to string
        st.session_state.tasks[task_status].append(new_task)
        st.success(f"Task '{task_name}' added to {task_status}.")

# 2️⃣ Task Columns (Corporate Layout)
st.markdown("### Your Tasks")
columns = st.columns(3)

for i, (status, tasks) in enumerate(st.session_state.tasks.items()):
    with columns[i]:
        st.markdown(f"#### {status}")  # Status as a clean header
        for task in tasks:
            task_name = task["name"]
            people_assigned = ", ".join(task["people"]) if task["people"] else "No one assigned"
            deadline = task["deadline"]

            # Task card layout
            st.markdown(f"""
                <div style="border: 1px solid #e0e0e0; border-radius: 5px; padding: 10px; margin-bottom: 10px;">
                    <strong>{task_name}</strong><br>
                    <small>👥 {people_assigned}</small><br>
                    <small>📅 {deadline}</small>
                </div>
            """, unsafe_allow_html=True)

            # Move buttons (compact layout)
            col1, col2, col3 = st.columns(3)
            if status != 'To-Do':
                if col1.button("To-Do", key=f"todo_{task_name}"):
                    st.session_state.tasks[status].remove(task)
                    st.session_state.tasks['To-Do'].append(task)
                    st.rerun()
            if status != 'In Progress':
                if col2.button("In Progress", key=f"inprogress_{task_name}"):
                    st.session_state.tasks[status].remove(task)
                    st.session_state.tasks['In Progress'].append(task)
                    st.rerun()
            if status != 'Done':
                if col3.button("Done", key=f"done_{task_name}"):
                    st.session_state.tasks[status].remove(task)
                    st.session_state.tasks['Done'].append(task)
                    st.rerun()
