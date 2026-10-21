<script lang="ts" module>
	export type EmitterEventFreeSpinIntro =
		| { type: 'freeSpinIntroShow' }
		| { type: 'freeSpinIntroHide' }
		| { type: 'freeSpinIntroUpdate'; totalFreeSpins: number };
</script>

<script lang="ts">
	import { Tween } from 'svelte/motion';
	import { backOut } from 'svelte/easing';

	import { Container, Rectangle, Sprite, Text } from 'pixi-svelte';
	import { MainContainer } from 'components-layout';
	import { FadeContainer } from 'components-pixi';
	import { stateBet } from 'state-shared';
	import { waitForResolve } from 'utils-shared/wait';

	import { getContext } from '../game/context';
	import { SYMBOL_SIZE } from '../game/constants';
	import PressToContinue from './PressToContinue.svelte';

	// La Pista / La Última Tanda intro, built from layered art (background, title plate, spins plate, couple).
	const context = getContext();
	const BACKGROUND = { width: 1024, height: 572 };
	const isSuper = $derived(String(stateBet.activeBetModeKey).toUpperCase() === 'SUPER');

	const canvas = $derived(context.stateLayoutDerived.canvasSizes());
	const coverScale = $derived(Math.max(canvas.width / BACKGROUND.width, canvas.height / BACKGROUND.height));
	const center = $derived({
		x: context.stateLayoutDerived.mainLayout().width * 0.5,
		y: context.stateLayoutDerived.mainLayout().height * 0.45,
	});

	const pop = new Tween(0.6, { duration: 450, easing: backOut });

	let show = $state(false);
	let spins = $state(0);
	let oncomplete = $state(() => {});

	context.eventEmitter.subscribeOnMount({
		freeSpinIntroShow: () => {
			show = true;
			pop.set(0.6, { duration: 0 });
			pop.set(1);
		},
		freeSpinIntroHide: () => (show = false),
		freeSpinIntroUpdate: async (emitterEvent) => {
			spins = emitterEvent.totalFreeSpins;
			await waitForResolve((resolve) => (oncomplete = resolve));
		},
	});
</script>

<FadeContainer {show}>
	<Sprite
		key={isSuper ? 'fxTandaBg' : 'fxPistaBg'}
		anchor={0.5}
		x={canvas.width / 2}
		y={canvas.height / 2}
		width={BACKGROUND.width * coverScale}
		height={BACKGROUND.height * coverScale}
	/>
	<Rectangle {...canvas} backgroundColor={0x000000} backgroundAlpha={0.25} />

	<MainContainer>
		{#if isSuper}
			<Sprite
				key="fxTandaCouple"
				anchor={{ x: 0.5, y: 1 }}
				x={center.x - SYMBOL_SIZE * 3.4}
				y={center.y + SYMBOL_SIZE * 2.6}
				width={SYMBOL_SIZE * 2.6}
				height={SYMBOL_SIZE * 2.6 * (836 / 549)}
			/>
		{/if}
		<Container {...center} scale={pop.current}>
			<Sprite
				key={isSuper ? 'fxTandaTitle' : 'fxPistaTitle'}
				anchor={0.5}
				y={-SYMBOL_SIZE * 1.75}
				width={SYMBOL_SIZE * 5}
				height={SYMBOL_SIZE * 5 * (isSuper ? 201 / 1022 : 245 / 1024)}
			/>
			<Sprite key="fxSpinsPlate" anchor={0.5} y={SYMBOL_SIZE * 0.25} width={SYMBOL_SIZE * 2.4} height={SYMBOL_SIZE * 2.4 * (768 / 726)} />
			<Text
				anchor={0.5}
				y={SYMBOL_SIZE * -0.05}
				text={String(spins)}
				style={{ fontFamily: 'Georgia, serif', fontSize: SYMBOL_SIZE * 0.85, fontWeight: '700', fill: 0xf2d692 }}
			/>
			<Text
				anchor={0.5}
				y={SYMBOL_SIZE * 0.62}
				text="FREE SPINS"
				style={{ fontFamily: 'Georgia, serif', fontSize: SYMBOL_SIZE * 0.17, fontWeight: '700', fill: 0xece5d8, letterSpacing: 1 }}
			/>
			{#if isSuper}
				<Text
					anchor={0.5}
					y={SYMBOL_SIZE * 1.75}
					text="COMPÁS STARTS AT x5 · ABRAZO ON THE FIRST SPIN"
					style={{ fontFamily: 'Georgia, serif', fontSize: SYMBOL_SIZE * 0.2, fontWeight: '700', fill: 0xf2d692, letterSpacing: 2 }}
				/>
			{/if}
		</Container>
	</MainContainer>

	<PressToContinue onpress={() => oncomplete()} />
</FadeContainer>
