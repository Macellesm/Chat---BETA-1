import time
from datetime import datetime
from zoneinfo import ZoneInfo  # Python 3.9+

import banco

AVISO = "\n\n⚠️ Este bot é informativo e não substitui orientação médica."

# Guarda último envio por usuário/medicamento
ultimos_envios = set()

def verificar_lembretes(bot):
    agora = datetime.now(ZoneInfo("America/Sao_Paulo")).strftime("%H:%M")

    lembretes = banco.listar_medicamentos()

    for chat_id, medicamento, horario in lembretes:
        chave = (chat_id, medicamento, horario, agora)

        if horario == agora and chave not in ultimos_envios:
            bot.send_message(
                chat_id,
                f"⏰ *Hora de tomar seu medicamento*\n"
                f"💊 *{medicamento.title()}* — {horario}"
                + AVISO,
                parse_mode="Markdown"
            )
            ultimos_envios.add(chave)

def iniciar_scheduler(bot):
    while True:
        verificar_lembretes(bot)
        time.sleep(30)
