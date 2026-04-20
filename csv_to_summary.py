"""
csv_to_summary.py
-----------------
Le arquivos CSV e gera resumo estatistico completo.
Ideal para analise rapida de dados de obras e projetos ERP.

Autor: SkinDevX | https://github.com/SkinDevX
"""

import csv
import statistics
from pathlib import Path
from datetime import datetime


EXTENSION_MAP = {
    ".pdf": "documentos/pdf",
    ".docx": "documentos/word",
    ".xlsx": "planilhas",
    ".csv": "dados",
    ".dwg": "projetos/autocad",
    ".py": "scripts/python",
    ".sql": "scripts/sql",
}


def read_csv(file_path):
    """Le um CSV e retorna headers e rows como lista de dicts."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Arquivo nao encontrado: {file_path}")
    with open(path, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        rows = list(reader)
    return headers, rows


def detect_numeric_columns(headers, rows):
    """Detecta colunas numericas automaticamente."""
    numeric = []
    for col in headers:
        values = [r[col] for r in rows if r.get(col, "").strip()]
        try:
            [float(v.replace(",", ".").replace("R$", "").strip()) for v in values[:20]]
            numeric.append(col)
        except (ValueError, AttributeError):
            pass
    return numeric


def summarize(file_path):
    """Gera resumo estatistico do CSV."""
    headers, rows = read_csv(file_path)
    total_rows = len(rows)
    numeric_cols = detect_numeric_columns(headers, rows)

    summary = {
        "arquivo": Path(file_path).name,
        "gerado_em": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "total_linhas": total_rows,
        "total_colunas": len(headers),
        "colunas": headers,
        "colunas_numericas": numeric_cols,
        "estatisticas": {},
    }

    for col in numeric_cols:
        values = []
        for row in rows:
            try:
                val = float(row[col].replace(",", ".").replace("R$", "").strip())
                values.append(val)
            except (ValueError, AttributeError, KeyError):
                pass

        if values:
            summary["estatisticas"][col] = {
                "min": min(values),
                "max": max(values),
                "media": round(statistics.mean(values), 2),
                "mediana": round(statistics.median(values), 2),
                "soma": round(sum(values), 2),
                "total_valores": len(values),
                "nulos": total_rows - len(values),
            }

    return summary


def print_summary(summary):
    """Exibe o resumo formatado."""
    sep = "=" * 55
    print(f"\n{sep}")
    print(f"  RESUMO: {summary['arquivo']}")
    print(f"  Gerado em: {summary['gerado_em']}")
    print(sep)
    print(f"  Linhas  : {summary['total_linhas']:,}")
    print(f"  Colunas : {summary['total_colunas']}")
    print(f"  Colunas numericas: {len(summary['colunas_numericas'])}")

    if summary["estatisticas"]:
        print(f"\n  ESTATISTICAS POR COLUNA")
        print(f"{'─' * 55}")
        for col, s in summary["estatisticas"].items():
            print(f"\n  {col}")
            print(f"     Soma    : {s['soma']:>15,.2f}")
            print(f"     Media   : {s['media']:>15,.2f}")
            print(f"     Min/Max : {s['min']:>,.2f} / {s['max']:>,.2f}")
    print(f"\n{sep}\n")


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Uso: python csv_to_summary.py <arquivo.csv>")
        sys.exit(1)
    result = summarize(sys.argv[1])
    print_summary(result)

