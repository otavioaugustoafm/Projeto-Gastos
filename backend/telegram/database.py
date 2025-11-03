import sqlite3
from datetime import datetime
import processing
import validations
import os
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database", "ExpensesTable.db")

def createTable():
    print("--------------------\nCriando ou verificando tabela...")
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Expenses (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Value INTEGER NOT NULL,
                Type VARCHAR(11) NOT NULL,
                Date DATE NOT NULL,
                Description VARCHAR(255)
                )
        """)
        connection.commit()
        connection.close()
        print("Tabela OK.\n--------------------")
        return True
    except Exception as e:
        print(f"Erro ao criar/verificar tabela.\nErro: {e}\n--------------------")
        return False
    
def store(expense):
    print("Armazenando gasto...")
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        Value = expense["Value"]; Type = expense["Type"]; Date = expense["Date"]; Description = expense["Description"]
        cursor.execute("""
            INSERT INTO Expenses (Value, Type, Date, Description)
            VALUES (?, ?, ?, ?)
        """, (Value, Type, Date, Description))
        connection.commit()
        connection.close()
        print("Gasto armazenado com sucesso.\n--------------------")
        return "Gasto armazenado com sucesso."
    except Exception as e:
        print(f"Erro ao armazenar gasto.\nErro:{e}\n--------------------")
        return None
    
def getExpenses(date, nextDate):
    print("Mostrando gastos de um mês específico...")
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        sqlCommand = "SELECT Type, SUM(Value) FROM Expenses WHERE Date BETWEEN ? AND ? GROUP BY Type"
        cursor.execute(sqlCommand, (date, nextDate))
        results = cursor.fetchall()
        if not results:
            return "Nenhum gasto encontrado."
        output = ""
        for row in results:
            Value = f"{row[1]:.2f}".replace(".", ",")
            output += f"{row[0]}: R${Value}\n"
        sqlCommand = "SELECT SUM(Value) FROM Expenses WHERE Date BETWEEN ? AND ?"
        cursor.execute(sqlCommand, (date, nextDate))
        results = cursor.fetchone()
        Value = f"{results[0]:.2f}".replace(".", ",")
        output += f"Total: R${Value}"
        connection.close()
        return output
    except Exception as e:
        print(f"Erro ao mostrar os gastos de um mês específico.\nErro: {e}")
        return None
        
def showAll(Month, command):
    print("Buscando gastos...")
    try:
        date, nextDate = validations.validateDBDates(Month)
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        sqlCommand = "SELECT "
        if command == "2":
            sqlCommand += "Value, Type, Date, Description "
        elif command == "5":
            sqlCommand += "* "
        elif command == "3":
            sqlCommand += "Value, Type, Date, Description FROM Expenses WHERE Date BETWEEN ? AND ? ORDER BY Date ASC"
            cursor.execute(sqlCommand, (date, nextDate))
            results = cursor.fetchall()
            half = len(results) // 2
            results1 = results[:half]
            results2 = results[half:]
            connection.close()
            print("\nBusca feita.\n--------------------")
            return results1, results2
        elif command == "4":
            sqlCommand += "* FROM Expenses WHERE Date BETWEEN ? AND ? ORDER BY Date ASC"
            cursor.execute(sqlCommand, (date, nextDate))
            results = cursor.fetchall()
            half = len(results) // 2
            results1 = results[:half]
            results2 = results[half:]
            connection.close()
            print("\nBusca feita.\n--------------------")
            return results1, results2
        sqlCommand += "FROM Expenses WHERE Date BETWEEN ? AND ? ORDER BY Date ASC"
        cursor.execute(sqlCommand, (date, nextDate))
        results = cursor.fetchall()
        connection.close()
        print("\nBusca feita.\n--------------------")
        return results
    except Exception as e:
        print(f"Erro ao mostrar todos os gastos.\nErro: {e}")
        return None

def removeExpenses(IDs):
    print("Removendo gastos de um mês específico...")
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        for id in IDs:
            cursor.execute("""
                DELETE FROM Expenses 
                WHERE ID = ?
            """,(id,))
        connection.commit()
        connection.close()
        return True
    except Exception as e:
        print(f"Erro ao mostrar os gastos de um mês específico.\nErro: {e}")
        return None
