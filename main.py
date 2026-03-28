import aibrain
from memory import add_user

def atlas_app(userinput, selected_grade, pdf_file = None):
    # Save user message (optional)
    add_user(userinput)

    # Route based on level
    if selected_grade == "3AC":
        answer = aibrain.atlas3AC(userinput, pdf_file)
        for chunk in answer:
            yield chunk

    elif selected_grade == "TC":
        answer = aibrain.atlasTC(userinput, pdf_file)
        for chunk in answer:
            yield chunk

    elif selected_grade == "1BAC":
        answer = aibrain.atlas1BAC(userinput, pdf_file)
        for chunk in answer:
            yield chunk

    elif selected_grade == "2BAC":
        answer = aibrain.atlas2BAC(userinput, pdf_file)
        for chunk in answer:
            yield chunk

    return "Please select a valid level."