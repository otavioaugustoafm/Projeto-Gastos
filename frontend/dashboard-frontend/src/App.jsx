import React, { useState, useEffect } from 'react';
import axios from 'axios';
// ResponsiveContainer é importante para o gráfico se ajustar
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';

// --- NOVA FUNÇÃO ---
// Esta função vai processar os dados que chegam da API
function processarDadosParaGrafico(dados) {
  // 1. Usamos um objeto para somar os valores
  const agregador = {}; // Ex: { Compras: 474, Extra: 50 }

  // Itera sobre cada item (gasto) que veio da API
  dados.forEach(item => {
    const tipo = item.Type;
    const valor = item.Value; // Lembre-se, este valor é INTEIRO (79, 93, etc)

    if (agregador[tipo]) {
      // Se já vimos "Compras", somamos o valor
      agregador[tipo] += valor;
    } else {
      // Se é a primeira vez, criamos a chave
      agregador[tipo] = valor;
    }
  });

  // 2. Transformamos o objeto em um array que o Recharts entende
  // De: { Compras: 474 }
  // Para: [ { Type: "Compras", TotalValue: 474 } ]
  const dadosAgregados = Object.keys(agregador).map(tipo => ({
    Type: tipo,
    TotalValue: agregador[tipo]
  }));

  console.log("Dados agregados pelo JS:", dadosAgregados);
  return dadosAgregados;
}


function App() {
  // State para os dados processados (para o gráfico)
  const [gastosAgregados, setGastosAgregados] = useState([]);
  // State para o número de registros individuais
  const [totalRegistros, setTotalRegistros] = useState(0);

  useEffect(() => {
    // Busca os dados INDIVIDUAIS do mês
    axios.get('http://localhost:5000/api/gastos/mes-atual')
      .then(response => {
        const dadosCrus = response.data.data;
        console.log("Dados crus recebidos:", dadosCrus);
        
        // Guarda o número de registros individuais
        setTotalRegistros(dadosCrus.length); 

        // --- MUDANÇA AQUI ---
        // Processamos os dados ANTES de salvar no state do gráfico
        const dadosProcessados = processarDadosParaGrafico(dadosCrus);
        setGastosAgregados(dadosProcessados);
      })
      .catch(error => {
        console.error("Erro ao buscar dados:", error);
      });
  }, []); // O [] faz rodar só uma vez

  return (
    // Dando um padding para ficar mais bonito
    <div style={{ width: '90%', margin: '20px' }}>
      <h1>Meu Dashboard</h1>
      <p>Registros individuais carregados: {totalRegistros}</p>
      
      <ResponsiveContainer width="100%" height={400}>
        <BarChart 
          data={gastosAgregados} // Usamos os dados processados
          margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          
          {/* O Eixo X agora lê a propriedade "Type" */}
          <XAxis dataKey="Type" />
          
          <YAxis />
          <Tooltip />
          
          {/* A Barra agora lê a propriedade "TotalValue" */}
          <Bar dataKey="TotalValue" fill="#8884d8" name="Total Gasto" />
          
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

export default App;

