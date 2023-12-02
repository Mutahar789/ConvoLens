import streamlit as st
import extra_streamlit_components as stx
import streamlit_ext as ste

import util
import home
import search
import add
import review

HOST = 'http://localhost:24000'

st.set_page_config(page_title="ConvoLens", page_icon="ui/icon_black.png", layout="wide")
ste.set_width("75em")
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

col1, col2 = st.columns([0.1, 0.7], gap="large")
with col1:
    st.image("./ui/icon_white.png", width=90)
with col2:
    st.title("ConvoLens")

tab_id = stx.tab_bar(data=[
    stx.TabBarItemData(id="tab1", title="Home", description=""),
    stx.TabBarItemData(id="tab2", title="Search", description=""),
    stx.TabBarItemData(id="tab3", title="Add files", description=""),
    stx.TabBarItemData(id="tab4", title="Agent review", description="")
], default="tab1")

if tab_id == "tab1":
    st.session_state.tab_id = "tab1"
    home.render()
    
if tab_id == "tab2":
    if 'tab_id' not in st.session_state or st.session_state.tab_id != "tab2":
        st.session_state.search = False
        util.get_agents()
    st.session_state.tab_id = "tab2"
    search.render()

if tab_id == "tab3":
    st.session_state.tab_id = "tab3"
    add.render()

if tab_id == "tab4":
    if 'tab_id' not in st.session_state or st.session_state.tab_id != "tab4":
        util.get_agents()
    st.session_state.tab_id = "tab4"
    review.render()
