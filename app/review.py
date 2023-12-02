import streamlit as st
from database import database
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

db = database.pgvector()

config = {'displayModeBar': False}

def render():
    col1, col2 = st.columns(2)
    with col1:
        agent_id = st.selectbox('**Agent:**', st.session_state.agents)

    query = """SELECT customer_satisfied, query_resolved, unprofessional_csr, user_qoi, customer_mood_change
    FROM audios
    WHERE csr_id = %s;
    """
    rows = db.select(query, (agent_id, ))
    total = len(rows)
    df = pd.DataFrame(rows)
    customer_sat_rate = ((df['customer_satisfied']==True).sum()/total)*100
    query_resol_rate = ((df['query_resolved']==True).sum()/total)*100
    unprofessional_behav = ((df['unprofessional_csr']==True).sum()/total)*100
    avg_user_qoi = (df['user_qoi']).sum()/total
    customer_mood = dict(df["customer_mood_change"].value_counts()/total)

    x_values = ["Customer satisfaction rate", "Query resolve rate", "Unprofessional conduct"]
    y_values = [customer_sat_rate, query_resol_rate, unprofessional_behav]
    fig = px.bar(x=x_values, y=y_values, title="Agent Performance Metrics")
    fig.update_xaxes(title_text="", tickfont=dict(size=18))
    fig.update_yaxes(title_text="Percentage", range=[0,100], title_font=dict(size=18), tickfont=dict(size=14))
    rounded_values = [f"{round(value, 1)}%" for value in y_values]
    fig.update_traces(
        text=rounded_values,
        textposition='inside',
        marker_color=["green", "blue", "red"],
        textfont=dict(size=16)
    )
    fig.update_layout(hovermode=False)
    st.plotly_chart(fig, theme="streamlit", use_container_width=True, config=config)

    fig = px.pie(values=customer_mood.values(), names=customer_mood.keys(), title="Customer sentiment shift")
    fig.update_traces(pull=[0.025, 0.025, 0.025], textfont=dict(size=16))
    fig.update_layout(legend=dict(font=dict(size=14)), hovermode=False)
    st.plotly_chart(fig, theme="streamlit", use_container_width=True, config=config)


    fig = go.Figure()
    
    fig.add_trace(
        go.Heatmap(
            z=[[0.01*p for p in range(11)]],
            y=[1],
            colorscale="RdYlGn",
            showscale=False
        )
    )

    x_pointer = avg_user_qoi
    fig.add_trace(
        go.Scatter(
            x=[x_pointer],
            y=[5],
            mode="markers+text",
            marker=dict(symbol="triangle-down", size=25, color="white"),
            showlegend=False,
            text=[f"   {str(round(x_pointer, 1))}"],
            textposition="middle right",
            textfont=dict(size=18, color="white")
        )
    )

    fig.update_layout(
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=True),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        height=220,
        title="Average customer quality of interaction",
        hovermode=False
    )
    
    fig.update_xaxes(range=[1, 10])

    st.plotly_chart(fig, theme="streamlit", use_container_width=True, config=config)