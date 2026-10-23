# Midnight Milonga — rediseño cartoon

Motivo: la revisión de Stake (2026-10-22) dio 3/9 puntos por assets de baja calidad, animaciones pobres, barra de apuesta pobre, sonido y estilo inconsistente. El rediseño pasa **todo el juego** a un solo estilo cartoon y suma animación real. Herramienta: Ludo.ai (MCP).

## 1. Guía de estilo

**Estilo elegido (2026-10-22): chibi.** Referencia: `Downloads\slot\7. Cartoon\chibi\referencia_pareja.webp` (pareja chibi, opción A, generada con Ludo). Todo el arte nuevo se genera con `generateWithStyle` y esa referencia. Lo que sigue en esta sección es la guía original y se mantiene en paleta, luz y personajes; las proporciones pasan a chibi (cabeza grande, cuerpo chico, ojos grandes).

| Aspecto | Decisión |
|---|---|
| Tema | Milonga porteña de los años 20, de noche. Se mantiene el tono elegante, pero en clave de dibujo animado. |
| Línea | Contorno oscuro (#2A1418), grosor uniforme y algo más grueso en la silueta exterior. |
| Sombreado | Cel-shading: 2 tonos por color más un brillo. Sin degradados realistas ni texturas fotográficas. |
| Formas | Redondeadas y exageradas. Cabezas y manos algo grandes en los personajes; objetos con proporciones "gorditas". |
| Paleta | Bordó/carmesí (#B3123A, #7A0C26), dorado cálido (#F2B53A, #C98A1E), negro azulado de noche (#1B1630), crema (#F6E7C8). Acentos: verde botella (#1F6B4A) y azul medianoche (#2B3F8C) para los palos. |
| Luz | Cálida, de arañas y faroles. Sombras moradas, nunca negras planas. |
| Personajes | El Bailarín (traje negro, sombrero, clavel rojo) y La Bailarina (vestido rojo con flecos, rosa en el pelo). Son los mismos en símbolos, El Abrazo, intros y portada. |
| Tipografía del juego | Federo se mantiene en la interfaz; los carteles (BIG WIN, LA PISTA, etc.) se dibujan con letras cartoon con volumen y contorno. |

**Prompt base** (se agrega a todos los pedidos de imagen):

> 2D cartoon game art, 1920s Buenos Aires tango hall at night, bold uniform dark outline (#2A1418), cel shading with two tones and one highlight, rounded exaggerated shapes, palette crimson #B3123A, deep burgundy #7A0C26, warm gold #F2B53A, night navy #1B1630, cream #F6E7C8, warm chandelier lighting, purple shadows, clean readable silhouette, no text, no watermark

Para sprites sueltos se agrega: `isolated on transparent background, centered, full object visible`.

**Regla de consistencia:** la primera pieza aprobada (el Bailarín) se usa como referencia de estilo para todas las demás.

## 2. Assets por prioridad

Prioridad según lo que marcaron los revisores: animaciones y assets (3 de 3), barra de apuesta (2 de 3), sonido y estilo (1 de 3).

### P1 — Símbolos (24 sprites hoy, todos cuadrados opacos)
Pasan a tener **fondo transparente** y una **animación de victoria** (spritesheet en loop, ~12 cuadros), en lugar del cambio de textura actual. Requiere cambio de código en `SymbolSprite.svelte` / `constants.ts`.

| Código | Símbolo | Animación de victoria |
|---|---|---|
| BM | El Bailarín (wild, rodillos 1–2) | gira y se acomoda el sombrero |
| BF | La Bailarina (wild, rodillos 4–5) | giro con el vestido y la rosa |
| W | Wild dorado (pareja abrazada) | brillo dorado que recorre la pareja |
| S | Entrada a la milonga (scatter) | la entrada se sacude y brilla |
| H1 | Bandoneón | se abre y se cierra |
| H2 | Rosa roja | se abre y suelta un pétalo |
| H3 | Sombrero | salta y gira |
| H4 | Copa de champagne | burbujas y brindis |
| L1–L4 | Pica, corazón, diamante, trébol | rebote con brillo (misma animación para los 4) |

### P1 — Animaciones de features
- **El Abrazo:** hoy son 4 poses fijas que se intercalan; pasa a ser un spritesheet continuo de la pareja bailando.
- **La Rosa Roja:** rosa voladora animada (girando) y explosión de pétalos en spritesheet.
- **Compás:** el metrónomo se rediseña en cartoon; el péndulo sigue animado por código.

### P2 — Barra de apuesta e interfaz
- Botón de giro, botón chico, botón de compra, botón de menú y placa de info (saldo, premio, apuesta).
- Íconos: autospin, turbo, menú, +, −.
- Estados: reposo, presionado y deshabilitado.

### P2 — Fondos y pantallas
- Fondo del juego, pantalla de carga, fondo de La Pista y fondo de La Última Tanda.
- Marco del tablero: el código asume una apertura transparente de ~74% × 69%.
- Carteles: LA PISTA, LA ÚLTIMA TANDA, LA ROSA ROJA, EL ABRAZO, BIG/SUPER/MEGA/EPIC/MAX WIN y el panel TOTAL WIN.
- Logo del juego en cartoon.
- Las tarjetas de compra de bonus se regeneran desde los fondos nuevos con `tools/make_bonus_card_art.py`.

### P3 — Sonido
- Efectos nuevos generados con Ludo: parada de rodillo, botones, victoria chica, anticipación, entradas, El Abrazo, la rosa y el Compás.
- Música: también generada con Ludo (tema base, giros gratis y loop de premios grandes); reemplazó a la de Pixabay.

### FX que deben seguir siendo brillo sobre negro
Anticipación, explosión de la rosa, estela del Abrazo y destellos: el código los dibuja en modo aditivo.

## 3. Cambios de código previstos
- Símbolos con transparencia y spritesheet de victoria (hoy no hay animación de símbolos).
- Ajustar las proporciones fijas en `WinAnimation`, `FeatureBanner`, `AbrazoDance`, `Compas`, `LoadingScreen`, `FreeSpinIntro`, `FreeSpinOutro`, `ButtonBuyBonus` y `Background` cuando cambien los tamaños de los sprites.
- Scripts de `tools/` para procesar lo que entregue Ludo (recorte, WebP, spritesheets en formato Pixi).
