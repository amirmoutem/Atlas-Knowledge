from google import genai
from google.genai import types
import memory
import os

# Secure API key (set this in your environment)
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# 🔹 Helper function (avoids repeating code)
def generate_response(prompt, pdf_file=None):
    if not prompt:
        yield "Please enter your question"
    try:
     if pdf_file is not None:
        with open (pdf_file, "rb") as f:
            pdf_bytes = f.read()
        model1 = "gemini-2.5-flash"
        response = client.models.generate_content_stream(model=model1, contents=[prompt, types.Part.from_bytes(data=pdf_bytes, mime_type="application/pdf")])
        partial_message = ""
        for chunk in response:
            partial_message += chunk.text
            yield partial_message
     else:
        model1 = "gemini-2.5-flash"
        response = client.models.generate_content_stream(model=model1, contents=prompt)
        partial_message=""
        for chunk in response:
            partial_message += chunk.text
            yield partial_message
    except Exception as e:
        yield f"Error: {str(e)}"

# 🔵 3AC
def atlas3AC(userinput, pdf_file=None):
    prompt = memory.memory3AC() + "\nUser: " + userinput
    
    final_answer = ""
    # We loop through the generator to get the actual text
    for chunk in generate_response(prompt, pdf_file):
        final_answer = chunk
        yield chunk # Send the text to the screen
        
    # ONLY save to memory after the loop is finished
    memory.add_ai(final_answer)

# 🟢 TC
def atlasTC(userinput, pdf_file=None):
    prompt = memory.memoryTC() + "\nUser: " + userinput

    final_answer = ""
    for chunk in generate_response(prompt, pdf_file):
        final_answer = chunk
        yield chunk

    memory.add_ai(final_answer)

# 🟡 1BAC
def atlas1BAC(userinput, pdf_file=None):
    prompt = memory.memory1BAC() + "\nUser: " + userinput

    final_answer = ""
    for chunk in generate_response(prompt, pdf_file):
        final_answer = chunk
        yield chunk

    memory.add_ai(final_answer)

# 🔴 2BAC
def atlas2BAC(userinput, pdf_file=None):
    prompt = memory.memory2BAC() + "\nUser: " + userinput

    final_answer = ""
    for chunk in generate_response(prompt, pdf_file):
        final_answer = chunk
        yield chunk

    memory.add_ai(final_answer)

def get_pedagogical_report(selected_grade):
    """
    Reads the logs and generates an AI summary for the Director.
    """
    if not selected_grade:
        yield "Erreur : Aucun niveau sélectionné."
        return

    safe_level = str(selected_grade).replace(" ", "_")
    filename = f"log_{safe_level}.txt"

    if not os.path.exists(filename):
        yield f"Aucune donnée disponible pour {selected_grade} (Fichier introuvable)."
        return

    try:
        with open(filename, "r", encoding="utf-8") as f:
            logs = f.read().strip()
        
        if not logs:
            yield f"Le journal pour {selected_grade} est actuellement vide."
            return

        director_prompt = f"""
        Tu es un expert en ingénierie pédagogique au Maroc. 
        Voici les questions posées par les élèves de {selected_grade} :
        
        {logs}
        
        Rédige un rapport structuré pour la direction de l'école :
        - TOP 3 des sujets les plus complexes.
        - Analyse des blocages types.
        - Conseil stratégique pour le prochain cours.
        """

        # Loop through the generator so the Markdown output streams properly!
        for chunk in generate_response(director_prompt, None):
            yield chunk

    except Exception as e:
        yield f"Erreur lors de la génération du rapport : {str(e)}"

