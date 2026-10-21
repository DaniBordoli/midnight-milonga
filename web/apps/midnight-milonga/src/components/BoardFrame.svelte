<script lang="ts" module>
	export type EmitterEventBoardFrame =
		| { type: 'boardFrameGlowShow' }
		| { type: 'boardFrameGlowHide' };
</script>

<script lang="ts">
	import { onDestroy } from 'svelte';
	import { Tween } from 'svelte/motion';

	import { Rectangle, Sprite } from 'pixi-svelte';

	import { getContext } from '../game/context';

	// Art-deco frame (transparent center) over a dark backing; during free spins a gold border pulses
	// around the board (replaces the sample "reelhouse" spine glow).
	const context = getContext();
	const FRAME_SCALE = 1.14;
	const board = $derived(context.stateGameDerived.boardLayout());

	const glow = new Tween(0, { duration: 400 });
	let pulse = $state(0);
	const timer = setInterval(() => (pulse += 0.05), 16);
	onDestroy(() => clearInterval(timer));

	context.eventEmitter.subscribeOnMount({
		boardFrameGlowShow: () => glow.set(1),
		boardFrameGlowHide: () => glow.set(0),
	});
</script>

<Rectangle
	x={board.x - board.width / 2}
	y={board.y - board.height / 2}
	width={board.width}
	height={board.height}
	backgroundColor={0x0e0b0b}
	backgroundAlpha={0.92}
/>

{#if glow.current > 0}
	<Rectangle
		x={board.x - (board.width * FRAME_SCALE) / 2}
		y={board.y - (board.height * FRAME_SCALE) / 2}
		width={board.width * FRAME_SCALE}
		height={board.height * FRAME_SCALE}
		backgroundAlpha={0}
		borderColor={0xf2d692}
		borderWidth={10}
		borderRadius={24}
		alpha={glow.current * (0.45 + 0.35 * Math.sin(pulse))}
		blendMode="add"
	/>
{/if}

<Sprite
	key="fxBoardFrame"
	anchor={0.5}
	x={board.x}
	y={board.y}
	width={board.width * FRAME_SCALE}
	height={board.height * FRAME_SCALE}
/>
