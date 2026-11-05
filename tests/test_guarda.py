"""Guarda contra perda de dados (pipeline/guarda.py): detecta itens que somem e ignora os que só mudam de valor."""
import os, sys
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "pipeline"))
import guarda  # noqa: E402

n = 0
ant = {"dias": [["2026-01-02", "VBBR3", 25.0], ["2026-06-30", "VBBR3", 29.89]],
       "series": {"2T26": {"CONS": {"v": 4499}}, "3T26": {"CONS": {"v": 1}}},
       "documentos": [{"protocolo": "123", "x": 1}, {"protocolo": "RAD-999", "x": 1}],
       "linhas": [{"cd_conta": "3.01", "2T26": 1}]}
# só valores corrigidos, itens novos e provisório do Plantão substituído pelo oficial: nada perdido
ok = {"dias": ant["dias"] + [["2026-11-04", "VBBR3", 29.25]], "series": {"2T26": {"CONS": {"v": 4500}}, "3T26": {"CONS": {"v": 2}}},
      "documentos": [{"protocolo": "123", "x": 2}, {"protocolo": "999", "x": 1}], "linhas": [{"cd_conta": "3.01", "2T26": 2, "3T26": 3}]}
assert guarda.perdidos(ant, ok) == [], guarda.perdidos(ant, ok); n += 1
# arquivo da B3 pela metade: pregões somem
assert guarda.perdidos(ant, dict(ok, dias=ant["dias"][:1])) == ["/dias[2026-06-30]"]; n += 1
# período inteiro some: conta uma vez, não com cada subcampo
s = dict(ok, series={"2T26": {"CONS": {"v": 1}}})
assert guarda.perdidos(ant, s) == ["/series/3T26"], guarda.perdidos(ant, s); n += 1
# conta some de um período publicado
assert guarda.perdidos(ant, dict(ok, linhas=[{"cd_conta": "3.01", "3T26": 3}])) == ["/linhas[3.01]/2T26"]; n += 1
# documento oficial some
assert guarda.perdidos(ant, dict(ok, documentos=[{"protocolo": "999"}])) == ["/documentos[123]"]; n += 1
print("TESTE GUARDA OK: %d conferências" % n)
