import gradio as gr
from main import atlas_app
import aibrain

user_usage = {}
MAX_MESSAGES = 15

def log_student_question(level, message):
    snake_level = str(level).replace(",", "_")
    filename = f"log_{snake_level}.txt"
    with open(filename, "a", encoding="utf-8") as file:
        file.write(f"-{message}\n") 

def set_level(level):
    return level, gr.update(visible=False)

def chat(user_input, history, level, pdf_file, request: gr.Request):
    if history is None:
        history = []
       
    if level == "Niveau":
        yield history, history, ""
    client_ip = request.client.host
    if client_ip not in user_usage:
        user_usage[client_ip]=0
    if user_usage[client_ip] >= MAX_MESSAGES:
        limit = "Vous avez fini votre max de questions du jour, veuillez reviser le matériel."
        history.append({"role": "user", "content": str(user_input)})
        history.append({"role": "assistant", "content": limit})
        yield history, history, ""
        return
    user_usage[client_ip] += 1
    
    history.append({"role": "user", "content": str(user_input)})
    history.append({"role": "assistant", "content": ""})

    try:
        # THE FIX: Added 'history' to the function call below
        for chunk in atlas_app(user_input, level, pdf_file, history):
            history[-1]["content"] = chunk
            yield history, history, ""
            
        log_student_question(level, user_input)

    except Exception as e:
        history[-1]["content"] = f"Error: {str(e)}"
        yield history, history, ""


def handle_director_dashboard(level, password):
    if password == "ExcellenceX": 
        for chunk in aibrain.get_pedagogical_report(level):
            yield chunk
    else:
        yield "## ❌ Accès Refusé\nLe mot de passe est incorrect. Veuillez contacter l'administrateur d'Atlas Knowledge."

theme1 = gr.themes.Soft(
    primary_hue="cyan", 
    secondary_hue="slate", 
    neutral_hue="slate", 
).set(
    body_background_fill="*neutral_950", 
    block_background_fill="*neutral_900",
    block_border_width="1px",
    button_primary_background_fill="*primary_500",
    button_primary_text_color="white",
    body_text_color="*neutral_50",
    block_label_text_color="*neutral_50",
    body_text_color_subdued="*neutral_300",
)

with gr.Blocks(title="AtlasKnowledge: Infrastructure IA Pédagogique | Atlantis") as demo:
    gr.Markdown("""
    # 🏛️ AtlasKnowledge
    **Infrastructure IA Pédagogique Officielle**
    """)
    gr.Markdown("## Upload a pdf file")
    file = gr.File(label="Upload PDF", file_types=[".pdf"])
    level_state = gr.State(value=None)
    history = gr.State(value=[])

    dropdown = gr.Dropdown(
        ["Niveau","3AC", "2AC", "1AC", "CE6"],
        label="Choose your level"
    )

    chatbot = gr.Chatbot(render_markdown=True, latex_delimiters=[{"left": "$$", "right": "$$", "display": True}, {"left": "$", "right": "$", "display": False}])

    textbox = gr.Textbox(
        placeholder="Type your message here...",
        show_label=False
    )

    dropdown.change(
        fn=set_level,
        inputs=dropdown,
        outputs=[level_state, dropdown]
    )

    textbox.submit(
        fn=chat,
        inputs=[textbox, chatbot, level_state, file],
        outputs=[chatbot, chatbot, textbox]
    )
    with gr.Accordion("🔒 Espace Direction", open=False):
     with gr.Row():
        grade_input = gr.Dropdown(["Niveau","3AC", "2AC", "1AC", "CE6"], label="Classe")
        pass_input = gr.Textbox(label="Code d'accès", type="password") 
    
    gen_btn = gr.Button("Générer le Rapport Stratégique", variant="primary")
    output_markdown = gr.Markdown()

    gen_btn.click(
        fn=handle_director_dashboard, 
        inputs=[grade_input, pass_input], 
        outputs=output_markdown
    )

demo.launch(theme=theme1)
