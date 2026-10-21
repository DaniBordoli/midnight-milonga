<script lang="ts" module>
	export type EmitterEventFeatureBanner = {
		type: 'featureBanner';
		// plate art for the main features; any other title is drawn as text on a dark panel
		variant?: 'abrazo' | 'rosa';
		title: string;
		subtitle?: string;
	};
</script>

<script lang="ts">
	import { Tween } from 'svelte/motion';
	import { backOut } from 'svelte/easing';

	import { Container, Rectangle, Sprite, Text } from 'pixi-svelte';
	import { FadeContainer } from 'components-pixi';
	import { MainContainer } from 'components-layout';
	import { waitForTimeout } from 'utils-shared/wait';

	import { getContext } from '../game/context';
	import { SYMBOL_SIZE } from '../game/constants';

	const context = getContext();
	const PLATES = {
		abrazo: { key: 'fxBannerAbrazo', ratio: 212 / 978 },
		rosa: { key: 'fxBannerRosa', ratio: 250 / 994 },
	} as const;
	const PLATE_WIDTH = SYMBOL_SIZE * 4.6;
	const PANEL = { width: SYMBOL_SIZE * 4.6, height: SYMBOL_SIZE * 1.3 };

	const pop = new Tween(0.6, { duration: 380, easing: backOut });
	let show = $state(false);
	let variant = $state<'abrazo' | 'rosa' | undefined>();
	let title = $state('');
	let subtitle = $state('');

	context.eventEmitter.subscribeOnMount({
		featureBanner: async (emitterEvent) => {
			variant = emitterEvent.variant;
			title = emitterEvent.title;
			subtitle = emitterEvent.subtitle ?? '';
			show = true;
			pop.set(0.6, { duration: 0 });
			pop.set(1);
			await waitForTimeout(1100);
			show = false;
			await waitForTimeout(250);
		},
	});
</script>

<FadeContainer {show}>
	<MainContainer>
		<Container
			x={context.stateGameDerived.boardLayout().x}
			y={context.stateGameDerived.boardLayout().y}
			scale={pop.current}
		>
			{#if variant}
				<Sprite
					key={PLATES[variant].key}
					anchor={0.5}
					width={PLATE_WIDTH}
					height={PLATE_WIDTH * PLATES[variant].ratio}
				/>
			{:else}
				<Rectangle
					x={-PANEL.width / 2}
					y={-PANEL.height / 2}
					width={PANEL.width}
					height={PANEL.height}
					backgroundColor={0x120c0c}
					backgroundAlpha={0.9}
					borderColor={0xdeb862}
					borderWidth={4}
					borderRadius={18}
				/>
				<Text
					anchor={0.5}
					text={title}
					style={{ fontFamily: 'Georgia, serif', fontSize: SYMBOL_SIZE * 0.5, fontWeight: '700', fill: 0xf2d692, letterSpacing: 4 }}
				/>
			{/if}
			{#if subtitle}
				<Text
					anchor={0.5}
					y={SYMBOL_SIZE * 0.85}
					text={subtitle}
					style={{
						fontFamily: 'Georgia, serif',
						fontSize: SYMBOL_SIZE * 0.3,
						fontWeight: '700',
						fill: 0xece5d8,
						dropShadow: { color: 0x000000, blur: 6, distance: 0, alpha: 0.9 },
					}}
				/>
			{/if}
		</Container>
	</MainContainer>
</FadeContainer>
