# 📅 Sistema de Escala Automatizada

Aplicação em Python para gestão e automação de escalas operacionais, integrada ao Google Sheets, permitindo controle de disponibilidade e redução de conflitos na organização de plantões.

---

## 💡 Contexto Real

Este projeto foi inspirado em um fluxo real de organização de escalas, onde parte das regras já é automatizada via Google Sheets, mas a alocação manual ainda representa um gargalo operacional.

---

## 🎯 Objetivo

Facilitar e otimizar o processo de organização de escalas, permitindo:

- Atualização centralizada de datas de plantão
- Controle de férias e indisponibilidade
- Redução de erros manuais
- Integração com planilhas já utilizadas no dia a dia

---

## 🛠️ Tecnologias

- Python  
- Tkinter (interface gráfica)  
- Google Sheets API (gspread)  
- Google Auth (service account)  
- tkcalendar  

---

## 📚 Funcionalidades

- Seleção e edição de dados de plantão por colaborador  
- Controle visual de férias e ausências (por dia)  
- Interface interativa para manipulação dos dados  
- Integração direta com Google Sheets  
- Sistema de cache para evitar limitações da API  
- Busca inteligente de nomes na interface  

---

## 🧠 Problema Resolvido

A organização de escalas operacionais é frequentemente feita de forma manual, o que pode gerar:

- conflitos de agenda  
- inclusão de pessoas indisponíveis  
- retrabalho constante  

Este sistema centraliza e facilita a gestão dessas informações, tornando o processo mais rápido e confiável.

---

## 🔐 Configuração (ANTES de rodar)

Antes de executar o projeto, é necessário configurar o acesso ao Google Sheets:

1. Criar credenciais no Google Cloud (Service Account)  
2. Baixar o arquivo JSON de credenciais  
3. Compartilhar a planilha com o e-mail da credencial  
4. Colocar o arquivo JSON na raiz do projeto  

  ⚠️ O arquivo de credenciais **não está incluído no repositório por segurança**

---

## ▶️ Como executar

Clone o repositório:

```bash
git clone https://github.com/seu-usuario/sistema-escala-tkinter.git
cd sistema-escala-tkinter
pip install -r requirements.txt
python app.py
