# B3 — última execução

Executado em 2026-11-04 23:45 UTC

- anos reaproveitados do arquivo anterior: 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025
- 2026 https://bvmf.bmfbovespa.com.br/InstDados/SerHist/COTAHIST_A2026.ZIP → ok (HTTP 200, 66304000 bytes)
- 2026: erro ao ler o arquivo
```
Traceback (most recent call last):
  File "/home/runner/work/vibraemnumeros.github.io/vibraemnumeros.github.io/pipeline/b3.py", line 135, in main
    for d, t, fech, vol, neg in le_zip(conteudo):
                                ^^^^^^^^^^^^^^^^
  File "/home/runner/work/vibraemnumeros.github.io/vibraemnumeros.github.io/pipeline/b3.py", line 62, in le_zip
    with zipfile.ZipFile(io.BytesIO(conteudo)) as z:
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.12.16/x64/lib/python3.12/zipfile/__init__.py", line 1396, in __init__
    self._RealGetContents()
  File "/opt/hostedtoolcache/Python/3.12.16/x64/lib/python3.12/zipfile/__init__.py", line 1463, in _RealGetContents
    raise BadZipFile("File is not a zip file")
zipfile.BadZipFile: File is not a zip file

```
- diário 2025-12-31 → ainda não publicado
- diário 2026-01-01 → ainda não publicado
- diário 2026-01-02 → ok (2 registros da Vibra/BOVA11)
- diário 2026-01-05 → ok (2 registros da Vibra/BOVA11)
- diário 2026-01-06 → ok (2 registros da Vibra/BOVA11)
- diário 2026-01-07 → ok (2 registros da Vibra/BOVA11)
- diário 2026-01-08 → ok (2 registros da Vibra/BOVA11)
- diário 2026-01-09 → ok (2 registros da Vibra/BOVA11)

Dias com cotação: 2003
Primeiro: 2017-12-15 (BRDT3) · último: 2026-01-09 (VBBR3) a R$ 25.53
Anos sem arquivo ou com erro: 1
