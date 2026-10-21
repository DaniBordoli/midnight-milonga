<script lang="ts" module>
	export type EmitterEventRosaThrow = { type: 'rosaThrow'; multiplier: number };
</script>

<script lang="ts">
	import { Tween } from 'svelte/motion';
	import { cubicIn, cubicOut } from 'svelte/easing';

	import { Container, Sprite, Text } from 'pixi-svelte';
	import { MainContainer } from 'components-layout';
	import { waitForTimeout } from 'utils-shared/wait';

	import { getContext } from '../game/context';
	import { SYMBOL_SIZE, WIN_TEXT_STYLE } from '../game/constants';

	// La Rosa Roja: a rose is thrown from the balcony (upper left) onto the board and bursts into petals,
	// revealing the multiplier.
	const context = getContext();
	const board = $derived(context.stateGameDerived.boardLayout());

	let show = $state(false);
	let multiplier = $state(2);
	const flight = new Tween(0, { duration: 600, easing: cubicIn });
	const burst = new Tween(0, { duration: 900, easing: cubicOut });

	const start = $derived({ x: board.x - board.width * 0.9, y: board.y - board.height * 0.9 });
	const rose = $derived({
		x: start.x + (board.x - start.x) * flight.current,
		y: start.y + (board.y - start.y) * flight.current,
	});

	context.eventEmitter.subscribeOnMount({
		rosaThrow: async (emitterEvent) => {
			multiplier = emitterEvent.multiplier;
			flight.set(0, { duration: 0 });
			burst.set(0, { duration: 0 });
			show = true;
			await flight.set(1);
			context.eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_multiplier_landing' });
			await burst.set(1);
			// hold the multiplier so the player can read it
			await waitForTimeout(700);
			show = false;
		},
	});
</script>

{#if show}
	<MainContainer>
		{#if burst.current === 0}
			<Sprite
				key="fxRosaFlying"
				anchor={0.5}
				{...rose}
				rotation={-0.6 + flight.current * 3.4}
				width={SYMBOL_SIZE * 1.4}
				height={SYMBOL_SIZE * 1.4}
			/>
		{:else}
			<Container x={board.x} y={board.y}>
				<Sprite
					key="fxRosaBurst"
					anchor={0.5}
					blendMode="add"
					alpha={1 - burst.current}
					width={SYMBOL_SIZE * (1 + burst.current * 4)}
					height={SYMBOL_SIZE * (1 + burst.current * 4)}
				/>
				<Text
					anchor={0.5}
					scale={0.6 + burst.current * 0.6}
					alpha={Math.min(1, burst.current * 3)}
					text={`x${multiplier}`}
					style={{ ...WIN_TEXT_STYLE, fontSize: SYMBOL_SIZE * 1.1 }}
				/>
			</Container>
		{/if}
	</MainContainer>
{/if}
