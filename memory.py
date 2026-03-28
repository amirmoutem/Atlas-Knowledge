from prompt import prompt3AC, prompt1BAC, prompt2BAC, promptTC

def format_history(history):
    conv = []
    if history:
        # Skip the last 2 items (the current question & empty assistant box added by app.py)
        for msg in history[:-2]: 
            if msg["role"] == "user":
                conv.append("User: " + str(msg["content"]))
            elif msg["role"] == "assistant" and msg["content"]:
                conv.append("Assistant: " + str(msg["content"]))
    return "\n".join(conv)

def memory3AC(history):
    return prompt2BAC + "\n" + format_history(history)

def memoryTC(history):
    return prompt1BAC + "\n" + format_history(history)

def memory1BAC(history):
    return promptTC + "\n" + format_history(history)

def memory2BAC(history):
    return prompt3AC + "\n" + format_history(history)
