from prompt import prompt3AC, prompt1BAC, prompt2BAC, promptTC

conversation = []
def add_user(msg):
  conversation.append("User: "+ msg)
def add_ai(msg):
   conversation.append("Assistant: "+ msg)
def memory3AC():
 full_prompt3AC = prompt3AC + "\n".join(conversation)
 return full_prompt3AC
def memoryTC():
 full_promptTC = promptTC + "\n".join(conversation)
 return full_promptTC
def memory1BAC():
 full_prompt1BAC = prompt1BAC + "\n".join(conversation)
 return full_prompt1BAC
def memory2BAC():
 full_prompt2BAC = prompt2BAC + "\n".join(conversation)
 return full_prompt2BAC