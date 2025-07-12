from flask import Flask, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import os
import json
import base64  

app = Flask(__name__)

def carregar_planilha():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    
    # 1. Obter a variável de ambiente codificada em Base64
    cred_base64 = os.getenv("GOOGLE_CREDENTIALS_BASE64")
    if not cred_base64:
        raise Exception("Erro: variável de ambiente GOOGLE_CREDENTIALS_BASE64 não está definida")
    
    try:
        # 2. Decodificar a string Base64 de volta para uma string JSON
        cred_json_string = base64.b64decode(cred_base64).decode('utf-8')
        
        # 3. Converter a string JSON em um dicionário Python
        creds_dict = json.loads(cred_json_string)
        
    except Exception as e:
        # Captura qualquer erro no processo de decodificação
        raise Exception(f"Erro ao decodificar as credenciais a partir da variável de ambiente: {e}")
    
    # 4. Usar o dicionário de credenciais para autorizar
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)

    planilha_id = "11VY8Yd7Jne2Ciq7bM-fLAuysAP82Scv7RkcyRFLELWY"
    planilha = client.open_by_key(planilha_id).worksheet("Sleep_health_and_lifestyle_dataset")
    
    dados = planilha.get_all_records()
    df = pd.DataFrame(dados)
    return df

@app.route("/dados", methods=["GET"])
def dados():
    try:
        df = carregar_planilha()
        return jsonify(df.to_dict(orient="records"))
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)