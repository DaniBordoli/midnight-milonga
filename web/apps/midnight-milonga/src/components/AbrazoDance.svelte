<script lang="ts" module>
	// row is the padded board row of the Abrazo (1..4), as in the book event
	export type EmitterEventAbrazoDance = { type: 'abrazoDance'; row: number };
</script>

<script lang="ts">
	import { Tween } from 'svelte/motion';
	import { cubicOut } from 'svelte/easing';

	import { Container, Sprite } from 'pixi-svelte';
	import { MainContainer } from 'components-layout';
	import { waitForTimeout } from 'utils-shared/wait';

	import { getContext } from '../game/context';
	import { SYMBOL_SIZE } from '../game/constants';

	// El Abrazo: the couple's four poses play over the board while a golden trail crosses the Abrazo row.
	const context = getContext();
	const FRAMES = [
		{ key: 'fxAbrazo1', ratio: 768 / 671 },
		{ key: 'fxAbrazo2', ratio: 768 / 476 },
		{ key: 'fxAbrazo3', ratio: 768 / 482 },
		{ key: 'fxAbrazo4', ratio: 768 / 569 },
	];
	const COUPLE_HEIGHT = SYMBOL_SIZE * 3.2;
	const FRAME_MS = 300;

	const board = $derived(context.stateGameDerived.boardLayout());
	let show = $state(false);
	let frame = $state(0);
	let rowY = $state(0);
	const trail = new Tween(0, { duration: FRAME_MS * 2, easing: cubicOut });
	const alpha = new Tween(0, { duration: 180 });

	context.eventEmitter.subscribeOnMount({
		abrazoDance: async (emitterEvent) => {
			rowY = board.y - board.height / 2 + (emitterEvent.row - 0.5) * SYMBOL_SIZE;
			frame = 0;
			show = true;
			trail.set(0, { duration: 0 });
			alpha.set(1);
			trail.set(1);
			for (let i = 1; i < FRAMES.length; i++) {
				await waitForTimeout(FRAME_MS);
				frame = i;
			}
			await waitForTimeout(FRAME_MS * 1.5);
			await alpha.set(0);
			show = false;
		},
	});
</script>

{#if show}
	<MainContainer>
		<Container alpha={alpha.current}>
			<Sprite
				key="fxAbrazoTrail"
				anchor={{ x: 0, y: 0.5 }}
				blendMode="add"
				x={board.x - board.width / 2}
				y={rowY}
				width={board.width * trail.current}
				height={SYMBOL_SIZE * 0.9}
			/>
			<Sprite
				key={FRAMES[frame].key}
				anchor={{ x: 0.5, y: 1 }}
				x={board.x}
				y={Math.min(rowY + COUPLE_HEIGHT * 0.45, board.y + board.height / 2 + SYMBOL_SIZE * 0.2)}
				width={COUPLE_HEIGHT / FRAMES[frame].ratio}
				height={COUPLE_HEIGHT}
			/>
		</Container>
	</MainContainer>
{/if}
