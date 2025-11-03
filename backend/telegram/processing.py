from datetime import datetime
import validations
import re

def inputProcessing(input):
    try:
        print("Processando entrada...")
        expenseValue = -1; expenseType = ""; expenseDate = ""; expenseDescription = "Nenhuma"
        currentDate = datetime.strftime(datetime.now().date(), "%Y-%m-%d")
        expense = {
            "Value": 0,
            "Type": "",
            "Date": "",
            "Description": ""
        }
        input = input.split(" ", 2)
        if len(input) == 1:
            print("Entrada inválida.\n--------------------")
            return "Entrada inválida."
        try:
            expenseValue = float(input[0].replace(",", "."))
        except: 
            return "Valor inválido."
        expenseType = validations.validateType(input[1])
        if expenseType is False:
            return "Tipo inválido."
        elif expenseType is None:
            return "Erro ao verificar o tipo."
        expense["Value"] = expenseValue; expense["Type"] = expenseType
        if len(input) == 2:
            expense["Date"] = currentDate; expense["Description"] = "Nenhuma"
            return expense
        else:        
            match = re.match(r"^(\d{1,2}(?:/)?(?:\d{1,2})?(?:/)?(?:\d+)?)(?:\s(.+))?$", input[2])
            if match:
                expenseDate, expenseDescription = match.groups()
                expenseDate = validations.validateDate(expenseDate)
                if expenseDescription is None:
                    expenseDescription = "Nenhuma"
                if expenseDate is False:
                    return "Data inválida.\n--------------------"
                elif expenseDate is None:
                    return "Erro ao verificar data.\n--------------------" 
                expense["Date"] = expenseDate
            else:
                expenseDescription = input[2]
                expense["Date"] = currentDate
            expense["Description"] = expenseDescription; 
        return expense
    except Exception as e:
        print(f"Erro ao processar a entrada.\nErro: {e}\n--------------------")
        return None
    
def outputProcessing(list, option=None):
    try:
        output = ""
        if option is None:
            output = "\n---------- Seus Gastos ----------\n"
        for item in list:
            try:
                Id, Value, Type, Date, Description = item
                output += f"ID: {Id}\n"
            except:
                Value, Type, Date, Description = item
            Date = datetime.strptime(Date, '%Y-%m-%d')
            Date = datetime.strftime(Date, '%d/%m/%Y')
            Value = f"{Value:.2f}".replace(".", ",")
            output += f"Valor: R${Value}\n"
            output += f"Tipo: {Type}\n"
            output += f"Data: {Date}\n"
            output += f"Descrição: {Description}"
            output += "\n---------------------------------\n"
        print(output)
        return output
    except Exception as e:
        print(f"Erro ao processar a saída.\nErro: {e}")
        return None