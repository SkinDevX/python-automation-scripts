# 🐍 Python Automation Scripts

> Scripts de automação, análise de dados e workflows com IA — por **SkinDevX**

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-4479A1?style=for-the-badge&logo=postgresql&logoColor=white)
![AI](https://img.shields.io/badge/AI%20Agents-412991?style=for-the-badge&logo=openai&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)

---

## 📁 Estrutura do Repositório

```
python-automation-scripts/
├── 📂 data_analysis/
│   ├── sql_report_generator.py     # Gera relatórios a partir de queries SQL
│   └── csv_to_summary.py          # Sumariza dados de CSVs automaticamente
├── 📂 ai_workflows/
│   ├── llm_task_agent.py          # Agente de tarefas com LLM
│   └── doc_auto_classifier.py     # Classificador automático de documentos
├── 📂 erp_utils/
│   ├── erp_data_sync.py           # Sincronização de dados ERP
│   └── report_scheduler.py        # Agendador de relatórios automáticos
└── 📂 automation/
    ├── file_organizer.py           # Organizador automático de arquivos
    └── batch_processor.py         # Processamento em lote de dados
```

---

## 🚀 Scripts em Destaque

### 📊 `sql_report_generator.py`
Conecta a qualquer banco SQL (SQLite, PostgreSQL, MySQL) e gera relatórios formatados em CSV/Excel automaticamente a partir de queries parametrizadas.

```python
# Uso básico
from data_analysis.sql_report_generator import ReportGenerator

rg = ReportGenerator(connection_string="sqlite:///database.db")
rg.generate(query="SELECT * FROM projetos WHERE status = 'ativo'",
            output="relatorio_projetos.xlsx")
```

### 🤖 `llm_task_agent.py`
Agente autônomo que usa LLMs (Claude / GPT) para executar tarefas de engenharia: análise de documentos, geração de relatórios e resposta a perguntas sobre dados.

```python
# Uso básico
from ai_workflows.llm_task_agent import TaskAgent

agent = TaskAgent(model="claude-3-5-sonnet")
result = agent.run("Analise os dados de produção e identifique gargalos")
print(result)
```

### 📁 `file_organizer.py`
Organiza automaticamente pastas de projeto por tipo, data e categoria. Útil para gerenciar documentação técnica de obras e projetos.

```python
# Uso básico
from automation.file_organizer import FileOrganizer

fo = FileOrganizer(source_dir="./downloads")
fo.organize(rules={"pdf": "documentos", "xlsx": "planilhas", "dwg": "projetos"})
```

---

## ⚙️ Requisitos

```bash
pip install pandas sqlalchemy openpyxl requests anthropic
```

---

## 📌 Casos de Uso Principais

- **ERP & Dados** — Extração, transformação e carga de dados de sistemas ERP
- **Relatórios Automáticos** — Geração de relatórios técnicos a partir de SQL
- **AI Workflows** — Automação de tarefas repetitivas com agentes de IA
- **Gestão de Arquivos** — Organização automática de documentação de projetos

---

## 📬 Contato

[![Portfolio](https://img.shields.io/badge/Portfolio-skindevx.github.io-00f5d4?style=flat-square)](https://skindevx.github.io)
[![GitHub](https://img.shields.io/badge/GitHub-SkinDevX-181717?style=flat-square&logo=github)](https://github.com/SkinDevX)

---

<p align="center">
  <i>"Automate the boring. Build the meaningful."</i><br>
  <b>SkinDevX</b>
</p>
