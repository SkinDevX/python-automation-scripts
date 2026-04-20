"""
file_organizer.py
-----------------
Organiza automaticamente arquivos de uma pasta por tipo, extensão e data.
Útil para gerenciar documentação técnica de obras e projetos de engenharia.

Autor: SkinDevX
GitHub: https://github.com/SkinDevX
"""

import os
import shutil
from pathlib import Path
from datetime import datetime


# Mapeamento de extensões para categorias
EXTENSION_MAP = {
    # Documentos
    ".pdf": "documentos/pdf",
    ".docx": "documentos/word",
    ".doc": "documentos/word",
    ".xlsx": "planilhas",
    ".xls": "planilhas",
    ".csv": "dados",
    # Projetos técnicos
    ".dwg": "projetos/autocad",
    ".dxf": "projetos/autocad",
    ".rvt": "projetos/revit",
    ".ifc": "projetos/bim",
    # Imagens
    ".jpg": "imagens",
    ".jpeg": "imagens",
    ".png": "imagens",
    # Código
    ".py": "scripts/python",
    ".sql": "scripts/sql",
    ".js": "scripts/javascript",
    # Comprimidos
    ".zip": "arquivos",
    ".rar": "arquivos",
}


def get_category(file_path: Path) -> str:
    """Retorna a categoria baseada na extensão do arquivo."""
    ext = file_path.suffix.lower()
    return EXTENSION_MAP.get(ext, "outros")


def organize_folder(
    source_dir: str,
    dest_dir: str = None,
    dry_run: bool = False,
    by_date: bool = False,
) -> dict:
    """
    Organiza arquivos de uma pasta em subpastas por tipo.

    Args:
        source_dir: Pasta de origem com os arquivos
        dest_dir: Pasta de destino (usa source_dir se não informado)
        dry_run: Se True, apenas simula sem mover arquivos
        by_date: Se True, agrupa também por ano/mês

    Returns:
        Dicionário com estatísticas da operação
    """
    source = Path(source_dir)
    dest = Path(dest_dir) if dest_dir else source

    if not source.exists():
        raise FileNotFoundError(f"Pasta não encontrada: {source_dir}")

    stats = {"moved": 0, "skipped": 0, "errors": 0, "categories": {}}

    for file_path in source.iterdir():
        if not file_path.is_file():
            continue

        category = get_category(file_path)

        if by_date:
            mod_time = datetime.fromtimestamp(file_path.stat().st_mtime)
            target_dir = dest / category / str(mod_time.year) / f"{mod_time.month:02d}"
        else:
            target_dir = dest / category

        target_file = target_dir / file_path.name

        # Evita sobrescrever arquivos existentes
        if target_file.exists():
            base = target_file.stem
            suffix = target_file.suffix
            counter = 1
            while target_file.exists():
                target_file = target_dir / f"{base}_{counter}{suffix}"
                counter += 1

        try:
            if not dry_run:
                target_dir.mkdir(parents=True, exist_ok=True)
                shutil.move(str(file_path), str(target_file))

            stats["moved"] += 1
            stats["categories"][category] = stats["categories"].get(category, 0) + 1
            print(f"{'[SIMULADO] ' if dry_run else ''}Movido: {file_path.name} → {category}/")

        except Exception as e:
            stats["errors"] += 1
            print(f"Erro ao mover {file_path.name}: {e}")

    return stats


def print_summary(stats: dict) -> None:
    """Exibe um resumo da operação."""
    print("\n" + "=" * 50)
    print(f"✅ Arquivos organizados: {stats['moved']}")
    print(f"⚠️  Erros: {stats['errors']}")
    if stats["categories"]:
        print("\nDistribuição por categoria:")
        for cat, count in sorted(stats["categories"].items()):
            print(f"  {cat:<30} {count:>3} arquivo(s)")
    print("=" * 50)


# ──────────────────────────────────────────────
# Exemplo de uso
# ──────────────────────────────────────────────
if __name__ == "__main__":
    import sys

    # Pasta padrão: Downloads do usuário
    source = sys.argv[1] if len(sys.argv) > 1 else str(Path.home() / "Downloads")

    print(f"📁 Organizando pasta: {source}")
    print("   (simulação — nenhum arquivo será movido)\n")

    stats = organize_folder(
        source_dir=source,
        dry_run=True,   # Mude para False para executar de verdade
        by_date=False,
    )

    print_summary(stats)

