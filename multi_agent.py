from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv
from openai import OpenAI
from supabase import create_client

import os



load_dotenv()
# ֆունկիցա է  այս կոդը ընդունում է մեր gitignore ներսի գտնվող տվյալները .env ֆիլը

FIRST_SUPABASE_URL=os.environ.get("FIRST_SUPABASE_URL")
FIRST_SUPABASE_SERVICE_ROLE_KEY=os.environ.get("FIRST_SUPABASE_SERVICE_ROLE_KEY")
sb2 = create_client(FIRST_SUPABASE_URL, FIRST_SUPABASE_SERVICE_ROLE_KEY)

SECOND_SUPABASE_URL = os.environ.get("SUPABASE_URL")
SECOND_SUPABASE_SERVICE_ROLE_KEY=os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
sb1 = create_client(SECOND_SUPABASE_URL , SECOND_SUPABASE_SERVICE_ROLE_KEY)

client = OpenAI() 



SYSTEM_PROMPT_ONE = {
    "role": "system",
    "content": (
        "What is programming and where can I start my career? I'm interested, what advice would you give?"
        "I restarted my career with Frontend because I wanted to clearly understand what web programming is. \n Since I chose this field, I felt it was important to first understand how UI and UX work. After that, \n "
        "I plan to move to server-side development. Another reason is that knowing JavaScript helps expand your way of thinking over time. Programming teaches us by making mistakes, especially through code errors, and that process helps us grow as developers."
        "1. Yes, this is normal, because in the early stages we cannot fully remember and manage our code. Mistakes happen almost all the time, and it is through these mistakes that we learn and grow as developers."
        "2.  Yes, you are correct. HTML and CSS are not considered programming languages. HTML stands for HyperText Markup Language and is used to create the structure of web pages. \n CSS is a Cascading Style Sheets language that is used to style and design websites. Learning usually starts with HTML because it forms the foundation of web platforms."
        "3. JavaScript is a dynamic programming language. It is used not only for web platforms but also for building desktop and mobile applications. In many cases, web development starts with JavaScript. It is a flexible language, and its syntax is relatively easy to understand."
        "Sure! Here’s the English version of what you wrote: Yes, **it helps**, but there is an important point. If we only use **vibe coding**  \n in a question-and-answer format, it doesn’t really count as actual programming. It can provide very useful assistance, such as examples, explanations, and ideas, but the **main thing is to write code on your own**, try solutions in practice, so you can truly develop and become more professional in the programming world.  "
        "I can also make a **shorter, more concise version** that’s easier to use as a direct answer if you want."
        "Sure! Here’s the English version of your answer, keeping the meaning clear and natural: Actually, no, that is not enough. **Vibe coding** is \n\n"
        "just a question-and-answer tool that can help a programmer to some extent. It is not a separate programming profession, because you are simply given code as examples or solutions. The main thing is that you need to **work on the code yourself**, make modifications," "and create your own version in order to truly become a programmer. If you want, I can also make a **shorter, smoother version** that sounds even more natural for a Q&A conversation."
    )
}
# SYSTEM_PROMPT_ONE պատրաստում է մեզ համար  ծրագրավորման մասնագետ հարց պատասխան  role և  content համակարգով
# takes in the string and outputs a vector

SYSTEM_PROMPT_TWO = {
    "role": "system",
    "content": (
        "Actually, programming as a professional is a great understanding in my opinion,"
        "As a beginner, I would recommend starting with web programming, \n\n as it is one of the most popular fields for beginners.  Web programming is divided into two parts:  Frontend and Backend. The frontend developer works on the visible part of the website," 
        "known as UI and UX, while the backend handles the invisible part, \n such as the server, database, and system logic. This part can be considered the backstage of the website."

        "For a beginner, which is easier to start with, Frontend or Backend, and why? Which one would you recommend?"
        
        "1.If your code has errors and, at the beginning, you cannot manage everything properly, is that normal or not?" 
        "2.I have heard that there are HTML and CSS languages. Are they considered programming languages or not, especially since most courses start by teaching HTML and CSS?"
        "3.What kind of language is JavaScript, and what is its role in web programming?"
        "4.I have heard that many people use vibe coding through a question-and-answer approach. Does this actually help programmers or not?"
        "5.If I only learn vibe coding, can I become a programmer, or is that not enough?"
    )
}
# SYSTEM_PROMPT_TWO պատրաստում է մեզ համար  սկսնակ ծրագրավորող    role և  content համակարգով
# takes in the string and outputs a vector




def embed_query(text: str) -> list[float]:
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )

    return response.data[0].embedding
# դեֆը ֆունկցիա է որը ընդունում է անուն պառամետր տեքստ անունով և զանգված լիստ float նշանակում է օրինակ 0.7 
# responce ստեղծում է embeddings մոդել և տեքստ փողանցում ինֆորմացիան 
# վերջում վերադարձ է անում դատան որը որ սկսվում է 0-ից ինդեքսը.
# takes as input a query, conducts the search, returns context
def semantic_search(query_text, sb) -> list[dict]:
    emb_q = embed_query(query_text)
    res = sb.rpc("match_chunks", {"query_embedding": emb_q, "match_count" : 5}).execute()
    rows = res.data or []
    # for easier debugging
   
    return rows
# semantic_searc ֆունկցիա որը ունի տեքստ պառամետր,  




def run_bot(user_message, system_prompt, sb_client) -> str:

    # conduct semantic search
    rag_rows = semantic_search(user_message, sb_client)

    # fixes our formatting
    context = "\n\n".join(
        f"[Source {i+1} | sim={row.get('similarity'):.3f}]\n{row.get('content','')}"
        for i, row in enumerate(rag_rows)
    )

    # create the rag prompt
    rag_message = {
        "role": "system",
        "content": (
            "Use the retrieved context below to answer. If it doesn't contain the answer, say so. \n\n"
            f"RETRIEVED CONTEXT:\n{context if context else '(no matches)'}"
        ) }

    # call the openai api
    full_user_message = {
        "role": "user",
        "content": (user_message),
    }

    full_message = [rag_message, full_user_message, system_prompt]

    print(system_prompt)


    resp = client.responses.create(
        model="gpt-5-nano",
        input=full_message
    )

      # return the output
    return resp.output_text
  

# runs chatbot one
def narek_the_great(user_message):
    return run_bot(user_message, SYSTEM_PROMPT_ONE, sb1)

# runs chatbot two
def irina_the_awesome(user_message):
    return run_bot(user_message, SYSTEM_PROMPT_TWO, sb2)

# run a conversation between chatbot one and chatbot two
def simulation():
    # contain the output at any given time
    output = narek_the_great("Ask a question about something that interests you.")
    print("NAREK SAYS:" + output)

    for _ in range(5):
        output = irina_the_awesome(output)
        print("IRINA SAYS:" + output)

        output = narek_the_great(output)
        print("NAREK SAYS:" + output)

if __name__ == "__main__":
    simulation()
