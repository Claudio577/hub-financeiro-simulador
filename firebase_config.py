import firebase_admin
from firebase_admin import credentials, firestore
import json
import os

# Carrega a chave que está nos Secrets do Streamlit
firebase_key_json = os.environ.get("FIREBASE_KEY_JSON")

if not firebase_key_json:
    raise ValueError("Chave FIREBASE_KEY_JSON não encontrada nos secrets do Streamlit!")

# Converte o texto JSON dos secrets para um dicionário Python
firebase_key_dict = json.loads(firebase_key_json)

# Cria a credencial Firebase a partir do dicionário
cred = credentials.Certificate(firebase_key_dict)

# Inicializa o Firebase se ainda não tiver sido inicializado
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

# Conexão com o Firestore
db = firestore.client()
