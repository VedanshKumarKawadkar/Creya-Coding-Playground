from numpy.lib.function_base import place
import streamlit as st
#from streamlit.state.session_state import Value
from streamlit_ace import st_ace, THEMES
import time
def funv():
    ...

def editorApp():
        st_ace(placeholder="aa")
        editor, params = st.beta_columns([3, 1])
        params.subheader("Parameters")

        with editor:
            content = st_ace(
                placeholder = "Write your code here",
                language = params.selectbox("Select Language", options=["Plain Text", "Python", "C++"], index=2),
                theme = params.selectbox("Theme", options=THEMES, index=35),
                font_size = params.slider("Font Size", 12, 24, 14),
                tab_size= params.slider("Tab Size", 2, 8, 4),
                wrap = params.checkbox("Wrap Enabled", value=False),
                auto_update = params.checkbox("Auto Update", value=False),
                min_lines = 45
            )

import requests

gfg_compiler_api_endpoint = "https://ide.geeksforgeeks.org/main.php"
languages = ['C', 'Cpp', 'Cpp14', 'Java', 'Python', 'Python3', 'Scala', 'Php', 'Perl', 'Csharp']


def gfg_compile(lang, code, _input=None, save=False):
    data = {
      'lang': lang,
      'code': code,
      'input': _input,
      'save': save
    }
    r = requests.post(gfg_compiler_api_endpoint, data=data)
    return r.json()


if __name__ == "__main__":
    lang = 'Python'
    code = """print(123123)
    """
    _input = "1 5"
    res = (gfg_compile(lang, code, _input))
 
    sid = res['sid']
    print(sid)
    
    response_api = "https://ide.geeksforgeeks.org/submissionResult.php"
    s = {
        "sid" : sid,
        "requestType" : "fetchResults"
    }
    time.sleep(10)
    d = requests.post(response_api, data=s)
    d = d.json()
    print(d)
    print(d['output'])
    print(d['time'])
    print(d['memory'])
