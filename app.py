import os
import streamlit as st
import concurrent.futures

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

from langchain_community.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

def gen_reply(query="", context=""):
    model_name = "gpt-3.5-turbo"
    chat = ChatOpenAI(model_name=model_name, temperature=0)
    question = f"""
    Sei un chatbot esperto di Marketing. Rispondi a questa domanda in modo breve e preciso. 
    Domanda: {query}
    """
    response = chat([HumanMessage(content=question)]).content
    return response

# Streamlit app
def main():
    st.title("Analisi di Mercato")
    
    # User inputs
    mercato = st.text_input("Mercato di interesse")
    paese = st.text_input("Paese di interesse")
    
    if st.button("Esegui Analisi"):
        if mercato and paese:
            # Questions to be asked
            questions = [
                f"Panoramica generale di 30 parole sul mercato del {mercato} nel paese {paese}",
                f"Descrizione del mercato del {mercato} e dati quantitativi nel paese {paese}",
                f"Qual è la tendenza e i tassi di crescita del mercato del {mercato} nel paese {paese}",
                f"Cosa cercano potenziali clienti su google per mercato del {mercato} nel paese {paese}",
                f"Cosa cercano su fb/pinterest per mercato del {mercato} nel paese {paese}",
                f"Quali sono i possibili buyer persona per mercato del {mercato} nel paese {paese}: età, caratteristiche, bisogni",
                f"In quali aree geografiche è concentrato il mercato del {mercato}  nel paese {paese}",
                f"Quali sono le esigenze e le tendenze esistenti del target nel paese {paese} per il mercato del {mercato} ",
                f"Concorrenza, descrizione generica per mercato del {mercato} nel paese {paese}",
                f"Quali sono i 3 best competitor per mercato del {mercato}  nel paese {paese}: descrizione, modello di business, strategia commerciale e di marketing, social ads",
                f"Quali sono possibili modelli di business per mercato del {mercato} nel paese {paese}",
                f"Conclusioni per il mercato del {mercato} nel paese {paese}"
            ]
            
            # Function to get answers in parallel
            def get_answer(question):
                return question, gen_reply(question)

            # Using ThreadPoolExecutor to call the GPT-3.5 model in parallel
            with concurrent.futures.ThreadPoolExecutor() as executor:
                results = list(executor.map(get_answer, questions))
            
            # Display the answers
            for question, answer in results:
                st.subheader(question)
                st.write(answer)
        else:
            st.error("Per favore, inserisci sia il mercato di interesse che il paese di interesse.")

main()
