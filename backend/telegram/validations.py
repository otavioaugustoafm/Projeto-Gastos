from datetime import datetime
currentYear = datetime.now().year
currentMonth = datetime.now().month

def validateDate(date):
    try:
        print(f"\nValidando data: {date}")
        try:
            date = datetime.strptime(date, "%d/%m/%Y").date()
            dbDate = datetime.strftime(date, "%Y-%m-%d")
            print("Data válida.\n--------------------")
            return dbDate
        except:
            try:    
                date1 = f"{date}/{currentYear}"
                date1 = datetime.strptime(date1, "%d/%m/%Y").date()
                dbDate = datetime.strftime(date1, "%Y-%m-%d")
                print("Data válida.\n--------------------")
                return dbDate
            except:
                try:
                    date2 = f"{date}/{currentMonth}/{currentYear}"
                    date2 = datetime.strptime(date2, "%d/%m/%Y")
                    dbDate = datetime.strftime(date2, "%Y-%m-%d")
                    print("Data válida.\n--------------------")
                    return dbDate
                except:
                    print("Data inválida.\n--------------------")
                    return False
    except Exception as e:
        print(f"Erro ao validar data.\nErro: {e}")
        return None

def validateType(type):
    try:
        print(f"\nValidando tipo: {type}")
        TYPES = ["COMPRAS", "TRANSPORTE", "EXTRA", "OUTROS"]
        type = type.upper()
        if type in TYPES:
            type = type.capitalize()
            print(f"Tipo válido.\n--------------------")
            return type
        else:
            type = type.capitalize()
            print(f"Tipo inválido.\n--------------------")
            return False
    except Exception as e:
        print(f"Erro ao checar tipo.\nErro: {e}\n--------------------")
        return None
    
def validateMonth(month):
    try:
        print(f"\nValidando mês: {month}")
        MONTHS = ["JANEIRO", "FEVEREIRO", "MARÇO", "ABRIL", "MAIO", "JUNHO", "JULHO", "AGOSTO", "SETEMBRO", "OUTUBRO", "NOVEMBRO", "DEZEMBRO"]
        if month.upper() in MONTHS:
            month = MONTHS.index(month.upper())
            print("Mês válido.\n--------------------")
            return month + 1
        else:
            print("Mês inválido.\n--------------------")
            return False
    except Exception as e:
        print(f"Erro ao checar o mês.\nErro: {e}\n--------------------")
        return None

def validateDBDates(month):
    try:
        currentYear = datetime.now().year
        date = f"2/{month}/{currentYear}"
        nextDate = '1/'
        if month == 12:
            nextDate += f"1/{currentYear + 1}"
        else:
            nextDate += f"{month + 1}/{currentYear}"
        date = datetime.strptime(date, "%d/%m/%Y").date()
        date = datetime.strftime(date, "%Y-%m-%d")
        nextDate = datetime.strptime(nextDate, "%d/%m/%Y").date()
        nextDate = datetime.strftime(nextDate, "%Y-%m-%d")
        return date, nextDate
    except Exception as e:
        print(f"Erro ao transformar o mês nas datas do BD.\nErro: {e}\n--------------------")
        return None