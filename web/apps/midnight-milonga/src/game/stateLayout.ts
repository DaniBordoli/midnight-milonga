import { createLayout } from 'utils-layout';

export const { stateLayout, stateLayoutDerived } = createLayout({
	backgroundRatio: {
		normal: 2039 / 1000,
		portrait: 1242 / 2208,
	},
	// sized so the board's Art Deco frame (1.4 x 1.5 the board) fits above the bottom UI bar
	mainSizesMap: {
		desktop: { width: 1778, height: 1000 },
		tablet: { width: 1000, height: 1000 },
		landscape: { width: 1778, height: 1000 },
		portrait: { width: 900, height: 1600 },
	},
});
