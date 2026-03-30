import aibrain

def atlas_app(userinput, selected_grade, pdf_file = None, history=[]):
    # Route based on level
    if selected_grade == "3AC":
        answer = aibrain.atlas3AC(userinput, pdf_file, history)
        for chunk in answer:
            yield chunk

    elif selected_grade == "2AC":
        answer = aibrain.atlasTC(userinput, pdf_file, history)
        for chunk in answer:
            yield chunk

    elif selected_grade == "1AC":
        answer = aibrain.atlas1BAC(userinput, pdf_file, history)
        for chunk in answer:
            yield chunk

    elif selected_grade == "CE6":
        answer = aibrain.atlas2BAC(userinput, pdf_file, history)
        for chunk in answer:
            yield chunk
    else:
        yield "Please select a valid level."
