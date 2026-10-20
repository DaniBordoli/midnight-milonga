<script lang="ts" module>
	export type EmitterEventCompas =
		| { type: 'compasShow' }
		| { type: 'compasHide' }
		| { type: 'compasUpdate'; value: number };
</script>

<script lang="ts">
	import { Container, Rectangle, Text } from 'pixi-svelte';
	import { FadeContainer } from 'components-pixi';
	import { waitForTimeout } from 'utils-shared/wait';

	import { getContext } from '../game/context';
	import { SYMBOL_SIZE } from '../game/constants';

	// Compás: free-spin multiplier meter, left of the board (placeholder until the metronome art).
	const context = getContext();
	const PANEL = { width: SYMBOL_SIZE * 1.3, height: SYMBOL_SIZE * 1.9 };
	const position = $derived({
		x: context.stateGameDerived.boardLayout().x - context.stateGameDerived.boardLayout().width / 2 - PANEL.width - SYMBOL_SIZE * 0.35,
		// below the free-spin counter, which sits at the top-left corner of the board
		y: context.stateGameDerived.boardLayout().y - PANEL.height / 2 + SYMBOL_SIZE * 0.7,
	});

	let show = $state(false);
	let value = $state(1);
	let pulse = $state(1);

	context.eventEmitter.subscribeOnMount({
		compasShow: () => (show = true),
		compasHide: () => (show = false),
		compasUpdate: async (emitterEvent) => {
			const grew = emitterEvent.value > value;
			value = emitterEvent.value;
			if (grew) {
				context.eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_multiplier_update' });
				pulse = 1.25;
				await waitForTimeout(350);
				pulse = 1;
			}
		},
	});
</script>

<FadeContainer {show}>
	<Container {...position}>
		<Rectangle
			width={PANEL.width}
			height={PANEL.height}
			backgroundColor={0x120c0c}
			backgroundAlpha={0.9}
			borderColor={0xdeb862}
			borderWidth={4}
			borderRadius={16}
		/>
		<Text
			anchor={0.5}
			x={PANEL.width / 2}
			y={SYMBOL_SIZE * 0.35}
			text="COMPÁS"
			style={{ fontFamily: 'Georgia, serif', fontSize: SYMBOL_SIZE * 0.22, fontWeight: '700', fill: 0xdeb862, letterSpacing: 3 }}
		/>
		<Text
			anchor={0.5}
			x={PANEL.width / 2}
			y={PANEL.height * 0.6}
			scale={pulse}
			text={`x${value}`}
			style={{ fontFamily: 'Georgia, serif', fontSize: SYMBOL_SIZE * 0.62, fontWeight: '700', fill: 0xf2d692 }}
		/>
	</Container>
</FadeContainer>
