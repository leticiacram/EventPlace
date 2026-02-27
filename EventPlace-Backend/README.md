# 🏟️ EventPlace – Agregador e Comparador de Espaços

O **EventPlace** é uma plataforma backend desenvolvida em Python que centraliza informações de diferentes salões de festas e salas de reunião. O sistema permite o cadastro de proprietários, busca avançada por filtros e um motor de comparação de custo-benefício entre locais selecionados.

---

## 🚀 Sobre o Projeto

Este projeto foi desenvolvido para a disciplina de **Projeto Prático Integrado – Aplicação Orientada a Objetos**, no 3º semestre do curso de Ciência da Computação. 

O foco principal é a aplicação dos pilares da **Programação Orientada a Objetos (POO)** para resolver o problema de fragmentação na busca por espaços de eventos.

### ✨ Funcionalidades Principais
- **Cadastro de Perfis:** Distinção entre Proprietários e Clientes.
- **Gerenciamento de Espaços:** Suporte para diferentes tipos de imóveis (Salões, Salas de Reunião, etc.) via Herança.
- **Motor de Comparação:** Comparação técnica lado a lado de infraestrutura e preço.
- **Cálculo de Orçamento:** Sistema polimórfico de cálculo baseado em participantes ou horas.
- **Persistência de Dados:** Armazenamento local em formato JSON.

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** [Python 3.12+](https://www.python.org/)
- **Paradigma:** Orientação a Objetos (Classes, Herança, Encapsulamento, Polimorfismo).
- **Armazenamento:** JSON (Persistência local).
- **Versionamento:** Git & GitHub.

---

## 📂 Estrutura do Repositório

```text
├── src/
│   ├── modelos.py        # Definição das classes (Espaco, Salão, Proprietário)
│   ├── logica.py         # Motor de comparação e cálculos financeiros
│   ├── armazenamento.py  # Manipulação do arquivo JSON
│   └── main.py           # Interface de usuário e menu principal
├── data/
│   └── dados.json        # Banco de dados local
├── docs/                 # Documentação e diagramas UML
└── README.md             # Documentação principal
