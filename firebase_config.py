import firebase_admin
from firebase_admin import credentials, firestore

# Carrega o arquivo da chave privada
cred = credentials.Certificate("firebase-key.json")

# Inicializa o Firebase Admin SDK
firebase_admin.initialize_app(cred)

# Cria o cliente Firestore
db = firestore.client()
