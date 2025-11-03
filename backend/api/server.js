const express = require('express');
const cors = require('cors');
const sqlite3 = require('sqlite3').verbose();

const app = express();
app.use(cors()); // Habilita o CORS
const port = 5000; // Porta onde seu backend vai rodar

const DB_PATH = '../database/ExpensesTable.db';

// --- Helper Function ---
function formatarDataParaSQL(data) {
  const ano = data.getFullYear();
  const mes = String(data.getMonth() + 1).padStart(2, '0'); 
  const dia = String(data.getDate()).padStart(2, '0');
  return `${ano}-${mes}-${dia}`;
}

// --- ROTA 1: Pegar TODOS os gastos ---
app.get('/api/gastos/todos', (req, res) => {
  const db = new sqlite3.Database(DB_PATH, (err) => {
    if (err) {
      console.error(err.message);
      return res.status(500).json({ error: err.message });
    }
  });

  db.all("SELECT * FROM Expenses ORDER BY Date ASC", [], (err, rows) => {
    if (err) {
      console.error(err.message);
      return res.status(500).json({ error: err.message });
    }
    res.json({ data: rows });
  });

  db.close((err) => {
    if (err) {
      console.error(err.message);
    }
  });
});

// --- ROTA 2: Filtro do Mês (Enviando TODOS os itens) ---
app.get('/api/gastos/mes-atual', (req, res) => {
  const hoje = new Date(); 
  const dataInicio = new Date(hoje.getFullYear(), hoje.getMonth(), 2);
  const dataFim = new Date(hoje.getFullYear(), hoje.getMonth() + 1, 1);
  const dataInicioSQL = formatarDataParaSQL(dataInicio);
  const dataFimSQL = formatarDataParaSQL(dataFim);

  const db = new sqlite3.Database(DB_PATH, (err) => {
    if (err) {
      console.error(err.message);
      return res.status(500).json({ error: err.message });
    }
  });

  // --- MUDANÇA: Voltamos ao "SELECT *" ---
  // Agora ele vai retornar todos os 4 itens de "Compras"
  const sql = `
    SELECT * FROM Expenses 
    WHERE Date BETWEEN ? AND ?
    ORDER BY Date ASC
  `;
  
  db.all(sql, [dataInicioSQL, dataFimSQL], (err, rows) => {
    if (err) {
      console.error(err.message);
      return res.status(500).json({ error: err.message });
    }
    res.json({
      info: {
        filtro_inicio: dataInicioSQL,
        filtro_fim: dataFimSQL
      },
      data: rows 
    });
  });

  db.close((err) => {
    if (err) {
      console.error(err.message);
    }
  });
});


// Ligar o servidor
app.listen(port, () => {
  console.log(`Backend rodando em http://localhost:${port}`);
  console.log('Rotas disponíveis:');
  console.log(`http://localhost:${port}/api/gastos/todos`);
  console.log(`http://localhost:${port}/api/gastos/mes-atual`);
});

