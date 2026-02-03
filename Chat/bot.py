import telebot
import threading

import banco
import faq
import scheduler

# Configurações Iniciais
TOKEN = "8165556275:AAG63FVXcFViG6Jxy3KCojD1cZQh8IbUoXE"
bot = telebot.TeleBot(TOKEN)

AVISO = "\n\n⚠️ Este bot é informativo e não substitui orientação médica."

# INICIALIZAÇÃO 
banco.criar_tabelas()

# BOT CONVERSACIONAL 
@bot.message_handler(func=lambda message: True)
def conversa(message):
    chat_id = message.chat.id
    texto = message.text.strip().lower()

    # garante que o usuário exista no banco
    banco.criar_usuario_se_nao_existir(chat_id)

    estado = banco.obter_estado(chat_id)

    # Usuario novo
    if estado is None:
        bot.send_message(chat_id, "Olá! 👋\nQual é o seu nome?")
        banco.definir_estado(chat_id, "nome")

    # DAdos Nome 
    elif estado == "nome":
        banco.salvar_temp(chat_id, texto)
        banco.definir_estado(chat_id, "senha")
        bot.send_message(chat_id, "Certo 😊\nAgora informe sua senha:")

    # Dados Login
    elif estado == "senha":
        nome = banco.obter_temp(chat_id)
        banco.cadastrar_usuario(chat_id, nome, texto)
        banco.definir_estado(chat_id, "medicamento")

        bot.send_message(
            chat_id,
            "✅ Login realizado com sucesso!\n\n"
            "Qual medicamento você toma?"
        )

    # Definir nome da medicação
    elif estado == "medicamento":
        banco.salvar_temp(chat_id, texto)
        banco.definir_estado(chat_id, "horario")

        bot.send_message(
            chat_id,
            "Perfeito 💊\n"
            "Em qual horário devo te lembrar? (formato HH:MM)"
        )

    # Definir Horário
    elif estado == "horario":
        usuario_id = banco.usuario_logado(chat_id)

        if not usuario_id:
            banco.definir_estado(chat_id, None)
            bot.send_message(chat_id, "Erro de sessão. Vamos começar de novo.")
            return

        medicamento = banco.obter_temp(chat_id)
        banco.cadastrar_medicamento(usuario_id, medicamento, texto)

        banco.definir_estado(chat_id, "faq")

        bot.send_message(
            chat_id,
            f"⏰ Pronto!\n"
            f"Vou te lembrar de tomar *{medicamento.title()}* às *{texto}*.",
            parse_mode="Markdown"
        )

    # Perguntas
    elif estado == "faq":
        resposta = faq.buscar_resposta("antibiotico para dor", texto)

        if resposta:
            bot.send_message(chat_id, resposta + AVISO)
        else:
            bot.send_message(
                chat_id,
                "Não encontrei essa informação específica.\n"
                "Se persistirem dúvidas, procure um profissional de saúde."
                + AVISO
            )

# Execução
if __name__ == "__main__":
    # thread separada para os lembretes
    threading.Thread(
        target=scheduler.iniciar_scheduler,
        args=(bot,),
        daemon=True
    ).start()

    print("🤖 Bot conversacional em execução...")
    bot.infinity_polling()
