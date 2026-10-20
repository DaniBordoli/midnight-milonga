# Midnight Milonga

Slot 5x4, 1024 formas de ganar, para Stake Engine (proveedor: Pampa Play).

## Estructura

- `math/`: Math SDK de Stake Engine con el juego en `math/games/midnight_milonga/`.
- `web/`: Web SDK (todavía no está; se suma en la etapa del front).

## Math

Requisitos: Python 3.12+ y Rust/Cargo (lo usa el optimizador).

```bash
cd math
python -m venv env
env\Scripts\python.exe -m pip install -r requirements.txt
env\Scripts\python.exe -m pip install -e .
```

Correr (desde `math/`, con `%USERPROFILE%\.cargo\bin` en el PATH):

```bash
env\Scripts\python.exe games\midnight_milonga\run.py debug
env\Scripts\python.exe games\midnight_milonga\run.py
env\Scripts\python.exe games\midnight_milonga\tools\stake_report.py
```

- `debug`: 500 jugadas por modo, sin comprimir y sin optimizar. Después se puede correr `tools\analyze_debug.py` para ver promedios por criterio.
- Sin argumentos: 100.000 jugadas por modo, optimización, análisis y chequeos de formato. Tarda unos 40 minutos.
- `stake_report.py`: compara las tablas publicadas con los chequeos de Stake y escribe `library/stake_report.md`.

Lo que se sube a Studio queda en `math/games/midnight_milonga/library/publish_files/`.

Si se cambian las tiras de rodillos, hay que editar `reels/generate_reels.py` y correrlo de nuevo.
