<script lang="ts" module>
	export type EmitterEventCompas =
		| { type: 'compasShow' }
		| { type: 'compasHide' }
		| { type: 'compasUpdate'; value: number };
</script>

<script lang="ts">
	import { onDestroy } from 'svelte';
	import { Tween } from 'svelte/motion';
	import { backOut } from 'svelte/easing';

	import { Container, Sprite, Text } from 'pixi-svelte';
	import { FadeContainer } from 'components-pixi';

	import { getContext } from '../game/context';
	import { SYMBOL_SIZE, GAME_FONT } from '../game/constants';

	// Compás: free-spin multiplier shown as a metronome left of the board. The pendulum swings faster as
	// the Compás grows and the number pops when it increases.
	const context = getContext();
	const BODY = { width: SYMBOL_SIZE * 1.3, height: SYMBOL_SIZE * 1.3 * (699 / 417) }; // cartoon art, tools/process_cartoon_bonus.py
	const PENDULUM = { width: BODY.height * 0.72 * (101 / 717), height: BODY.height * 0.72 };
	const position = $derived({
		x: context.stateGameDerived.boardLayout().x - context.stateGameDerived.boardLayout().width / 2 - SYMBOL_SIZE * 1.85, // clear of the frame's side ornaments
		// below the free-spin counter, which sits at the board's top-left
		y: context.stateGameDerived.boardLayout().y + SYMBOL_SIZE * 0.95,
	});

	let show = $state(false);
	let value = $state(1);
	let phase = $state(0);
	const pop = new Tween(1, { duration: 400, easing: backOut });
	const timer = setInterval(() => (phase += 0.03 + Math.min(value, 12) * 0.006), 16);
	onDestroy(() => clearInterval(timer));

	context.eventEmitter.subscribeOnMount({
		compasShow: () => (show = true),
		compasHide: () => (show = false),
		compasUpdate: async (emitterEvent) => {
			const grew = emitterEvent.value > value;
			value = emitterEvent.value;
			if (grew) {
				context.eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_multiplier_update' });
				pop.set(1.45, { duration: 0 });
				await pop.set(1);
			}
		},
	});
</script>

<FadeContainer {show}>
	<Container {...position}>
		<!-- pendulum hinges near the base of the body and swings behind the front plaque -->
		<Sprite
			key="fxMetronomePendulum"
			anchor={{ x: 0.5, y: 1 }}
			y={BODY.height * 0.12}
			rotation={Math.sin(phase) * 0.38}
			{...PENDULUM}
		/>
		<Sprite key="fxMetronomeBody" anchor={0.5} {...BODY} />
		<Text
			anchor={0.5}
			y={BODY.height * 0.25}
			scale={pop.current}
			text={`x${value}`}
			style={{
				fontFamily: GAME_FONT,
				fontSize: SYMBOL_SIZE * 0.36,
				fontWeight: '400',
				fill: 0x2a1408,
				stroke: { color: 0xf2d692, width: 2 },
			}}
		/>
	</Container>
</FadeContainer>
