import streamlit as st
from firebase_config import db

# Importando serviços
from services.pix import enviar_pix
from services.pagamentos import pagar_boleto
from services.recargas import fazer_recarga
from services.emprestimos import contratar_emprestimo

USER_ID = "usuario_01"

# =============================
# Funções auxiliares
# =============================

def get_saldo():
    doc = db.collection("usuarios").document(USER_ID).get()
    if doc.exists:
        return doc.to_dict().get("saldo", 0)
    return 0

def get_transacoes(limit=10):
    trans = (
        db.collection("transacoes")
        .where("user_id", "==", USER_ID)
        .order_by("data", direction="DESCENDING")
        .limit(limit)
        .stream()
    )
    return [t.to_dict() for t in trans]

# =============================
# Interface Streamlit
# =============================

st.set_page_config(page_title="Hub Financeiro", layout="wide")

st.title("💸 Hub Financeiro — Firebase + Streamlit")

menu = st.sidebar.radio(
    "Menu",
    ["Dashboard", "PIX", "Pagamentos", "Recargas", "Empréstimos"]
)

# =============================
# Dashboard
# =============================
if menu == "Dashboard":
    st.header("📊 Dashboard Financeiro")

    st.metric("Saldo atual", f"R$ {get_saldo():,.2f}")

    st.subheader("Últimas transações")

    transacoes = get_transacoes()

    if len(transacoes) == 0:
        st.info("Nenhuma transação encontrada.")
    else:
        for t in transacoes:
            st.write(
                f"**{t['tipo']}** — {t['descricao']} — R$ {t['valor']:.2f} — {t['data']}"
            )

# =============================
# PIX
# =============================
elif menu == "PIX":
    st.header("⚡ Enviar PIX")

    chave = st.text_input("Chave PIX")
    valor = st.number_input("Valor", min_value=1.0)

    if st.button("Enviar PIX"):
        ok, msg = enviar_pix(USER_ID, chave, valor)
        st.success(msg) if ok else st.error(msg)

# =============================
# Pagamentos
# =============================
elif menu == "Pagamentos":
    st.header("💳 Pagamento de Boleto")

    codigo = st.text_input("Código de barras")
    valor = st.number_input("Valor do boleto", min_value=1.0)

    if st.button("Pagar boleto"):
        ok, msg = pagar_boleto(USER_ID, codigo, valor)
        st.success(msg) if ok else st.error(msg)

# =============================
# Recargas
# =============================
elif menu == "Recargas":
    st.header("📱 Recarga de Celular")

    numero = st.text_input("Número do celular")
    operadora = st.selectbox("Operadora", ["Vivo", "Claro", "TIM", "Oi"])
    valor = st.number_input("Valor da recarga", min_value=1.0)

    if st.button("Fazer recarga"):
        ok, msg = fazer_recarga(USER_ID, numero, operadora, valor)
        st.success(msg) if ok else st.error(msg)

# =============================
# Empréstimos
# =============================
elif menu == "Empréstimos":
    st.header("🏦 Contratar Empréstimo")

    valor = st.number_input("Valor desejado", min_value=100.0)

    if st.button("Contratar empréstimo"):
        ok, total = contratar_emprestimo(USER_ID, valor)
        if ok:
            st.success(f"Empréstimo aprovado! Total a pagar: R$ {total:.2f}")
        else:
            st.error(total)
