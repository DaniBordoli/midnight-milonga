import _ from 'lodash';

import type { RawSymbol, SymbolState } from './types';
import { stateLayoutDerived } from './stateLayout';

export const SYMBOL_SIZE = 120;

export const REEL_PADDING = 0.53;

// initial board: 5 reels x 4 rows, padded with one symbol on top and bottom
const reel = (...names: RawSymbol['name'][]): RawSymbol[] => names.map((name) => ({ name }));
export const INITIAL_BOARD: RawSymbol[][] = [
	reel('L1', 'H1', 'L2', 'H3', 'L4', 'L2'),
	reel('L3', 'H2', 'L1', 'L4', 'H4', 'L1'),
	reel('H4', 'L2', 'H1', 'L3', 'L1', 'H2'),
	reel('L2', 'L4', 'H3', 'H2', 'L3', 'L4'),
	reel('H1', 'L3', 'L4', 'L1', 'H2', 'L3'),
];

export const BOARD_DIMENSIONS = { x: INITIAL_BOARD.length, y: INITIAL_BOARD[0].length - 2 };

export const BOARD_SIZES = {
	width: SYMBOL_SIZE * BOARD_DIMENSIONS.x,
	height: SYMBOL_SIZE * BOARD_DIMENSIONS.y,
};

export const BACKGROUND_RATIO = 2039 / 1000;
export const PORTRAIT_BACKGROUND_RATIO = 1242 / 2208;
const PORTRAIT_RATIO = 800 / 1422;
const LANDSCAPE_RATIO = 1600 / 900;
const DESKTOP_RATIO = 1422 / 800;

const DESKTOP_HEIGHT = 800;
const LANDSCAPE_HEIGHT = 900;
const PORTRAIT_HEIGHT = 1422;
export const DESKTOP_MAIN_SIZES = { width: DESKTOP_HEIGHT * DESKTOP_RATIO, height: DESKTOP_HEIGHT };
export const LANDSCAPE_MAIN_SIZES = {
	width: LANDSCAPE_HEIGHT * LANDSCAPE_RATIO,
	height: LANDSCAPE_HEIGHT,
};
export const PORTRAIT_MAIN_SIZES = {
	width: PORTRAIT_HEIGHT * PORTRAIT_RATIO,
	height: PORTRAIT_HEIGHT,
};

export const HIGH_SYMBOLS = ['H1', 'H2', 'H3', 'H4'];

export const INITIAL_SYMBOL_STATE: SymbolState = 'static';

const SPIN_OPTIONS_SHARED = {
	reelBounceBackSpeed: 0.15,
	reelSpinSpeedBeforeBounce: 4,
	reelPaddingMultiplierNormal: 1.2,
	reelPaddingMultiplierAnticipated: 10,
	reelSpinDelay: 145,
};

export const SPIN_OPTIONS_DEFAULT = {
	...SPIN_OPTIONS_SHARED,
	reelPreSpinSpeed: 2,
	reelSpinSpeed: 3,
	reelBounceSizeMulti: 0.3,
};

export const SPIN_OPTIONS_FAST = {
	...SPIN_OPTIONS_SHARED,
	reelPreSpinSpeed: 5,
	reelSpinSpeed: 5,
	reelBounceSizeMulti: 0.05,
};

export const MOTION_BLUR_VELOCITY = 31;

// win amounts (replaces the sample "gold" bitmap font)
// Federo is bundled (src/fonts.css); Georgia only shows if it ever failed to load
export const GAME_FONT = 'Federo, Georgia, serif';

export const WIN_TEXT_STYLE = {
	fontFamily: GAME_FONT,
	fontSize: SYMBOL_SIZE * 0.8,
	fontWeight: '400',
	fill: 0xf2d692,
	stroke: { color: 0x4a1f10, width: 6 },
	dropShadow: { color: 0x000000, blur: 8, distance: 0, alpha: 0.9 },
} as const;

export const zIndexes = {
	background: {
		backdrop: -3,
		normal: -2,
		feature: -1,
	},
};

// win spritesheet cells are this much larger than the still, so the motion has room (WIN_PAD in
// tools/process_cartoon_symbols.py); the first frame lines up with the still
const WIN_SCALE = 1.25;

// cartoon symbols: a still for every state, and a looping win spritesheet while the symbol is part of a win
const milongaSymbol = (key: string, size = 0.94) => {
	const normal = { type: 'sprite', assetKey: key, sizeRatios: { width: size, height: size } } as const;
	const win = {
		type: 'spriteSheet',
		assetKey: `${key}Win`,
		sizeRatios: { width: size * WIN_SCALE, height: size * WIN_SCALE },
	} as const;
	// code-driven motion on the still (SymbolSprite): a squash-and-bounce on landing, a gentle breath at rest
	const land = { ...normal, motion: 'land' } as const;
	const idle = { ...normal, motion: 'idle' } as const;
	// 'explosion' is a state the SDK board knows but this game never sets; it shows the plain symbol
	return { explosion: normal, static: idle, spin: normal, land, win, postWinStatic: idle };
};

export const SYMBOL_INFO_MAP = {
	W: milongaSymbol('mmW'),
	BM: milongaSymbol('mmBM'),
	BF: milongaSymbol('mmBF'),
	S: milongaSymbol('mmS'),
	H1: milongaSymbol('mmH1'),
	H2: milongaSymbol('mmH2'),
	H3: milongaSymbol('mmH3'),
	H4: milongaSymbol('mmH4'),
	L1: milongaSymbol('mmL1'),
	L2: milongaSymbol('mmL2'),
	L3: milongaSymbol('mmL3'),
	L4: milongaSymbol('mmL4'),
} as const;

export const SCATTER_LAND_SOUND_MAP = {
	1: 'sfx_scatter_stop_1',
	2: 'sfx_scatter_stop_2',
	3: 'sfx_scatter_stop_3',
	4: 'sfx_scatter_stop_4',
	5: 'sfx_scatter_stop_5',
} as const;

// The header (clock + game name, provider name) uses fixed-size text; on narrow canvases such as Stake's
// small popout it shrinks so the two never overlap.
export const headerScale = () => Math.min(1, Math.max(0.5, stateLayoutDerived.canvasSizes().width / 1100));
