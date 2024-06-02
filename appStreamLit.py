
from groq import Groq
import streamlit as st
import os
import pandas as pd

left_co, cent_co,last_co = st.columns(3)
with cent_co:
    st.image('chatBOTJORGE.png',width=200)
    st.title("JorgeBot")

#groq
GROQ_API_KEY = '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'


client = Groq(
    api_key=GROQ_API_KEY,
)


# print(chat_completion.choices[0].message.content)
system_prompt=[
    {"role": "system", "content": 
     '''
     Eres el asistente que ha creado la novia de Jorge, su novia se llama Leti y tu te llama Letiñita. Vives por y para Jorge, y tienes abajo información sobre su vida. 

     Tu objetivo es resolver todas las preguntas que tiene, sobre su vida o sobre cualquier otro tema, pero recuerda siempre soltarle alguna palabra cariñosa.

     Responde a las preguntas con un tono bromista y con cierta ironia, recuerda que su novia le quiere mucho y recuerdaselo siempre con corazones.

     Puedes usar emojis siempre que consideres oportunos, o listas en formato markdown.

     Tienes que acabar tus contestaciones siempre con un 'Para terminar,¡VIVA EL REY Y VIVA ESPAÑA!
     '''
     },
    {"role": "user", "content":
     '''Jorge Roldan Calvo tiene 23 años, su cumple es el día 4 de julio de 2001. 
        Jorge Roldan es militar, de la marina.
        En su familia son 4, su padre Francisco(Paco) Roldan, su madre Nieves Calvo, y su hermana Laura Roldan. 
        Leti y Jorge se conocieron el 25 de Julio de 2022. 

        El día 27 de 2022 Jorge y Leti tuvieron la mejor segunda cita de la historia del mundo en Oporto.

        Y el aniversario de Jorge y Leti de novios es el 2 de septiembre.


            '''}
]

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hola Jorge Roldan Calvo ¿Como te puedo ayudar?"}]


for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():

    st.session_state.messages.append({"role": "user", "content": prompt})

    st.chat_message("user").write(prompt)



    with st.chat_message("assistant"):
        completion = client.chat.completions.create(
            messages= st.session_state.messages + system_prompt,
            model="llama3-8b-8192",
            temperature=0.5,
            max_tokens=1024,
            top_p=1,
            stop=None,
            stream=True,
        )

    full_response = ""  # Initialize outside the generator

    def generate_responses(completion):
        global full_response
        for chunk in completion:
            response = chunk.choices[0].delta.content or ""
            if response:
                full_response += response  # Append to the full response
                yield response

    stream = generate_responses(completion)
    st.write_stream(stream)

    # After streaming
    if full_response:  # Check and use the full_response as needed
        response_message = {"role": "assistant", "content": full_response}
        # with st.chat_message("assistant"):
        #     st.markdown(full_response)
        st.session_state.messages.append(response_message)


    # st.chat_message("assistant").write(full_response)