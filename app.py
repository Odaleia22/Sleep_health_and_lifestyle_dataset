from flask import Flask, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import os
import json

app = Flask(__name__)

def carregar_planilha():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    # Pegando a credencial JSON da variável de ambiente (string JSON)
    cred_json = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
    if not cred_json:
        raise Exception("Variável de ambiente GOOGLE_SERVICE_ACCOUNT_JSON não definida")
    
    creds_dict = json.loads(cred_json)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)

    # Usando open_by_key com o ID da planilha
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
