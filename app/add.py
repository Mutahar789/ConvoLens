import streamlit as st
import time

import analysis
from database import database
from embeddings import embeddings_model

db = database.pgvector()

mapping = {
    "Yes": True,
    "No": False,
    "N/A": False
}

def process_file(filepath):
    csr_id = filepath.split("_")[-2]
    customer_id = filepath.split("_")[-1][:-4]

    raw_transcription = analysis.get_transcription(filepath)
    transcription = analysis.get_script(raw_transcription)
    features = analysis.get_features(transcription)

    row = {
        'customer_id': customer_id,
        'csr_id': csr_id,
        'customer_satisfied': mapping[features['Customer Satisfied']],
        'query_resolved': mapping[features['Query Resolved']],
        'unprofessional_csr': mapping[features['Unprofessional CSR']],
        'call_purpose': features['Call Purpose'],
        'user_qoi': int(features['Quality of User Interaction']),
        'customer_mood_change': features['Customer Emotion Progression'],
        'transcript': transcription,
        'audio_path': filepath,
        'embedding': embeddings_model.embed_query(transcription)
    }
    db.insert(row)

def render():
    with st.form("form", clear_on_submit=True):
        files = st.file_uploader("Upload", type=["wav"], accept_multiple_files=True, label_visibility="collapsed")
        upload = st.form_submit_button("Upload files", type="primary")
        placeholder = st.empty()
        total = len(files)
        done = 0
        error = False
        if total!= 0 and upload:
            placeholder.empty()
            progress = st.progress(done/total, text=f"{done}/{total}")
            with st.spinner("Processing your files..."):
                while len(files) != 0:
                    try:
                        progress.progress(done/total,  text=f"{done}/{total}")
                        
                        timestamp = int(time.time())
                        uploaded_file = files[0]
                        bytes_data = uploaded_file.getvalue()
                        csr_id = uploaded_file.name.split("_")[-2]
                        customer_id = uploaded_file.name.split("_")[-1][:-4]
                        filepath = f"./audio_files/{timestamp}_{csr_id}_{customer_id}.wav"

                        with open(filepath, "wb") as file:
                            file.write(bytes_data)

                        process_file(filepath)

                        files.pop(0)
                        done += 1

                    except:
                        error = True                            
                        break

            progress.empty()
            with placeholder:
                if error:
                    st.error("Invalid filename format. Please use the following format: <timestamp>_<agent_id>_<customer_id>.wav")
                else:
                    st.info("Done!")


                
