import pandas as pd
from transformers import BertTokenizer, BertModel
import torch
from bert_score import score

archivo_excel = r"C:\Users\Patricia\OneDrive - Universidad Politécnica de Madrid\Documentos\TFM\NewCode\Excels\excel100_BERT.xlsx"
df = pd.read_excel(archivo_excel)

respuestas_correctas = df['Context']
respuestas_generadas = df['Answer']

bert_scores = []

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

for idx, (respuesta_correcta, respuesta_generada) in enumerate(zip(respuestas_correctas, respuestas_generadas)):
    try:
       
        P, R, F1 = score([respuesta_generada], [respuesta_correcta], model_type='bert-base-uncased')
        bert_score = F1.mean().item()  
        
        bert_scores.append(bert_score)

        print(f'BERT Score para el par {idx + 1} de 100')
    except Exception as e:
     
        bert_scores.append(None)
        print(f'Error en el cálculo para el par {idx + 1}: {e}')


df['BERT Score'] = bert_scores

df.to_excel(archivo_excel, index=False)

print("Cálculo completado.")
