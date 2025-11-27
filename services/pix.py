from firebase_config import db
from datetime import datetime

def enviar_pix(user_id, chave, valor):
    # Referência ao usuário
    user_ref = db.collection("usuarios").document(user_id)
    user = user_ref.get().to_dict()

    if not user:
        return False, "Usuário não encontrado."

    if user["saldo"] < valor:
        return False, "Saldo insuficiente."

    # Atualiza saldo
    user_ref.update({"saldo": user["saldo"] - valor})

    # Registra transação
    db.collection("transacoes").add({
        "user_id": user_id,
        "tipo": "PIX enviado",
        "valor": -valor,
        "descricao": f"PIX para {chave}",
        "data": datetime.now().isoformat()
    })

    return True, "PIX enviado com sucesso!"
