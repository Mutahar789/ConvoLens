import streamlit as st
import pandas as pd

from database import database
from embeddings import embeddings_model
import util

db = database.pgvector()

def mapping(arg):
    dict_map = {
        "None selected": "",
        "Yes": "True",
        "No": "False"
    }
    if dict_map.get(arg) !=None:
        return dict_map.get(arg)
    else:
        return arg
    
map_bool_to_str = {True: "Yes", False: "No"}

@st.cache_data
def get_embedding(query_str):
    return embeddings_model.embed_query(query_str)

def search(data, query_str):
    conditions = []
    values = []
    for k,v in data.items():
        if v != "":
            conditions.append(f'{k} = %s')
            values.append(v)

    query = """
        SELECT id, customer_id, csr_id, customer_satisfied, query_resolved, unprofessional_csr, call_purpose, user_qoi, customer_mood_change, transcript, audio_path 
        FROM audios
        WHERE 1=1
    """
    
    if conditions:
        query += "AND " + "AND ".join(conditions)
    if query_str != "":
        emb_vector = get_embedding(query_str)
        query += f" ORDER BY embedding <#> '{emb_vector}'"

    rows = db.select(query, values)
    return rows    

def display(results):
    for index, result in enumerate(results[:st.session_state.counter]):
        with st.expander(f"**Call # {result['id']}**"):

            st.audio(result['audio_path'])
            toggle = st.toggle("Show transcript", False, key=f"toggle_1_{index}")
            if toggle:            
                transcript = result['transcript'].replace('\n', '\n\n')
                transcript = transcript.replace('Customer:', ':red[Customer]:')
                transcript = transcript.replace('CSR:', ':blue[CSR]:')
                st.markdown(f"""**Transcript:** \n\n {transcript}""")

            df = pd.DataFrame({
                "Customer": [result['customer_id']],
                "Agent": [result['csr_id']],
                "Customer Satisfied": map_bool_to_str[result['customer_satisfied']],
                "Query Resolved": map_bool_to_str[result['query_resolved']],
                "Unprofessional Agent Behavior": map_bool_to_str[result['unprofessional_csr']],
                "Customer Quality of Interaction: 1 (Poor) - 10 (Excellent)": str([result['user_qoi']][0]),
                "Purpose of call": [result['call_purpose']]
            })
            df = df.melt(var_name="Variable", value_name="Value")
            st.dataframe(df, hide_index=True,column_config=None, use_container_width=True)

    if len(results) > st.session_state.counter:
        view_more = st.button("View more results")
        if view_more:
            st.session_state.counter = min(len(results), st.session_state.counter+5)
            view_more = False
            st.experimental_rerun()

def render():
    error = False
    
    util.tooltip(
        heading="Find Related:", 
        tooltip="Enter your search query here, and the system will find related audio calls based on the context."
    )
    query_str = st.text_input('Find Related', max_chars=256, label_visibility="collapsed")

    col1, col2 = st.columns(2)
    with col1:
        util.tooltip("Call ID:", "Specify the unique Call ID to look up a specific call.")
        call_id = st.text_input('**Call ID**:', label_visibility="collapsed")
        
        util.tooltip("Customer Satisfied:", "Filter calls by customer satisfaction.")
        customer_satisfied = mapping(st.selectbox("Customer Satisfied:", ["None selected", "Yes", "No"], label_visibility="collapsed"))
        
        util.tooltip("Customer Mood After Call:", "Filter calls based on the change in the customer's mood after the call.")
        customer_mood_change = mapping(st.selectbox("**Customer mood after call**:", ["None selected", "No change in the mood", "Customer left in a worse mood", "Customer left in a better mood"], label_visibility="collapsed"))

    with col2:
        agents = ["None selected"]
        agents.extend(st.session_state.agents)
        util.tooltip("Agent:", "Select an agent to filter calls associated with a specific agent.")
        csr_id = mapping(st.selectbox('Agent:', agents, label_visibility="collapsed"))
        
        util.tooltip("Query Resolved:", "Filter calls by query resolution.")
        query_resolved = mapping(st.selectbox("**Query Resolved**:", ["None selected", "Yes", "No"], label_visibility="collapsed"))

        util.tooltip("Unprofessional Agent:", "Filter calls for unprofessional agent behaviour.")
        unprofessional_csr = mapping(st.selectbox("Unprofessional agent:", ["None selected", "Yes", "No"], label_visibility="collapsed"))
    
    util.tooltip("Customer Quality of Interaction:", "Specify the customer quality of interaction on a scale of 1 (Poor) to 10 (Excellent). Use the slider to set the value or check 'Any' for any quality.")
    option = st.checkbox("Any", True)
    user_qoi = st.slider("slider", 1, 10, 5, disabled=(option==True), label_visibility="collapsed")
    if option == True:
        user_qoi = ""
    else:
        user_qoi = str(user_qoi)

    search_button = st.button("Search", type="primary", disabled=error)
    if search_button:
        st.session_state.search = True
        if "counter" in st.session_state:
            del st.session_state.counter
    
    clear_results = st.button("Clear search results")
    if clear_results:
        st.session_state.search = False

    if 'search' in st.session_state and st.session_state.search:
        search_data = {
            "id": call_id,
            "csr_id": csr_id,
            "customer_satisfied": customer_satisfied,
            "unprofessional_csr": unprofessional_csr,
            "query_resolved": query_resolved,
            "customer_mood_change": customer_mood_change,
            "user_qoi": user_qoi
        }
        results = search(search_data, query_str)

        if len(results) == 0:
            st.info("No search results found!")
        else:
            st.info(f"{len(results)} results found!")
            st.divider()

            if "counter" not in st.session_state or st.session_state.counter < 10:
                st.session_state.counter = min(len(results), 10)
            display(results)
