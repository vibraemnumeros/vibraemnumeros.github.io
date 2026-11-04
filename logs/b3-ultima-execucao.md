# B3 — última execução

Executado em 2026-11-04 23:50 UTC

- anos reaproveitados do arquivo anterior: 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025
- 2026 https://bvmf.bmfbovespa.com.br/InstDados/SerHist/COTAHIST_A2026.ZIP → ok (HTTP 200, 66304000 bytes)
- 2026: erro ao ler o arquivo (provável download incompleto); mantidos os 209 pregões já gravados
```
Traceback (most recent call last):
  File "/home/runner/work/vibraemnumeros.github.io/vibraemnumeros.github.io/pipeline/b3.py", line 136, in main
    regs = le_zip(conteudo)
           ^^^^^^^^^^^^^^^^
  File "/home/runner/work/vibraemnumeros.github.io/vibraemnumeros.github.io/pipeline/b3.py", line 62, in le_zip
    with zipfile.ZipFile(io.BytesIO(conteudo)) as z:
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.12.15/x64/lib/python3.12/zipfile/__init__.py", line 1396, in __init__
    self._RealGetContents()
  File "/opt/hostedtoolcache/Python/3.12.15/x64/lib/python3.12/zipfile/__init__.py", line 1463, in _RealGetContents
    raise BadZipFile("File is not a zip file")
zipfile.BadZipFile: File is not a zip file

```
- diário 2026-11-04 → ok (2 registros da Vibra/BOVA11)
- diário 2026-11-05 → ainda não publicado

Dias com cotação: 2207
Primeiro: 2017-12-15 (BRDT3) · último: 2026-11-04 (VBBR3) a R$ 29.25
Anos sem arquivo ou com erro: 1
