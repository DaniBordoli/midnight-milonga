<script lang="ts" module>
	// row is the padded board row of the Abrazo (1..4), as in the book event
	export type EmitterEventAbrazoDance = { type: 'abrazoDance'; row: number };
</script>

<script lang="ts">
	import { Tween } from 'svelte/motion';
	import { cubicOut } from 'svelte/easing';

	import { Container, Sprite, SpriteSheet } from 'pixi-svelte';
	import { MainContainer } from 'components-layout';
	import { waitForResolve, waitForTimeout } from 'utils-shared/wait';

	import { getContext } from '../game/context';
	import { SYMBOL_SIZE } from '../game/constants';

	// El Abrazo: the couple dances a turn and a dip over the board while a golden trail crosses the Abrazo row.
	const context = getContext();
	// dance spritesheet frames are 384 x 381 (tools/process_cartoon_bonus.py)
	const COUPLE = { width: SYMBOL_SIZE * 3.2 * (384 / 381), height: SYMBOL_SIZE * 3.2 };
	// 25 frames in about 1.5 seconds at 60 fps
	const DANCE_SPEED = 25 / 90;
	const HOLD_MS = 350;

	const board = $derived(context.stateGameDerived.boardLayout());
	let show = $state(false);
	let rowY = $state(0);
	let danced = () => {};
	const trail = new Tween(0, { duration: 600, easing: cubicOut });
	const alpha = new Tween(0, { duration: 180 });

	context.eventEmitter.subscribeOnMount({
		abrazoDance: async (emitterEvent) => {
			rowY = board.y - board.height / 2 + (emitterEvent.row - 0.5) * SYMBOL_SIZE;
			trail.set(0, { duration: 0 });
			await waitForResolve((resolve) => {
				danced = resolve;
				show = true;
				alpha.set(1);
				trail.set(1);
			});
			await waitForTimeout(HOLD_MS);
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
			<SpriteSheet
				key="fxAbrazoDance"
				anchor={{ x: 0.5, y: 1 }}
				x={board.x}
				y={Math.min(rowY + COUPLE.height * 0.45, board.y + board.height / 2 + SYMBOL_SIZE * 0.2)}
				{...COUPLE}
				animationSpeed={DANCE_SPEED}
				loop={false}
				onComplete={() => danced()}
				play
			/>
		</Container>
	</MainContainer>
{/if}
