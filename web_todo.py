import streamlit as st
import os
import functions_todo
from datetime import datetime, timedelta
from priority import Priority

# Define themes
themes = {
    "Light": "#FFFFFF",
    "Lavender": "#E6E6FA",
    "Green": "#CCFFCC",
    "Blue": "#CCE5FF"
}

# Add a selectbox for theme selection
selected_theme = st.sidebar.selectbox("Select Theme", list(themes.keys()))

# Add custom CSS to set the background color
st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {themes[selected_theme]};
    }}
    .clock {{
        position: fixed;
        top: 10px;
        right: 10px;
        font-size: 20px;
        color: #333;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Add a live clock to the corner of the web app
st.markdown(
    """
    <div class="clock" id="clock"></div>
    <script>
    function updateClock() {
        var now = new Date();
        var hours = now.getHours().toString().padStart(2, '0');
        var minutes = now.getMinutes().toString().padStart(2, '0');
        var seconds = now.getSeconds().toString().padStart(2, '0');
        var timeString = hours + ':' + minutes + ':' + seconds;
        document.getElementById('clock').innerHTML = timeString;
    }
    setInterval(updateClock, 1000);
    updateClock();
    </script>
    """,
    unsafe_allow_html=True
)
# get the tasks from the file
todos = functions_todo.get_todos()
priority_manager = Priority()

# Group tasks by priority
for todo in todos:
    priority = todo.get("priority", "High")  # Default to "High" if "priority" key is missing
    priority_manager.add_task(todo, priority)

# add the new tasks to the file
def add_todo():
    # get the task from the input using session_state which is a dictionary
    task = st.session_state["task"] + "\n"
    new_task = {"task": task, "priority": "High", "timestamp": datetime.now().isoformat()}
    todos.append(new_task)  # Default priority is High
    priority_manager.add_task(new_task, "Medium")
    functions_todo.write_todos(todos)

st.markdown("# <div style='text-align: center;'>Task Manager 📝</div>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Manage your day to day tasks</h3>", unsafe_allow_html=True)

if not os.path.exists("Todo.txt"):
    with open("Todo.txt", "w") as file:
        pass

# Display tasks in columns
for todo in todos:
    col1, col2 = st.columns([3, 2], border=True)
    with col1:
        checkbox = st.checkbox(todo["task"], key=todo["task"])
        if checkbox:
            todos.remove(todo)
            priority_manager.remove_task(todo)
            functions_todo.write_todos(todos)
            del st.session_state[todo["task"]]
            st.rerun()
    with col2:
        if f"priority_{todo['task']}" not in st.session_state:
            st.session_state[f"priority_{todo['task']}"] = todo["priority"]
        priority = st.selectbox("priority", ["High", "Medium", "Low"], key=f"priority_{todo['task']}")
        if priority != st.session_state[f"priority_{todo['task']}"]:
            st.session_state[f"priority_{todo['task']}"] = priority
            todo["priority"] = priority
            priority_manager.add_task(todo, priority)
            functions_todo.write_todos(todos)

# Display tasks grouped by priority in the sidebar
with st.sidebar:
    for priority, tasks in priority_manager.get_all_tasks().items():
        with st.expander(f"{priority} Priority Tasks ({len(tasks)})"):
            for todo in tasks:
                st.checkbox(todo["task"], key=f"{priority}_{todo['task']}")

# Check for high priority tasks added within the last hour
current_time = datetime.now()
for todo in todos:
    if todo["priority"] == "High":
        # Convert the timestamp to datetime object
        task_time = datetime.fromisoformat(todo["timestamp"])
        if current_time - task_time <= timedelta(hours=1):
            st.warning(f"Reminder: High priority task '{todo['task']}' was added within the last hour!")

st.text_input(label="", placeholder="Enter your task below", type='default', on_change=add_todo, key="task")
