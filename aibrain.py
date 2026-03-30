import os
import random
from google import genai
import memory
# List of all your keys from environment variables
API_KEYS = [
    os.getenv("KEY1"),
    os.getenv("KEY2"),
    os.getenv("KEY3"),
    os.getenv("KEY4"),
    os.getenv("KEY5")
]

# REMOVE the global client = genai.Client(...) line

def get_random_client():
    """Picks a random key to spread the load across all 5 quotas."""
    selected_key = random.choice([k for k in API_KEYS if k]) # Filters out empty keys
    return genai.Client(api_key=selected_key)

# 🔹 Helper function (avoids repeating code)
def generate_response(prompt, pdf_file=None):
    if not prompt:
        yield "Please enter your question"
    try:
     if pdf_file is not None:
        with open (pdf_file, "rb") as f:
            pdf_bytes = f.read()
        model1 = "gemini-2.5-flash"
        client = get_random_client()
        response = client.models.generate_content_stream(model=model1, contents=[prompt, types.Part.from_bytes(data=pdf_bytes, mime_type="application/pdf")])
        partial_message = ""
        for chunk in response:
            partial_message += chunk.text
            yield partial_message
     else:
        model1 = "gemini-2.5-flash"
        client = get_random_client()
        response = client.models.generate_content_stream(model=model1, contents=prompt)
        partial_message=""
        for chunk in response:
            partial_message += chunk.text
            yield partial_message
    except Exception as e:
        yield f"Error: {str(e)}"

# 🔵 3AC
def atlas3AC(userinput, pdf_file=None, history=[]):
    prompt = memory.memory3AC(history) + "\nUser: " + userinput
    for chunk in generate_response(prompt, pdf_file):
        yield chunk

# 🟢 TC
def atlasTC(userinput, pdf_file=None, history=[]):
    prompt = memory.memoryTC(history) + "\nUser: " + userinput
    for chunk in generate_response(prompt, pdf_file):
        yield chunk

# 🟡 1BAC
def atlas1BAC(userinput, pdf_file=None, history=[]):
    prompt = memory.memory1BAC(history) + "\nUser: " + userinput
    for chunk in generate_response(prompt, pdf_file):
        yield chunk

# 🔴 2BAC
def atlas2BAC(userinput, pdf_file=None, history=[]):
    prompt = memory.memory2BAC(history) + "\nUser: " + userinput
    for chunk in generate_response(prompt, pdf_file):
        yield chunk

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
        Voici les questions posées par les élèves de {selected_grade}, N'ecris pas la date, et n'ecris pas [Votre nom] dans le sans le nom. soit concret avec votre reponse:
        soit professional et donne juste le rapport, n'explique pas les questions donné par les eleves avant le rapport. donne directement le rapport à destination de la direction, Faites votre rapport en se basant par ces questions posée par les étudiants.
        {logs}
        
        Rédige un rapport structuré pour la direction de l'école :
        - TOP 3 des sujets les plus complexes 
        - Analyse des blocages types.
        - Conseil stratégique pour le prochain cours.
        - Recommendation à destination du corps professoral.
        - Un plan hebdomadaire (3 Semaines) sur comment soigner les blocages des eleves pour chaque des TOP trois sujets.
        """

        for chunk in generate_response(director_prompt, None):
            yield chunk

    except Exception as e:
        yield f"Erreur lors de la génération du rapport : {str(e)}"
