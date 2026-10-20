Midnight Milonga - reglas implementadas en la math

Tablero: 5 rodillos x 4 filas, 1024 formas de ganar, de izquierda a derecha, desde 3 rodillos seguidos.
Premios en múltiplos de la apuesta total, por forma de ganar (paytable en game_config.py).

Símbolos
- H1 bandoneón, H2 rosa, H3 fedora, H4 champagne; L1-L4 pica, corazón, diamante, trébol.
- BM Bailarín (wild, solo rodillos 1-2) y BF Bailarina (wild, solo rodillos 4-5).
- W: wild creado por El Abrazo. Las formas formadas solo por wilds pagan como W (igual que H1).
- S Entrada (scatter).
Los wilds sustituyen en todos los rodillos, incluido el primero.

El Abrazo (base y free spins)
Si en la misma tirada aparecen el Bailarín (rodillos 1-2) y la Bailarina (rodillos 4-5), la fila del Bailarín
se vuelve wild en los 5 rodillos (los scatters de esa fila se mantienen). Evento "abrazo".

La Rosa Roja (solo juego base)
En una tirada ganadora, al azar (12%), multiplica el premio total de la tirada por x2, x3, x5 o x10. Evento "rosaRoja".

Free spins "La Pista"
3 / 4 / 5 entradas dan 10 / 12 / 15 giros. 3 o más entradas durante el bono suman +5 giros.
Compás: multiplicador de todos los premios del bono. Arranca en x1 y suma +1 con cada Abrazo
(se aplica a la tirada del Abrazo). No se reinicia durante el bono. Evento "updateGlobalMult".
Rodillos por sesión: al empezar cada bono se sortea una tira para todas sus tiradas: FR0 (normal) o FR1
("noche caliente", más bailarines y por lo tanto más Abrazos), con peso 10:1. Las reglas visibles no cambian;
esto da variedad entre bonos y permite premios naturales altos. La distribución de ganancia máxima usa FRWCAP.

Modos
- base (1x): juego normal.
- ante (1,5x, "Noche de Gala"): free spins más seguido (objetivo 1 cada 90 vs 1 cada 200).
- bonus (100x, "La Pista"): compra directa de free spins.
- super (400x, "La Última Tanda"): free spins con Compás desde x5 y un Abrazo garantizado en el primer giro.

RTP 96,3% en todos los modos. Ganancia máxima 15.000x en todos los modos.
