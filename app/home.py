import streamlit as st

def render():
    
    st.header("ConvoLens - Your Call Center Superpower!")

    st.write("Discover the ultimate tool for call centers, where every conversation becomes a source of power. ConvoLens empowers you to transform your customer interactions, turning data into valuable insights.")
    st.image("ui/superhero_agent.png", use_column_width=True)

    # Section 1
    st.header("Unleash the Power of Insights")

    st.subheader("Crystal Clear Analysis")
    st.image("ui/analysis.jpg", use_column_width=True)
    st.write("Dive deep into customer interactions to find those moments that matter, ensuring satisfaction every time. Unlock the potential of your team by identifying the stars and guiding the underperformers. Track the satisfaction of your customers, ensuring their journey with you is a delightful one.")

    st.subheader("Smart Search")
    st.write("Leverage advanced embeddings and vector cosine similarity search to uncover hidden gems in your audio database. Find relevant conversations with ease, whether it's a topic, sentence, or keyword.")

    st.subheader("Effortless Insights")
    st.write("Easily navigate and explore your data with our intuitive, user-friendly dashboard.")

    # Section 2
    st.header("Stay Ahead with ConvoLens")
    st.image("ui/happy_customer.png", use_column_width=True)
    st.write("Experience the future of call center management with ConvoLens. Harness the power of data, gain valuable insights, and elevate your customer service to new heights.")
