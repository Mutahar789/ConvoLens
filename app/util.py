import streamlit as st
from database import database

OPENAI_API_KEY = "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"

db = database.pgvector()

def tooltip(heading, tooltip):
    return st.markdown(
    f"""
        <style>
            /* Tooltip container */
            .tooltip {{
                position: relative;
                display: inline-block;
                cursor: help;
                font-weight: bold;
                font-size: 14px;
            }}

            /* Tooltip text */
            .tooltip .tooltiptext {{
                visibility: hidden;
                width: 200px;
                background-color: #333;
                color: #fff;
                text-align: center;
                border-radius: 6px;
                padding: 5px;
                position: absolute;
                z-index: 1;
                bottom: 125%;
                left: 50%;
                opacity: 0;
                transition: opacity 0.3s;
            }}

            /* Tooltip container:hover */
            .tooltip:hover .tooltiptext {{
                visibility: visible;
                opacity: 1;
            }}
        </style>
        <div class="tooltip">
            <strong> {heading} </strong>
            <span class="tooltiptext">{tooltip}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

def get_agents():
    query = '''SELECT DISTINCT csr_id FROM audios;'''
    agents = db.select(query, ())
    st.session_state.agents = [agent['csr_id'] for agent in agents]
