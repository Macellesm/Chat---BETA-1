from difflib import get_close_matches

FAQ = {
    "antibiotico para dor": {
        "esqueci de tomar": "Tome assim que lembrar. Se estiver perto da próxima dose, pule a esquecida.",
        "posso tomar em outro horario": "Evite alterar o horário sem orientação médica.",
        "quantos dias devo tomar": "Antibióticos devem ser tomados pelo período completo prescrito."
    }
}

def buscar_resposta(medicamento, pergunta):
    if medicamento not in FAQ:
        return None

    perguntas = FAQ[medicamento].keys()
    match = get_close_matches(pergunta.lower(), perguntas, n=1, cutoff=0.5)

    if match:
        return FAQ[medicamento][match[0]]
    return None
