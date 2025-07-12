from flask import Flask, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

app = Flask(__name__)

def carregar_planilha():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("mae-carol-jemison-e14399619f29.json", scope)
    client = gspread.authorize(creds)

    # Altere abaixo com sua planilha e aba
    planilha = client.open("Sleep_health_and_lifestyle_dataset").worksheet("Sleep_health_and_lifestyle_dataset")
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