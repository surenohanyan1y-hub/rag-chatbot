# from flask import Flask, request, jsonify, send_from_directory
# from dotenv import load_dotenv
# from openai import OpenAI
# from supabase import create_client
# import os

# load_dotenv()
# # ֆունկիցա է  այս կոդը ընդունում է մեր gitignore ներսի գտվող տվյալները .env ֆիլը

# FIRST_SUPABASE_URL = os.environ.get("FIRST_SUPABASE_URL")
# FIRST_SUPABASE_SERVICE_ROLE_KEY = os.environ.get("FIRST_SUPABASE_SERVICE_ROLE_KEY")
# sb = create_client(FIRST_SUPABASE_URL, FIRST_SUPABASE_SERVICE_ROLE_KEY) 


# #այս գործողությունը աշխատում է հետևյալ կերպ ունենք 2 փոփողական  
# # SUPABASE և SU1PABASE_SERVICE_ROLE_KEY 1-ին ընդունում է օս աշխատում է օպերացիոն համակարգերի հետ, 
# # environ.get("SUPABASE_URL") ընդունում է մեր ստեղծված SUPABASE_URL
# # մյուսը ընդունում է ("SUPABASE_SERVICE_ROLE_KEY") 
# # sb = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY) նշանակում է այս գործողությունը միացնում է ընդանուր իրար
# # create_client. նշանակում է ստեղծիր հաճախորդ


# app = Flask(__name__, static_folder="public", static_url_path="")
# client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# # app = Flask(__name__, static_folder="public", static_url_path="")
# # ընդանուր առմամբ այս կոդը ընդունում է սարքում է ստատիկ ֆոլդեր և ընդունում մեր ստեղծված թղթապանակը և փողանցում ֆլասկին
# # client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
# # ստեղծիր OpenAI արեստական բանականություն և ցույց տուր մեզ մեր ապի բանալին

# SYSTEM_PROMPT = {
#     "role": "system",
#     "content": (
#         "You are an expert on all things related to the state of California. "
#         "You have deep knowledge of California history, geography, politics, "
#         "law, culture, climate, universities, technology, and local customs. "
#         "When answering questions, prioritize California-specific context, "
#         "examples, and accuracy."
#     )
# }
# # SYSTEM_PROMPT պատրաստում է մեզ համար  California մասնագետ  role և  content համակարգով
# # takes in the string and outputs a vector



# def embed_query(text: str) -> list[float]:
#     response = client.embeddings.create(
#         model="text-embedding-3-small",
#         input=text
#     )

#     return response.data[0].embedding
# # դեֆը ֆունկցիա է որը ընդունում է անուն պառամետր տեքստ անունով և զանգված լիստ float նշանակում է օրինակ 0.7 
# # responce ստեղծում է embeddings մոդել և տեքստ փողանցում ինֆորմացիան 
# # վերջում վերադարձ է անում դատան որը որ սկսվում է 0-ից ինդեքսը.
# # takes as input a query, conducts the search, returns context
# def semantic_search(query_text: str) -> list[dict]:
#     emb_q = embed_query(query_text)
#     res = sb.rpc("match_chunks", {"query_embedding": emb_q, "match_count" : 5}).execute()
#     rows = res.data or []
#     # for easier debugging
#     print("RAG OUTPUT:", rows)
#     return rows
# # semantic_searc ֆունկցիա որը ունի տեքստ պառամետր,  
# res = sb.rpc("match_chunks", {"query_embedding": emb_q, "match_count" : 5}).execute()
# # այս կոդը աշխատում է հետևյալ կերպ սբ մեր օպերացիոն համակարգը ճանաչում է մեր տվյալները rpc հրահանգի միջոցով
# # տրված է match_chunks անվանում  փողանցվել է նաև query_embedding և քանակը որը որ 5 է նշված որը ընդունում է execute ֆունկցիայի միջոցով


# @app.get("/")
# def index():
#     return send_from_directory("public", "index.html")
# # այս գործողությունը ընդունում է  public թղթապանակը իր ներսում գտնվող տվյալները index ֆունկցիյի միջոցով
# @app.post("/api/chat")
# def chat():
#     data = request.get_json(silent=True) or {}
#     # ունենք չատ ֆունկցիա որը կատարում է հետևալ քայլերը ունենք դատա որը request է անում մեր տվյալները ջսոնի տեսքով 
#     # օռ նշանակում է հակառակ դեպք հասկացողություն հառակակ դեպքում օբյեկտ
#     user_message = data.get("message", "")
#     # դատա նամակները ընդունելու համար
#     # conduct semantic search
#     rag_rows = semantic_search(user_message)
#     # ռագերը որոնման համար փողանցվել է     user_message 1
#     # fixes our formatting
#     context = "\n\n".join(
#         f"[Source {i+1} | sim={row.get('similarity'):.3f}]\n{row.get('content','')}"
#         for i, row in enumerate(rag_rows)
#     )
#     # կոնտեքստ ստեղծվել է միացնելու համար, "\n\n" 2 տող միացնում է իրար, join միացնում ենք իրար
#     # ֆ ֆոռմատավորում է  {i+1} ի 0 է սկսում բայց 1-ով ավելացնում ենք սկսվում է 1-ից.
#     # row.get('similarity'):.3f} 

#     # create the rag prompt
#     rag_message = {
#         "role": "system",
#         "content": (
#             "Use the retrieved context below to answer. If it doesn't contain the answer, say so. \n\n"
#             f"RETRIEVED CONTEXT:\n{context if context else '(no matches)'}"
#         )
#     }
#     # rag_message փողողական որի ներսում պատրաստված է օբյեկտ role system և content content զրուցում է թե ինչի մասին է կայքը եթե  If it doesn't contain the answer, say so 
#     # \n\n ավելացնում է 2 տող f ֆոռմատավորում է եթե  RETRIEVED CONTEXT այս տեքստը  :\n 1 տող context  հակառակ դեպքում   '(no matches)'


#     full_user_message = {
#         "role": "user",
#         "content": user_message,
#     }
#     # այս ոդը    full_user_message ընդանուր տեղակատվության մաար է 
#     # նախատեսված այն ամենը ինչ գրել ենք փողանցում ենք այս օբյեկտին
 

#     full_message = [rag_message, full_user_message, SYSTEM_PROMPT]
#    # full_message = [rag_message, full_user_message, SYSTEM_PROMPT] 
#     # այս օբյեկտը նախատեսված է մեր rag_message, full_user_message,SYSTEM_PROMPT փողանցելու համար ընդանուր 1 օբյեկտի ներսում, իսկ       
#     #  "role": "user",
#     #     "content": user_message, պատրաստում  1 ռոլ և content
#     resp = client.responses.create(
#         model="gpt-5-nano",
#         input=full_message
#     )
# #    return jsonify({"text": resp.output_text}) 
# #    այս կոդը ստեղծում է resp փոփողական,client.responses.create նշանակում է 
# #    ստեղծիր responses փողանցիր gpt-5-nano մոդելը և 
# #    ընդանուր տեղեկատվությունը full_message ինփուտ դաշտին հետո վերադարձ կատարիր ջսոն տեսքով 

# # Serves /styles.css, /app.js, etc.



# @app.get('/<path:path>')
# def serve_static(path):
#     return send_from_directory('public', path)

# if __name__ == '__main__':
#     app.run(debug=True)

# if __name__ == "__main__":
#     app.run(host="127.0.0.1", port=3000, debug=True)

# # @app.get("/<path:path>") 
# # այս կոդը 
# # գտնվում է թե որ թղթապանակի հետ է 
# # զրուցելու օրինակ /home հետո վերադարծ է անում պատրաստում է մեզ համար   
# # ուղարկել_է_տեղեկատուից ֆունկցիա որը ընդունում է մեր public թղթապանակը և path  
# # եթե անունը   "__main__" ապպա app.run եղիր ցույց տուր մեզ հասցեն և պորտը եթե debug true է ապպա կբացվի մեր սերվերը 
# # հտտպ խնթրանքով

# #     curl --request POST 'https://znwxkmyxrsdlgfgvwsvm.supabase.co/functions/v1/smart-task' \
# #   --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inpud3hrbXl4cnNkbGdmZ3Z3c3ZtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjgzODg1NTcsImV4cCI6MjA4Mzk2NDU1N30.7wHZ6N0kSuh76HlgfZ_bbkaLCgBvjl5REB9ZMdnpqSU' \
# #   --header 'Content-Type: application/json' 



from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv
from openai import OpenAI
from supabase import create_client
import os

# --------------------------------------------------
# Load environment variables
# --------------------------------------------------
load_dotenv()


FIRST_SUPABASE_URL = os.environ.get("FIRST_SUPABASE_URL")
FIRST_SUPABASE_SERVICE_ROLE_KEY = os.environ.get("FIRST_SUPABASE_SERVICE_ROLE_KEY")
sb = create_client(FIRST_SUPABASE_URL, FIRST_SUPABASE_SERVICE_ROLE_KEY) 


# --------------------------------------------------
# Clients
# --------------------------------------------------

client = OpenAI()

# --------------------------------------------------
# Flask app
# --------------------------------------------------
app = Flask(__name__, static_folder="public", static_url_path="")

# --------------------------------------------------
# System prompt
# --------------------------------------------------
SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "You are an expert on all things related to the state of California. "
        "You have deep knowledge of California history, geography, politics, "
        "law, culture, climate, universities, technology, and local customs. "
        "When answering questions, prioritize California-specific context, "
        "examples, and accuracy."
    )
}

# --------------------------------------------------
# Embedding function
# --------------------------------------------------
def embed_query(text: str) -> list[float]:
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

# --------------------------------------------------
# Semantic search (Supabase RPC)
# --------------------------------------------------
def semantic_search(query_text: str) -> list[dict]:
    emb_q = embed_query(query_text)

    res = sb.rpc(
        "match_chunks",
        {
            "query_embedding": emb_q,
            "match_count": 5
        }
    ).execute()

    rows = res.data or []
    print("RAG OUTPUT:", rows)
    return rows

# --------------------------------------------------
# Routes
# --------------------------------------------------
@app.get("/")
def index():
    return send_from_directory("public", "index.html")

@app.post("/api/chat")
def chat():
    data = request.get_json(silent=True) or {}
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"text": "Please provide a message."})

    # RAG search
    rag_rows = semantic_search(user_message)

    # Build context
    context = "\n\n".join(
        f"[Source {i+1} | sim={row.get('similarity', 0):.3f}]\n{row.get('content','')}"
        for i, row in enumerate(rag_rows)
    )

    rag_message = {
        "role": "system",
        "content": (
            "Use the retrieved context below to answer the user question. "
            "If the answer is not in the context, say you do not know.\n\n"
            f"RETRIEVED CONTEXT:\n{context if context else '(no matches)'}"
        )
    }

    messages = [
        SYSTEM_PROMPT,
        rag_message,
        {"role": "user", "content": user_message}
    ]

    resp = client.responses.create(
        model="gpt-5-nano",
        input=messages
    )

    return jsonify({"text": resp.output_text})

# --------------------------------------------------
# Static files (CSS / JS)
# --------------------------------------------------
@app.get("/<path:path>")
def serve_static(path):
    return send_from_directory("public", path)

# --------------------------------------------------
# Run server
# --------------------------------------------------
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=3000, debug=True)
