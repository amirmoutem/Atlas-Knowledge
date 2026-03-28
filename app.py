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
    # 2. Add an EMPTY Assistant message for the stream to fill
        history.append({"role": "assistant", "content": limit})
        yield history, history, ""
        return
    user_usage[client_ip] += 1
    # 1. Add User message to history immediately
    history.append({"role": "user", "content": str(user_input)})
    # 2. Add an EMPTY Assistant message for the stream to fill
    history.append({"role": "assistant", "content": ""})

    try:
       
        
        
        for chunk in atlas_app(user_input, level, pdf_file):
            history[-1]["content"] = chunk
            
            # Yield the history so the UI updates word-by-word
            yield history, history, ""
            
        # 5. Log it ONLY after the loop is finished
        log_student_question(level, user_input)

    except Exception as e:
        history[-1]["content"] = f"Error: {str(e)}"
        yield history, history, ""


def handle_director_dashboard(level, password):
    if password == "ExcellenceX": 
        # Loop to handle the streaming report
        for chunk in aibrain.get_pedagogical_report(level):
            yield chunk
    else:
        yield "## ❌ Accès Refusé\nLe mot de passe est incorrect. Veuillez contacter l'administrateur d'Atlas Knowledge."

theme1 = gr.themes.Soft(
    primary_hue="cyan", # The "Neon" glow
    secondary_hue="slate", # Professional dark gray
    neutral_hue="slate", # Dark background
).set(
    body_background_fill="*neutral_950", # Deep black/blue background
    block_background_fill="*neutral_900",
    block_border_width="1px",
    button_primary_background_fill="*primary_500",
    button_primary_text_color="white",
)
with gr.Blocks() as demo:
    gr.Markdown("## Upload a pdf file")
    file = gr.File(label="Upload PDF", file_types=[".pdf"])
    level_state = gr.State(value=None)
    history = gr.State(value=[])

    dropdown = gr.Dropdown(
        ["Niveau","CE6", "1AC", "2AC", "3AC"],
        label="Choose your level"
    )

    chatbot = gr.Chatbot(render_markdown=True, latex_delimiters=[{"left": "$$", "right": "$$", "display": True}, {"left": "$", "right": "$", "display": False}
                                                                 ]
                                                                 )  # no type argument

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
        grade_input = gr.Dropdown(["Niveau","CE6", "1AC", "2AC", "3AC"], label="Classe")
        # Ensure type="password" so the characters are hidden while typing
        pass_input = gr.Textbox(label="Code d'accès", type="password") 
    
    gen_btn = gr.Button("Générer le Rapport Stratégique", variant="primary")
    output_markdown = gr.Markdown()

    # THE CONNECTION
    gen_btn.click(
        fn=handle_director_dashboard, 
        inputs=[grade_input, pass_input], # Both inputs are sent to the function
        outputs=output_markdown
    )

demo.launch(share=True,
theme=theme1,)