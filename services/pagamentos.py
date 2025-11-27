from firebase_config import db
from datetime import datetime

def pagar_boleto(user_id, codigo, valor):
    user_ref = db.collection("usuarios").document(user_id)
    user = user_ref.get().to_dict()

    if not user:
        return False, "Usuário não encontrado."

    if user["saldo"] < valor:
        return False, "Saldo insuficiente."

    user_ref.update({"saldo": user["saldo"] - valor})

    db.collection("transacoes").add({
        "user_id": user_id,
        "tipo": "Pagamento de boleto",
        "valor": -valor,
        "descricao": f"Boleto {codigo}",
        "data": datetime.now().isoformat()
    })

    return True, "Pagamento realizado!"
