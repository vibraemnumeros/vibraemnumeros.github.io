#!/usr/bin/env python3
"""Guarda contra perda de dados: nenhuma atualização pode apagar o que o painel já tinha.

Roda depois de todas as coletas e antes de gravar no repositório. Compara cada data/*.json com a versão já publicada
(HEAD) e lista os itens que sumiram: chaves de dicionário (contas, períodos, séries) e itens de listas identificados pela
data, período, protocolo ou id. Fonte que falha, arquivo baixado pela metade ou mudança de formato na origem aparecem
aqui como itens perdidos. Nesse caso o arquivo volta à versão anterior (o painel continua com os dados bons), o motivo
fica em logs/guarda.md e um aviso é gravado em guarda-alerta.md para abrir o alerta no GitHub.

Itens que somem por natureza não contam: a janela móvel do Plantão da B3, os documentos provisórios do Plantão
substituídos pelo registro oficial (protocolo "RAD-…") e os arquivos de controle.

Uso: python pipeline/guarda.py [--ref HEAD]
"""
import argparse
import datetime as dt
import glob
import json
import os
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IGNORAR = {"plantao.json", "links.json", "auditoria.json", "cvm_status.json"}
IDS = ("cd_conta", "id", "data", "periodo", "protocolo", "chave", "dt_refer", "nsd")
PROFUNDIDADE = 5


def chaves(o, pre="", out=None, prof=0):
    """Conjunto de caminhos que identificam o conteúdo (sem os valores): o que existe, não quanto vale."""
    if out is None:
        out = set()
    if prof > PROFUNDIDADE:
        return out
    if isinstance(o, dict):
        for k, v in o.items():
            p = pre + "/" + str(k)
            out.add(p)
            chaves(v, p, out, prof + 1)
    elif isinstance(o, list):
        for x in o:
            if isinstance(x, list) and x and isinstance(x[0], (str, int)):
                k = str(x[0])
            elif isinstance(x, dict):
                k = next((str(x[i]) for i in IDS if i in x), None)
                if k is None:
                    continue
            else:
                continue
            p = pre + "[" + k + "]"
            out.add(p)
            if isinstance(x, dict):
                chaves(x, p, out, prof + 1)
    return out


def perdidos(antes, depois):
    """Itens que existiam e sumiram, só no nível mais alto (um período perdido conta uma vez, não com cada subcampo)."""
    p = {k for k in chaves(antes) - chaves(depois) if "RAD-" not in k}
    def pai_perdido(k):
        for i in range(len(k) - 1, 0, -1):
            if k[i] in "/[" and k[:i] in p:
                return True
        return False
    return sorted(k for k in p if not pai_perdido(k))


def versao(ref, rel):
    r = subprocess.run(["git", "show", "%s:%s" % (ref, rel)], cwd=RAIZ, capture_output=True)
    if r.returncode != 0:
        return None, None
    return r.stdout, json.loads(r.stdout.decode("utf-8"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ref", default="HEAD")
    a = ap.parse_args()
    log = ["# Guarda contra perda de dados — última execução", "",
           "Executado em %s UTC" % dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M"), ""]
    restaurados = []
    for caminho in sorted(glob.glob(os.path.join(RAIZ, "data", "*.json"))):
        nome = os.path.basename(caminho)
        if nome in IGNORAR:
            continue
        rel = "data/" + nome
        try:
            bruto_ant, ant = versao(a.ref, rel)
        except ValueError:
            continue
        if ant is None:
            continue
        try:
            novo = json.load(open(caminho, encoding="utf-8"))
        except ValueError as e:
            novo, perd = None, ["(arquivo novo ilegível: %s)" % e]
        if novo is not None:
            perd = perdidos(ant, novo)
        if perd:
            open(caminho, "wb").write(bruto_ant)
            restaurados.append((nome, perd))
            log.append("- **%s**: %d item(ns) sumiram em relação à versão publicada; mantida a versão anterior. Exemplos: %s"
                       % (nome, len(perd), ", ".join(perd[:5])))
    if not restaurados:
        log.append("Nenhum dado perdido: todas as atualizações só acrescentaram ou corrigiram valores.")
    open(os.path.join(RAIZ, "logs", "guarda.md"), "w", encoding="utf-8").write("\n".join(log) + "\n")
    alerta = os.path.join(RAIZ, "guarda-alerta.md")
    if restaurados:
        txt = ["A atualização de %s trouxe arquivo(s) com menos dados do que a versão publicada. Para não publicar dados "
               "incompletos, esses arquivos voltaram à versão anterior; o restante da atualização seguiu normalmente." % dt.date.today().strftime("%d/%m/%Y"), ""]
        txt += ["- %s: %d item(ns) a menos (ex.: %s)" % (n, len(p), ", ".join(p[:3])) for n, p in restaurados]
        txt += ["", "Causa mais comum: a fonte (CVM ou B3) respondeu com arquivo incompleto; a próxima atualização tenta de novo. "
                "Se o aviso se repetir por vários dias com os mesmos itens, a fonte mudou de fato e o pipeline precisa de revisão."]
        open(alerta, "w", encoding="utf-8").write("\n".join(txt) + "\n")
    elif os.path.exists(alerta):
        os.remove(alerta)
    if os.environ.get("GITHUB_OUTPUT"):
        open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8").write("restaurados=%d\n" % len(restaurados))
    print("\n".join(log[4:]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
