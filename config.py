import platform
import os

def is_windows():
    return platform.system() == "Windows"


project_directory = os.path.dirname(os.path.abspath(__file__))
# define the path to streamlit web app.py
streamlit_filepath_webapp = os.path.join(project_directory, "web_app", "app.py")

if is_windows():
    # define the path to streamlit.exe for windows
    streamlit_exe_filepath = os.path.join(project_directory, 'venv', 'Scripts', 'streamlit.exe')
else:
    # define the path to streamlit for Linux/MacOS
    streamlit_exe_filepath = os.path.join(project_directory, 'venv', 'bin', 'streamlit')

