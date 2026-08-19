# AtlasKnowledge

**AtlasKnowledge is a Socratic AI tutoring engine designed for the Moroccan education system, from CE6 to 3AC.**

Unlike conventional LLM-based tutors that often provide complete solutions and little to no explanation, AtlasKnowledge is designed to guide students toward solutions through progressive hints, grade-specific explanations, questioning, and feedback.

The system combines:
- Grade-specific pedagogical prompting
- Socratic exercise guidance
- Curriculum grounding
- Conversational memory
- PDF input
- Multilingual interaction
- LaTeX rendering
- Anonymized pedagogical analytics for administrators

AtlasKnowledge is implemented entirely in Python using the Gemini API and Gradio.
## The Problem

Modern society has seen an invention that has changed the way we learn and think, and that invention is Artificial Intelligence. AI has affected the education sector greatly, where here in Morocco and the entire world, students use AI everyday for their studies, either for help, explanations or solutions. LLMs are great at solving problems, but this ability could undermine the students learning. Where a student asks for help and gets a direct solution instead of developing the method and cognitive ability to solve the problem. That's why I created AtlasKnowledge, which was designed thoroughly to make the LLM behave and act more like a tutor and teacher rather than an answer machine.

## What AtlasKnowledge Does

AtlasKnowledge is composed of two main system: the student system and the administrative system. For the students, it contains a variety of rich feature. Primarily its specialty in the Moroccan curriculum, grade specific behavior where it changes its explanation based on the level, Socratic questioning and exercise guidance which means that the engine actively questions the user and guides them using progressive hints instead of giving a direct solutions. It also includes detailed and easy to follow explanations, multilingual input and output, PDF input, LaTeX rendering when needed, conversational memory and real-world examples. AtlasKnowledge acts as a helper and teacher to the student, guiding them to the solution and developing their critical thinking skills. As for the administrative side, it features the ability to generate a comprehensive pedagogical report depending on the grade based on the students questions (Which are anonymized) to give the director a more clearer picture of the classrooms level.

## How AtlasKnowledge works

We will be using a diagram to give a clearer picture of the architecture works of AtlasKnowledge:

```mermaid
flowchart TD
    GradioInterface["Gradio Interface<br/>Student selects grade"]
    StudentInput["Student input"]
    GradeRouter["Grade Router"]
    GradeSpecificPrompts["Grade-Specific<br/>Prompts"]
    ConversationalMemory["Conversational<br/>Memory"]
    PromptAssembly["Prompt Assembly<br/>Student input + grade-specific prompts + conversational memory"]
    AIGeneration["AI Generation<br/>Gemini"]
    SocraticBoundaries["Specific Socratic<br/>boundaries"]
    StreamingOutput["Streaming Output<br/>+ LaTeX rendering"]

    GradioInterface --> StudentInput
    GradioInterface -->|Selected grade| GradeRouter
    GradeRouter --> GradeSpecificPrompts
    StudentInput --> PromptAssembly
    GradeSpecificPrompts --> PromptAssembly
    ConversationalMemory --> PromptAssembly
    PromptAssembly --> AIGeneration
    SocraticBoundaries -->|Constrains Gemini output| AIGeneration
    AIGeneration --> StreamingOutput

    classDef interfaceNode stroke:#4ade80,fill:#f0fdf4
    classDef processNode stroke:#818cf8,fill:#eef2ff
    classDef routingNode stroke:#facc15,fill:#fefce8
    classDef dataNode stroke:#22d3ee,fill:#ecfeff
    classDef constraintNode stroke:#f87171,fill:#fef2f2
    classDef outputNode stroke:#fb7185,fill:#fff1f2

    class GradioInterface,StudentInput interfaceNode
    class GradeRouter routingNode
    class GradeSpecificPrompts,ConversationalMemory dataNode
    class PromptAssembly,AIGeneration processNode
    class SocraticBoundaries constraintNode
    class StreamingOutput outputNode
```

This Flow chart visualizes how the system works. The student chooses his specific grade (CE6 to 3AC) one time, the system puts that in lock. then he inputs his specific question. when he sends the message, it is bundled with the recent conversation history and the specific prompt for the grade chosen and the master prompt that has the socratic boundaries needed for the engine. all of this content is then transferred to the Gemini API, and finally the AIs output is passed into a latex renderer which is then outputted to the user. The response is streamed progressively to the interface, reducing perceived latency and allowing the student to begin reading before the complete response has been generated.

## The Socratic Engine

The Socratic Engine is a core component of AtlasKnowledge, it is what distinguishes it from standard LLMs. To paint a clearer picture of the system, we will use two diagrams, one when the user asks a question or provides a solution, the other when they ask for an explanation

Diagram 1: Question or solution input from the user

```mermaid
flowchart TD
    Start(["Student asks a question<br/>or provides a solution"]) --> Assess{"Does the student need<br/>guidance?"}

    Assess -->|Yes| Hint["Provide a small hint"]
    Assess -->|No| Review["Review the student's solution"]

    Hint --> Attempt["Student attempts reasoning"]
    Attempt --> Stuck{"Is the student still stuck?"}

    Stuck -->|Yes| Clearer["Provide a clearer hint"]
    Stuck -->|No| Review

    Clearer --> Guidance["Give more explicit guidance"]
    Guidance --> Review

    Review --> Correct{"Is the solution correct?"}
    Correct -->|Yes| Complete(["Student reaches the solution"])
    Correct -->|Not yet| Feedback["Give targeted feedback"]
    Feedback --> Attempt

    classDef startEnd fill:#f0fdfa,stroke:#2dd4bf,stroke-width:2px
    classDef process fill:#eef2ff,stroke:#818cf8,stroke-width:2px
    classDef decision fill:#fefce8,stroke:#facc15,stroke-width:2px
    classDef feedback fill:#fff7ed,stroke:#fb923c,stroke-width:2px

    class Start,Complete startEnd
    class Hint,Attempt,Review,Guidance process
    class Assess,Stuck,Correct decision
    class Clearer,Feedback feedback
```

As we can observe, the LLM first asks itself if the student needs guidance, if yes, then it will give progressive hints until the student finds the solution. if not, in the case of inputting solutions, if it is wrong, it will give constructive feedback

Diagram 2: asking for an explanation 

```mermaid
flowchart TD
    A(["Student asks for explanation"]) --> B["Identify concept and grade"]
    B --> C["Grade is selected by the student"]
    C --> D["Retrieve grade-specific prompts"]
    D --> E["Adapt complexity to student's level"]
    E --> F["Explain concept"]
    F --> G["Use concrete, real-world examples for clearer understanding"]
    G --> H["Add a mini quiz or question to test understanding"]
    H --> I(["Student responds"])
    I --> J["Identify misunderstanding"]
    J --> K["Clarify or simplify"]
    K --> L{"Understanding demonstrated?"}
    L -->|No| H
    L -->|Yes| M(["Explanation complete"])

    classDef startEnd fill:#eef2ff,stroke:#818cf8,stroke-width:2px
    classDef preparation fill:#f0fdfa,stroke:#2dd4bf,stroke-width:2px
    classDef teaching fill:#fff7ed,stroke:#fb923c,stroke-width:2px
    classDef assessment fill:#f5f3ff,stroke:#a78bfa,stroke-width:2px
    classDef decision fill:#fefce8,stroke:#facc15,stroke-width:2px

    class A,I,M startEnd
    class B,C,D,E preparation
    class F,G teaching
    class H,J,K assessment
    class L decision
```

This flowchart demonstrates how AtlasKnowledge acts when the student wants an explanation, where it first adapts to the users grade, then explains thoroughly using useful examples, then adds at the end a small quiz or question to test the student, then it decides based on the answer given, whether to re explain more clearly or not.

## Curriculum adaptation

```mermaid
flowchart TD
    Student["Student"] --> GradeChoice{"Choose grade"}

    subgraph GradePrompts["Grade-specific prompts"]
        direction LR

        CE6["CE6"] --> PromptCE6["Simple explanations<br/>and many examples"]
        Grade1AC["1AC"] --> Prompt1AC["Easy-to-follow explanations<br/>bridging CE6's concrete, real-world lessons<br/>to 1AC's more abstract concepts"]
        Grade2AC["2AC"] --> Prompt2AC["More detailed explanations<br/>for profound comprehension"]
        Grade3AC["3AC"] --> Prompt3AC["Rigorous and detailed explanations<br/>to prepare for TC"]
    end

    GradeChoice -->|CE6| CE6
    GradeChoice -->|1AC| Grade1AC
    GradeChoice -->|2AC| Grade2AC
    GradeChoice -->|3AC| Grade3AC

    PromptCE6 --> Response["Gemini response"]
    Prompt1AC --> Response
    Prompt2AC --> Response
    Prompt3AC --> Response

    classDef student stroke:#818cf8,fill:#eef2ff
    classDef choice stroke:#2dd4bf,fill:#f0fdfa
    classDef grade stroke:#a78bfa,fill:#f5f3ff
    classDef prompt stroke:#38bdf8,fill:#ecfeff
    classDef output stroke:#fb923c,fill:#fff7ed
    classDef group stroke:#818cf8,fill:#eef2ff

    class Student student
    class GradeChoice choice
    class CE6,Grade1AC,Grade2AC,Grade3AC grade
    class PromptCE6,Prompt1AC,Prompt2AC,Prompt3AC prompt
    class Response output
    class GradePrompts group
```

AtlasKnowledge uses specific pedagogical prompts for each grade level to facilitate clearer comprehension. and for 3AC rigorous explanations and exercises are needed to build the needed cognitive ability for Tronc Commun (First year of high school in Morocco). We put strong guardrails in place to make sure the engine doesn't drift off and give explanations that are too advanced for the specific grade. The interaction is also variable across the grades, whereas AtlasKnowledge expects a 3AC student to know negative and positive number addition and subtraction and doesn't expect a CE6 pupil to know these concepts.

## Curriculum Grounding

AtlasKnowledge is curriculum grounded by the master prompts. We explicitly tell the engine in the system prompt to primarily bring its info from well known Moroccan educational websites like Alloschool, Dyrassa and Moutamadris. We have implemented this to make AtlasKnowledges response more familiar to the student. Since if you ask a standard LLM i.e "Explain Vectors" it may add complex concepts not taught in 2AC or 3AC, while our engine outputs (depending on the grade) the exact concepts taught in that level.

## API Architecture

AtlasKnowledge API key management technology to ensure stability of the engine. We will be using a diagram to detail the architecture of the system:

Diagram: API rotation Architecture:

```mermaid
flowchart LR
    apiKey1[API Key 1]
    apiKey2[API Key 2]
    apiKey3[API Key 3]
    apiKey4[API Key 4]
    apiKey5[API Key 5]
    keyRotation[Key rotation]

    apiKey1 --> keyRotation
    apiKey2 --> keyRotation
    apiKey3 --> keyRotation
    apiKey4 --> keyRotation
    apiKey5 --> keyRotation

    classDef apiKeyStyle stroke:#818cf8,fill:#eef2ff
    classDef processStyle stroke:#fb923c,fill:#fff7ed

    class apiKey1,apiKey2,apiKey3,apiKey4,apiKey5 apiKeyStyle
    class keyRotation processStyle
```

AtlasKnowledge selects randomly API keys to ensure maximum stability and availability and to improve resilience when individual keys face availability or usage constraints.

## PDF Interaction

AtlasKnowledge features PDF interaction where the student can upload a specific lesson or exercise to explain and to make the ideas clearer. We will be using a diagram to explain in detail the mechanics of this feature:

```mermaid
flowchart TD
    A[PDF Uploaded] --> B[Gemini Receives PDF]
    B --> C[Content Interpreted and Analyzed]
    C --> D[Grade-Specific Prompt Applied]
    D --> E{Socratic Tutoring Type}
    E -->|Explanation| F[Generate Detailed Explanation]
    E -->|Exercise| G[Create Problem-Solving Guidance]
    F --> H[Streaming Response]
    G --> H
    H --> I[Response Delivered to User]
    
    classDef input stroke:#818cf8,fill:#eef2ff
    classDef process stroke:#38bdf8,fill:#f0f9ff
    classDef decision stroke:#fb923c,fill:#fff7ed
    classDef output stroke:#4ade80,fill:#f0fdf4
    
    class A input
    class B,C,D process
    class E decision
    class F,G process
    class H,I output
```

The user uploads a PDF to the app, then its contents get interpreted and analyzed. After that the grade specific prompt (determined by the grade chosen) gets bundled with the contents of the PDF. Then the engine determines if it is an explanation or an exercise, after that it applies the socratic constraints and outputs the response as streaming content to the user.

## Design Principles

AtlasKnowledge was built around several core principles and values:

### 1. Guide, don't solve
The engine should help the student develop the reasoning required to reach a solution rather than immediately providing the final answer.

### 2. Teach at the student's level
Explanations, terminology, examples, and expected knowledge are adapted to the selected grade.

### 3. Stay within the curriculum
The engine is instructed to remain aligned with the concepts and methods expected at the student's level.

### 4. Encourage active participation
The student is repeatedly asked to reason, answer questions, and attempt intermediate steps.

### 5. Prefer transparency over automation
The system is designed as a tutoring assistant rather than a replacement for the teacher.

## Administration Mode:

AtlasKnowledge also features an administrative system as mentioned before. where the administration enters a specific protected password and chooses a grade. Then the users and a separate pedological report prompt gets bundled with the students anonymized data and gets sent to the engine which analyzes the data and outputs a comprehensive report including students most asked questions and confusing concepts, and advice to the professors and the administration of the school to paint a clearer picture of the educational state of the classroom.

## Tech Stack:

| Component           | Technology             |
| ------------------- | ---------------------- |
| Language            | Python                 |
| Interface           | Gradio                 |
| AI                  | Google Gemini API      |
| Mathematical output | LaTeX                  |
| Deployment          | Hugging Face Spaces    |
| Memory              | Conversational history |
| Document input      | Gemini PDF processing  |

- We chose python as the language for its compatibility with many AI libraries and the google-genai SDK.
- We implemented Gradio as the UI and UX for its focus on AI apps
- We used the Gemini API as the engine for its ability to process multimodal and multilingual inputs and its stability
- We deployed on HF spaces for the reliability of its servers
- We decided using native Gemini PDF processing feature to make the link between PDF input and the engine seamless.

## Project Architecture

AtlasKnowledge is divided into 5 main python files:

- main.py: this is the file that is responsible for grade routing and uses the aibrain.py functions to output the response which then is sent to app.py.
- app.py: this file is responsible for the UI/UX and to show the user the output generated by aibrain.py and passed through main.py.
- aibrain.py: Core engine responsible for API-key management, PDF processing, response generation, and administrative report generation.
- memory.py: it is responsible for saving the users question and the engines output as conversational history and it bundles the history with the master prompts from prompt.py to be given to aibrain.py.
- prompt.py: this file contains all the necessary prompts for each grade excluding the pedagogical prompt. it is imported to memory.py.
  
We chose this architecture to make debugging and implementing new features easier and faster.

## Development Story

Development started around 6 months ago, when I was myself a 3AC student, I wanted to create an AI tutor for Morocco to help myself and my classmates. 
So the first features implemented were the backend and the prompts. I started experimenting with different Gemini models and prompts, I landed on gemini 2.5 flash since it was cost effective and fast. At first, I made one single system prompt for all grades, but then I made multiple prompts, one for each grade for better personalization, and I added latex rendering too. After that I started researching for a python based UI framework for AI apps and I found Gradio. So I learnt the framework and implemented it to the system. Then I was brainstorming for new features, so I changed the prompts to be socratic, added API key rotation and the administrative system. then it was tested with around 5-10 of my classmates who returned positive feedback. It was also presented to multiple school directors, who reported that it is a good idea but that they want to return to traditional methods of schooling. It was deployed on hugging face spaces.

## Evaluation And Feedback

AtlasKnowledge was informally tested by approximately 5–10 students, who reported that the system was useful for studying and that its explanations and guided approach helped them work through problems. AtlasKnowledge was compared informally with Other LLMs (Gemini 3.0 flash, GPT model) with 15 questions covering middle school math, physics and SVT. It was observed that standard LLMs produced straight solutions to exercises, dry explanations, and advanced concepts. While AtlasKnowledge gave hints to students instead of solutions, easy to follow explanations and grade level concepts. However, it was noted that standard LLMs gave more detailed solutions and elegant proofs than AtlasKnowledge. It was presented to school directors who expressed interest but were more cautious about implementing it in their schools amid concerns about dependency of students on the tool.

## Limitations

Their are many limitations to AtlasKnowledge for example:

- Limited User Base
- no formal testing or educational study
- No verification of the engines mathematical solutions
- Dependence on external servers
- Rate limits
- curriculum grounding is based on the quality of the websites
- General stability problems.

In the future, we will aim to fix these problems and to make AtlasKnowledge more accessible and smarter.

## Future Roadmap

Near Term:
- The creation of a dataset focused with questions to benchmark formally with other LLMs
- Broader Student Testing
- Implementing model fallback system
- Implementing mathematical verification of the engines output

Far Term:
- Increasing UserBase to many schools
- Usage Analytics
- Improved Administrative Tools
- Additional  Moroccan Grades
- Account login and Database

Together, we could make AtlasKnowledge the tool that will help thousands of students across Morocco who don't have the resources to afford tutoring

## Thank You!

I would like to thank you immensely for your time and attention to this project, I welcome you to contribute to this project.

Author: Mohamed Amir Moutem
Email: amirmoutem19@gmail.com
Age: 15
Github: I think you already know :)
