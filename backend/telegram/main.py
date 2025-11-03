from telegram.ext import Application, ConversationHandler, MessageHandler, CommandHandler, filters, ContextTypes
from datetime import datetime
from telegram import Update
import validations
import processing
import database

TOKEN = "8030257844:AAEzUlXSamdDxZHqA1tnSSk9zMc9fpSWEbA"

removeMonth = ""

GO_TO_SHOWEXPENSES, GO_TO_REMOVEEXPENSES, GO_TO_GETMONTH, GO_TO_GETIDS, GO_TO_SHOWALL = range(5)

async def showMenu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        print("Mostrando menu.\n---------------------------------")
        await update.message.reply_text("---------- Bot de finanças ----------\nInsira um gasto no seguinte modelo:\n\n VALOR TIPO DATA DESCRIÇÃO\n29,99 Compras 26/09/2005 Camiseta\n\nOs tipos disponíveis são: Transporte, Compras, Extra e Outros.\n\nDigite /1 para mostrar a soma dos gastos em um mês.\n\nDigite /2 para mostrar as informações dos gastos em um mês.\n\nDigite /3 para remover gastos.\n-------------------------------------")
        return True
    except Exception as e:
        print(f"Erro ao mostrar o menu.\nErro: {e}\n--------------------")
        return None

async def storeExpenses(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        input = update.message.text
        input = processing.inputProcessing(input)
        if isinstance(input, str):
            await update.message.reply_text(input)
            return
        output = database.store(input)
        if output is None:
            await update.message.reply_text("Erro ao armazenar gasto.")
            return    
        await update.message.reply_text(output)
    except Exception as e:
        print(e)
        return None
    
async def showAux(update:Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Digite o mês que quer visualizar.")
    return GO_TO_SHOWEXPENSES

async def showExpenses(update:Update, context: ContextTypes.DEFAULT_TYPE):
    print("Apresentando gastos...")
    try:
        input = update.message.text
        month = validations.validateMonth(input)
        if month is False:
            await update.message.reply_text("Mês inválido, tente novamente.")
            return
        date, nextDate = validations.validateDBDates(month)
        search = database.getExpenses(date, nextDate)
        output = f"--- Resumo dos Gastos no Mês de {input.capitalize()} ---\n" + search 
        await update.message.reply_text(output)
        print(search)
        return ConversationHandler.END
    except Exception as e:
        print(f"Erro ao mostrar gastos.\nErro: {e}")
        return None
    
async def removeAux1(update:Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Digite o mês que quer remover algum gasto.")
    return GO_TO_GETMONTH

async def removeAux2(update:Update, context: ContextTypes.DEFAULT_TYPE):
    global removeMonth 
    removeMonth = update.message.text
    Month = validations.validateMonth(removeMonth)
    if Month is False:
        await update.message.reply_text("Mês inválido.")
        return ConversationHandler.END
    results = database.showAll(Month, "5")
    if not results:
        await update.message.reply_text("Nenhum gasto encontrado.")
        return ConversationHandler.END        
    output = processing.outputProcessing(results)
    try:
        await update.message.reply_text(output)
        await update.message.reply_text("Digite os IDs dos gastos que quer remover.\n\nUtilize uma barra de espaço entre eles.\n\nSe mudar de ideia, digite SAIR.")
        return GO_TO_GETIDS
    except:
        print("Mensagem muito grande. Dividindo ela em duas...")
        results1, results2 = database.showAll(Month, "4")
        if not results1 and not results2:
            await update.message.reply_text("Nenhum gasto encontrado.")
            return ConversationHandler.END   
        output = processing.outputProcessing(results1, 1)
        await update.message.reply_text(output)
        output = processing.outputProcessing(results2, 1)
        await update.message.reply_text(output)
        await update.message.reply_text("Digite os IDs dos gastos que quer remover.\n\nUtilize uma barra de espaço entre eles.\n\nSe mudar de ideia, digite SAIR.")
        return GO_TO_GETIDS
        
async def removeExpenses(update:Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        removeIDs = update.message.text
        if removeIDs.upper() == "SAIR":
            await update.message.reply_text("Saindo da remoção de gastos.")
            return ConversationHandler.END
        removeIDs = removeIDs.split(" ")
        status = database.removeExpenses(removeIDs)
        if status is True:
            await update.message.reply_text("Remoção finalizada.")
        return ConversationHandler.END
    except Exception as e:
        print(f"Erro ao remover gastos.\nErro: {e}")
        return None
    
async def showAllAux(update:Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Digite o mês que quer visualizar os detalhes dos gastos.")
    return GO_TO_SHOWALL

async def showAllExpenses(update:Update, context: ContextTypes.DEFAULT_TYPE):
    print("Mostrando gastos...")
    try:
        global removeMonth 
        removeMonth = update.message.text
        Month = validations.validateMonth(removeMonth)
        if Month is False:
            await update.message.reply_text("Mês inválido.")
            return ConversationHandler.END
        results = database.showAll(Month, "2")
        if not results:
            await update.message.reply_text("Nenhum gasto encontrado.")
            return ConversationHandler.END               
        output = processing.outputProcessing(results)
        try:
            await update.message.reply_text(output)
            return ConversationHandler.END
        except:
            print("Mensagem muito grande. Dividindo ela em duas...")
            results1, results2 = database.showAll(Month, "3")
            output = processing.outputProcessing(results1)
            await update.message.reply_text(output)
            output = processing.outputProcessing(results2, 1)
            await update.message.reply_text(output)
            return ConversationHandler.END
    except Exception as e:
        print(f"Erro ao mostrar gastos.\nErro: {e}")
        await update.message.reply_text(e)
        return None

def main():
    try:
        database.createTable()
        application = Application.builder().token(TOKEN).build()
        conv_handler = ConversationHandler(
            entry_points = [
                CommandHandler("1", showAux),
                CommandHandler("2", showAllAux),
                CommandHandler("3", removeAux1),
                ],
            states = {
                GO_TO_SHOWEXPENSES: [MessageHandler(filters.TEXT & ~filters.COMMAND, showExpenses)],
                GO_TO_GETMONTH: [MessageHandler(filters.TEXT & ~filters.COMMAND, removeAux2)],
                GO_TO_GETIDS: [MessageHandler(filters.TEXT & ~filters.COMMAND, removeExpenses)],
                GO_TO_SHOWALL: [MessageHandler(filters.TEXT & ~filters.COMMAND, showAllExpenses)]
                },
            fallbacks = []
        )
        application.add_handler(conv_handler)
        application.add_handler(CommandHandler("start", showMenu))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, storeExpenses))
        application.run_polling()
    except Exception as e:
        print(f"Erro no main.\nErro: {e}")
        return None
    
if __name__ == "__main__":
    main()