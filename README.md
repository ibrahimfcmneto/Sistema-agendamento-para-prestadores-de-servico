# Sistema-agendamento-paraprestadores-de-serviço
# 📅 MicroERP de Agendamento Inteligente (Agendamento-SI)

### Status do Projeto: 🚧 Em Desenvolvimento (MVP - Mínimo Produto Viável)

**Desenvolvido como projeto prático e de portfólio no curso de Sistemas de Informação (PUC-Campinas).**

---

## Sobre o Projeto

O **Agendamento-SI** é um sistema de gestão de agendamentos e presença (*Micro-ERP*) focado em otimizar as operações de **pequenos prestadores de serviço** (ex: barbearias, salões, clínicas independentes).

O principal objetivo de negócio é **reduzir a taxa de *no-show*** (clientes faltosos) e fornecer ao gestor **dados acionáveis** para melhorar a eficiência operacional.

### Valor de Negócio (Foco em SI)

* **Redução de Perdas:** Fornece um mecanismo para registrar e analisar as faltas, ajudando o gestor a tomar decisões sobre a política de cancelamento.
* **Decisão Baseada em Dados (BI):** Apresenta um Dashboard de KPI's (Taxa de No-Show, Serviços Mais Vendidos) essencial para a gestão.
* **Otimização de Processos:** Automatiza a visualização da agenda e prepara a base para futuros lembretes automáticos.

---

## Funcionalidades do MVP

O MVP está focado nas seguintes funcionalidades essenciais para a área administrativa:

1.  **Autenticação e Controle de Acesso:** Login seguro para o gestor.
2.  **CRUD de Clientes e Serviços:** Gerenciamento completo de cadastro de usuários e dos serviços oferecidos (com preço e duração).
3.  **Agendamento Simplificado:** Criação, edição e exclusão de novos agendamentos pelo painel administrativo.
4.  **Status de Presença:** Marcação de agendamentos como `Concluído`, `Cancelado` ou `Falta`.
5.  **Dashboard Gerencial:** Visualização de métricas (KPIs), incluindo o cálculo da **Taxa de No-Show**.

---

## Stack Tecnológica

Esta *stack* foi escolhida para demonstrar proficiência em tecnologias modernas e amplamente utilizadas no mercado de São Paulo.

| Categoria | Tecnologia | Justificativa no Portfólio |
| :--- | :--- | :--- |
| **Back-end** | Python (Flask) | Leveza, prototipagem rápida e excelente para integrar módulos de análise de dados futuros. |
| **Banco de Dados** | PostgreSQL | Robustez e padrão de mercado para aplicações com escalabilidade. |
| **Front-end / UI** | HTML, CSS e JavaScript (Bootstrap) | Foco na funcionalidade e interface limpa (utilizando Bootstrap para agilizar o desenvolvimento UI/UX). |
| **Segurança** | Python-dotenv (Variáveis de Ambiente) | Prática de segurança essencial (uso do arquivo `.env` e `.gitignore`). |
| **Próxima Etapa** | Integração Twilio/WhatsApp (Simulada) | Demonstração de integração com APIs externas e serviços de Cloud. |

---

## Configuração do Ambiente de Desenvolvimento

Para rodar este projeto em sua máquina local, siga os passos abaixo:

### Pré-requisitos

* Python 3.x instalado.
* PostgreSQL instalado e rodando.
* Conhecimento básico de Git.

### Passos de Instalação

1.  **Clone o Repositório:**
    ```bash
    git clone [https://github.com/SeuUsuario/MicroERP-Agendamento-Service.git](https://github.com/SeuUsuario/MicroERP-Agendamento-Service.git)
    cd MicroERP-Agendamento-Service
    ```
2.  **Crie e Ative o Ambiente Virtual:**
    ```bash
    python -m venv venv
    # Para Linux/macOS
    source venv/bin/activate
    # Para Windows
    venv\Scripts\activate
    ```
3.  **Instale as Dependências:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configure as Variáveis de Ambiente:**
    Crie um arquivo chamado `.env` na raiz do projeto e adicione suas credenciais (este arquivo é ignorado pelo Git por segurança):
    ```env
    # Exemplo de conteúdo do arquivo .env
    SECRET_KEY="sua_chave_secreta_aqui"
    DATABASE_URL="postgresql://user:senha@localhost:5432/nomedobanco"
    ```
5.  **Inicialize o Banco de Dados e Rode o Servidor:**
    *(Estes comandos serão adicionados aqui após definirmos a estrutura inicial do Flask/SQLAlchemy)*

---

## Contribuições e Licença

Este é um projeto de portfólio pessoal e está licenciado sob a **Licença MIT**.

**Desenvolvedor:** [Ibrahim Fleury de Camargo Madeira Neto]
**LinkedIn:** [Ifleuryneto]
