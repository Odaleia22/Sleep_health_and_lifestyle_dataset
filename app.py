from flask import Flask, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import os
import json

app = Flask(__name__)

def carregar_planilha():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    
    cred_json = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
    if not cred_json:
        raise Exception("Erro: variável de ambiente GOOGLE_SERVICE_ACCOUNT_JSON não está definida")
    
    try:
        creds_dict = json.loads(cred_json)
        creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
    except json.JSONDecodeError:
        raise Exception("Erro ao decodificar o JSON da variável GOOGLE_SERVICE_ACCOUNT_JSON")
    
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
