import os
import openai
from dotenv import load_dotenv, find_dotenv
import fitz  
import streamlit as st

#OpenAI API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

#PDF files
file_paths = { 
    "CNMC": {"file": r"C:\Users\Patricia\OneDrive - Universidad Politécnica de Madrid\Documentos\TFM\NewCode\Documentos_Chatbot\1.1CNMC.pdf", "countries": ["Spain", "España", "Espagne", "Spanje", "Spanien", "Spagna", 
               "español", "spanish", "espagnol", "spaans", "spanisch", "spagnolo"]},
    
    "ARCEP": {"file": r"C:\Users\Patricia\OneDrive - Universidad Politécnica de Madrid\Documentos\TFM\NewCode\Documentos_Chatbot\2.1ARCEP.pdf", "countries": ["France", "Francia", "Frankrijk", "Frankreich", 
               "francés", "frances", "french", "français", "frans", "französisch", "francese"]},
    "ARCEP": {"file": r"C:\Users\Patricia\OneDrive - Universidad Politécnica de Madrid\Documentos\TFM\NewCode\Documentos_Chatbot\2.2ARCEP.pdf", "countries": ["France", "Francia", "Frankrijk", "Frankreich", 
               "francés", "frances", "french", "français", "frans", "französisch", "francese"]},
    "ARCEP": {"file": r"C:\Users\Patricia\OneDrive - Universidad Politécnica de Madrid\Documentos\TFM\NewCode\Documentos_Chatbot\2.3ARCEP.pdf", "countries": ["France", "Francia", "Frankrijk", "Frankreich", 
               "francés", "frances", "french", "français", "frans", "französisch", "francese"]},
    
    "BIPT": {"file": r"C:\Users\Patricia\OneDrive - Universidad Politécnica de Madrid\Documentos\TFM\NewCode\Documentos_Chatbot\3.1BIPT.pdf", "countries": ["Belgium", "Bélgica", "Belgique", "België", "Belgien", "Belgio", 
               "belga", "belgian", "belge", "belgisch", "belgier"]},
    "BIPT": {"file": r"C:\Users\Patricia\OneDrive - Universidad Politécnica de Madrid\Documentos\TFM\NewCode\Documentos_Chatbot\3.2BIPT.pdf", "countries": ["Belgium", "Bélgica", "Belgique", "België", "Belgien", "Belgio", 
               "belga", "belgian", "belge", "belgisch", "belgier"]},
    
    "ACM": {"file": r"C:\Users\Patricia\OneDrive - Universidad Politécnica de Madrid\Documentos\TFM\NewCode\Documentos_Chatbot\4.1ACM.pdf", "countries": ["Netherlands", "Países Bajos", "Pays-Bas", "Nederland", "Niederlande", "Paesi Bassi", 
               "neerlandés", "neerlandes", "dutch", "néerlandais", "nederlands", "holländisch", "olandese"]},
    "ACM": {"file": r"C:\Users\Patricia\OneDrive - Universidad Politécnica de Madrid\Documentos\TFM\NewCode\Documentos_Chatbot\4.2ACM.pdf", "countries": ["Netherlands", "Países Bajos", "Pays-Bas", "Nederland", "Niederlande", "Paesi Bassi", 
               "neerlandés", "neerlandes", "dutch", "néerlandais", "nederlands", "holländisch", "olandese"]},
    
    "BNetzA": {"file": r"C:\Users\Patricia\OneDrive - Universidad Politécnica de Madrid\Documentos\TFM\NewCode\Documentos_Chatbot\5.1BNETZA.pdf", "countries": ["Germany", "Alemania", "Allemagne", "Duitsland", "Deutschland", "Germania", 
               "alemán", "aleman", "german", "allemand", "duits", "deutsch", "tedesco", "Bundesnetzagentur", "breitbandmessung"]},
    "BNetzA": {"file": r"C:\Users\Patricia\OneDrive - Universidad Politécnica de Madrid\Documentos\TFM\NewCode\Documentos_Chatbot\5.2BNETZA.pdf", "countries": ["Germany", "Alemania", "Allemagne", "Duitsland", "Deutschland", "Germania", 
               "alemán", "aleman", "german", "allemand", "duits", "deutsch", "tedesco", "Bundesnetzagentur", "breitbandmessung"]},
    
    "AGCOM": {"file": r"C:\Users\Patricia\OneDrive - Universidad Politécnica de Madrid\Documentos\TFM\NewCode\Documentos_Chatbot\6.1AGCOM.pdf", "countries": ["Italy", "Italia", "Italie", "Italië", "Italien", 
               "italiano", "italian", "italien", "italiaans", "italienisch"]},
    "AGCOM": {"file": r"C:\Users\Patricia\OneDrive - Universidad Politécnica de Madrid\Documentos\TFM\NewCode\Documentos_Chatbot\6.2AGCOM.pdf", "countries": ["Italy", "Italia", "Italie", "Italië", "Italien", 
               "italiano", "italian", "italien", "italiaans", "italienisch"]},
    
    "RTR": {"file": r"C:\Users\Patricia\OneDrive - Universidad Politécnica de Madrid\Documentos\TFM\NewCode\Documentos_Chatbot\7RTR.pdf", "countries": ["Austria", "Autriche", "Oostenrijk", "Österreich", 
               "austriaco", "austrian", "autrichien", "oostenrijks", "österreichisch"]},
    
    "ComReg": {"file": r"C:\Users\Patricia\OneDrive - Universidad Politécnica de Madrid\Documentos\TFM\NewCode\Documentos_Chatbot\8.1COMREG.pdf", "countries": ["Ireland", "Irlanda", "Irlande", "Ierland", "Irland", 
               "irlandés", "irlandes", "irish", "irlandais", "iers", "irisch", "irlandese"]},
    "ComReg": {"file": r"C:\Users\Patricia\OneDrive - Universidad Politécnica de Madrid\Documentos\TFM\NewCode\Documentos_Chatbot\8.2COMREG.pdf", "countries": ["Ireland", "Irlanda", "Irlande", "Ierland", "Irland", 
               "irlandés", "irlandes", "irish", "irlandais", "iers", "irisch", "irlandese"]},
    
    "Ofcom": {"file": r"C:\Users\Patricia\OneDrive - Universidad Politécnica de Madrid\Documentos\TFM\NewCode\Documentos_Chatbot\9.1OFCOM.pdf", "countries": ["United Kingdom", "UK", "Reino Unido", "Royaume-Uni", "Verenigd Koninkrijk", "Vereinigtes Königreich", "Regno Unito", 
               "británico", "britanico", "british", "britannique", "brits", "britisch", "britannico"]},
    "Ofcom": {"file": r"C:\Users\Patricia\OneDrive - Universidad Politécnica de Madrid\Documentos\TFM\NewCode\Documentos_Chatbot\9.2OFCOM.pdf", "countries": ["United Kingdom", "UK", "Reino Unido", "Royaume-Uni", "Verenigd Koninkrijk", "Vereinigtes Königreich", "Regno Unito", 
               "británico", "britanico", "british", "britannique", "brits", "britisch", "britannico"]},
    
    "FCC": {"file": r"C:\Users\Patricia\OneDrive - Universidad Politécnica de Madrid\Documentos\TFM\NewCode\Documentos_Chatbot\10.1FCC.pdf", "countries": ["United States", "USA", "Estados Unidos", "États-Unis", "Verenigde Staten", "Vereinigte Staaten", "Stati Uniti", 
               "estadounidense", "american", "américain", "amerikaans", "amerikanisch", "americano"]},
    "FCC": {"file": r"C:\Users\Patricia\OneDrive - Universidad Politécnica de Madrid\Documentos\TFM\NewCode\Documentos_Chatbot\10.2FCC.pdf", "countries": ["United States", "USA", "Estados Unidos", "États-Unis", "Verenigde Staten", "Vereinigte Staaten", "Stati Uniti", 
               "estadounidense", "american", "américain", "amerikaans", "amerikanisch", "americano"]},
    "FCC": {"file": r"C:\Users\Patricia\OneDrive - Universidad Politécnica de Madrid\Documentos\TFM\NewCode\Documentos_Chatbot\10.3FCC.pdf", "countries": ["United States", "USA", "Estados Unidos", "États-Unis", "Verenigde Staten", "Vereinigte Staaten", "Stati Uniti", 
               "estadounidense", "american", "américain", "amerikaans", "amerikanisch", "americano"]}
}

#Extract text from PDF
def extract_text_with_pymupdf(file_path):
    try:
        doc = fitz.open(file_path)
        text = ''
        for page in doc:
            text += page.get_text()  
        return text
    except Exception as e:
        print(f"Error al procesar {file_path}: {e}")
        return ""

#Read only relevant PDFs
def get_relevant_pdfs(user_question):
    relevant_pdfs = []
    for regulator, details in file_paths.items():
        if regulator.lower() in user_question.lower() or any(country.lower() in user_question.lower() for country in details["countries"]):
            relevant_pdfs.append(details["file"])
    return relevant_pdfs

#Answer in the same language as user
def detect_language(text):
    messages = [
        {"role": "system", "content": "You are a language detection bot. Detect the language of the following question and respond with the name of the language"},
        {"role": "user", "content": text}
    ]
    
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",  
        messages=messages,
        temperature=0
    )
    
    return response['choices'][0]['message']['content'].strip()

#API call
def get_completion_from_messages(messages, model="gpt-4o-mini", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response['choices'][0]['message']['content']


#User interface
st.title("TelReg AI")

st.write("Get answers on telecommunication regulators mobile measurement methodologies.")

user_question = st.text_input("Write your question here:")

if user_question:
    
    language = detect_language(user_question)
    
    
    relevant_pdfs = get_relevant_pdfs(user_question)
    
    
    if not relevant_pdfs:
        st.write("I don't manage that information. I recommend you to look on the corresponding official website.")
    else:
     
        context = ""
        for pdf in relevant_pdfs:
            context += extract_text_with_pymupdf(pdf) + "\n"
        
        #Prompt
        messages = [
            {"role": "system", "content": f"""
            You are TelReg AI, a chatbot to answer questions related to the measurement methodologies of the NRAs provided to you. \
            You respond in the same language as the user writes the question, which for this conversation is {language}. \
            You first read the question, and then you look for that information in the texts given to you. \
            Make sure to understand the question and search for that information in the texts provided to you. \
            You respond in an accurate style, following exactly the format of the answer that the user is telling to you. \
            For questions whose answer is a number, answer with the number in digits followed by its corresponding unit, without adding additional information. \
            You never respond saying that some information has been provided to you or saying "as per the provided information" or "The document...", \
            you just respond the answer without letting the user know that information has been passed on to you. \
            If the user asks you which are the measurement methodologies used by any regulator, you just answer telling the method that it uses. \
            The information provided to you is about the regulators CNMC, ARCEP, BIPT, ACM, BNetzA, AGCOM, RTR, ComReg, Ofcom and FCC, and it is in text format. \
            """},
            {"role": "user", "content": f"Here are the texts extracted from the methodologies of some telecommunication regulators:\n{context}\n\nPregunta: {user_question}"}
        ]
        
        answer = get_completion_from_messages(messages)
        st.write(f"{answer}")
