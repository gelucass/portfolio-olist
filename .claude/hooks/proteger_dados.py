#!/usr/bin/env python3
"""Hook PreToolUse: impede o Claude de ler arquivos ou rodar comandos listados em .claude/governanca.json.

Recebe a chamada de ferramenta em JSON pelo stdin. Sai com código 2 (bloqueia e explica ao Claude)
quando a chamada toca um caminho ou comando protegido; com 0 (libera) nos demais casos.
"""
import fnmatch
import json
import os
import re
import sys
from pathlib import Path

projeto = Path(os.environ.get("CLAUDE_PROJECT_DIR", Path(__file__).resolve().parents[2]))
config = json.loads((projeto / ".claude" / "governanca.json").read_text())
chamada = json.load(sys.stdin)
ferramenta, entrada = chamada.get("tool_name", ""), chamada.get("tool_input", {})


def caminho_protegido(caminho):
    # Caminho relativo é resolvido a partir do diretório da sessão; a barra final cobre a própria pasta.
    alvo = Path(caminho).expanduser()
    if not alvo.is_absolute():
        alvo = Path(chamada.get("cwd") or os.getcwd()) / alvo
    alvo = str(alvo)
    return next((p for p in config["caminhos_bloqueados"]
                 if fnmatch.fnmatch(alvo, p) or fnmatch.fnmatch(alvo + "/", p)), None)


def bloquear(motivo):
    print(f"Bloqueado pela governança de dados ({motivo}). Trabalhe só com a estrutura ou com dados "
          "sintéticos; veja a skill dados-confidenciais.", file=sys.stderr)
    sys.exit(2)


if ferramenta in ("Read", "Edit", "Write", "NotebookEdit"):
    alvo = entrada.get("file_path") or entrada.get("notebook_path") or ""
    if (p := caminho_protegido(alvo)):
        bloquear(f"caminho {alvo} bate com {p}")

elif ferramenta in ("Grep", "Glob"):
    alvo = entrada.get("path") or ""
    if alvo and (p := caminho_protegido(alvo)):
        bloquear(f"busca em {alvo} bate com {p}")

elif ferramenta == "Bash":
    comando = entrada.get("command", "")
    for c in config["comandos_bloqueados"]:
        if re.search(rf"(^|[\s;|&(]){re.escape(c)}(\s|$)", comando):
            bloquear(f"comando {c}")
    for palavra in re.split(r"[\s;|&<>()'\"=]+", comando):
        if palavra and (p := caminho_protegido(palavra)):
            bloquear(f"o comando cita {palavra}, que bate com {p}")

sys.exit(0)
