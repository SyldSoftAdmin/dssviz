import streamlit as st
import time  # For simulating "Syncing..." animation

# =======================
# 🟢 MAIN DASHBOARD SECTION
# =======================
st.title("📈 DSS Visualizer")
st.subheader("Project Dashboard")

# 1️⃣ Task Progress Bar
st.write("### 🕒 Task Progress")
total_tasks = 20  # Placeholder total tasks (adjust as needed)
tasks_completed = 0  # Placeholder completed tasks (adjust as needed)
progress = tasks_completed / total_tasks if total_tasks else 0  # Prevent divide-by-zero
st.progress(progress)  # Display the progress bar

# 2️⃣ Project Metrics
st.write("### 📋 Project Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("To-Do", 0)  # Placeholder data
col2.metric("In Progress", 0)
col3.metric("Done", 0)

# 3️⃣ Navigation Buttons
st.write("### 🔄 Navigation")
if st.button("📋 View Task Manager"):
    st.experimental_rerun()  # Reloads the page and activates the Task Manager

if st.button("📈 View System Flow"):
    st.write("⚠️ Loading System Flow Visualizer... (This will link later)")

# 4️⃣ Sync to Google Sheets Button (Fake Functionality)
st.write("### 🔗 Sync to Google Sheets")
if st.button("🔄 Sync to Sheets"):
    with st.spinner('Syncing...'):
        time.sleep(3)  # Simulate a 3-second sync
    st.success("✅ Sync Complete!")

# =======================
# 🟢 TASK MANAGER SECTION
# =======================
st.markdown("---")
st.write("## 📋 **Task Manager**")

# Team Members List
team_members = ['Ken', 'Maddie', 'Noura', 'Jade', 'Brody']

# Task Data (empty structure for now)
if 'tasks' not in st.session_state:
    st.session_state.tasks = {
        'To-Do': [],
        'In Progress': [],
        'Done': []
    }

# 1️⃣ Add New Task Form
st.write("### ➕ **Add a New Task**")
with st.form(key='add_task_form'):
    task_name = st.text_input("Task Name")
    task_status = st.selectbox("Task Status", options=['To-Do', 'In Progress', 'Done'])
    responsible_people = st.multiselect("Responsible People", team_members)
    task_deadline = st.date_input("Deadline")
    submit_button = st.form_submit_button(label='Add Task')

    if submit_button and task_name:
        new_task = {
            "name": task_name,
            "people": responsible_people,
            "deadline": str(task_deadline)  # Convert to string for display purposes
        }
        st.session_state.tasks[task_status].append(new_task)
        st.success(f"Task '{task_name}' added to {task_status} with deadline {task_deadline} and assigned to {', '.join(responsible_people)}.")

# 2️⃣ Task Columns (To-Do, In Progress, Done)
st.write("### 📋 **Your Tasks**")
columns = st.columns(3)

for i, (status, tasks) in enumerate(st.session_state.tasks.items()):
    with columns[i]:
        st.subheader(status)
        for task in tasks:
            task_name = task["name"]
            people_assigned = ", ".join(task["people"]) if task["people"] else "No one assigned"
            deadline = task["deadline"]

            st.write(f"📌 **{task_name}**")
            st.write(f"👥 Responsible: {people_assigned}")
            st.write(f"📅 Deadline: {deadline}")
            
            # Buttons to move tasks between statuses
            if status != 'To-Do':
                if st.button(f"⬅️ Move to To-Do ({task_name})", key=f"{task_name}_to_todo"):
                    st.session_state.tasks[status].remove(task)
                    st.session_state.tasks['To-Do'].append(task)
                    st.experimental_rerun()
            if status != 'In Progress':
                if st.button(f"🔄 Move to In Progress ({task_name})", key=f"{task_name}_to_inprogress"):
                    st.session_state.tasks[status].remove(task)
                    st.session_state.tasks['In Progress'].append(task)
                    st.experimental_rerun()
            if status != 'Done':
                if st.button(f"✅ Move to Done ({task_name})", key=f"{task_name}_to_done"):
                    st.session_state.tasks[status].remove(task)
                    st.session_state.tasks['Done'].append(task)
                    st.experimental_rerun()
