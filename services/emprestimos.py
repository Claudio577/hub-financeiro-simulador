from firebase_config import db
from datetime import datetime

def contratar_emprestimo(user_id, valor, juros=0.1):
    total = round(valor * (1 + juros), 2)

    user_ref = db.collection("usuarios").document(user_id)
    user = user_ref.get().to_dict()

    if not user:
        return False, "Usuário não encontrado."

    # Crédito do empréstimo
    user_ref.update({"saldo": user["saldo"] + valor})

    # Salvar empréstimo
    db.collection("emprestimos").add({
        "user_id": user_id,
        "valor": valor,
        "total": total,
        "juros": juros,
        "data": datetime.now().isoformat()
    })

    # Registrar transação
    db.collection("transacoes").add({
        "user_id": user_id,
        "tipo": "Empréstimo contratado",
        "valor": valor,
        "descricao": f"Total a pagar R$ {total}",
        "data": datetime.now().isoformat()
    })

    return True, total
