import streamlit as st
import requests
import assemblyai as aai

# AssemblyAI API key (replace with your actual API key)
ASSEMBLYAI_API_KEY = "your_api_key"

def aai_transcribe(audio_file, language):
    aai.settings.api_key = ASSEMBLYAI_API_KEY

    transcriber = aai.Transcriber()

    # You can use a local filepath:
    # audio_file = "./example.mp3"

    config = aai.TranscriptionConfig(speaker_labels=True,language_code=language, speech_model=aai.SpeechModel.best)

    transcript = transcriber.transcribe(audio_file, config)

    if transcript.status == aai.TranscriptStatus.error:
        return(f"Transcription failed: {transcript.error}")
        #exit(1)

    #return(transcript.text)

    result = ""
    for utterance in transcript.utterances:
        result += f"{utterance.speaker} : {utterance.text}\n"
    
    return(result)


# Streamlit app UI
st.title("Meeting Transcription App")
st.write("Upload an audio file to generate a transcript of the meeting.")

# File upload
uploaded_file = st.file_uploader("Choose an audio file", type=["mp3", "wav", "m4a"])

if uploaded_file is not None:
    st.audio(uploaded_file, format="audio/wav")
    language = st.selectbox("Select language", ["en", "fr"])
    # Generate transcript button
    if st.button("Generate Transcript"):
        with st.spinner("Transcribing audio... this may take a moment."):
            transcript = aai_transcribe(uploaded_file, language)
            if transcript:
                st.success("Transcription completed!")
                st.text_area("Meeting Transcript", transcript, height=400)

                if st.download_button(label="Download Transcript", data=transcript, file_name="transcript.txt", mime="text/plain"):
                    st.success("Transcript ready for download")
