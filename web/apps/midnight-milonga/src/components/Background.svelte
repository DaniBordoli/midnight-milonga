<script lang="ts">
	import { Rectangle, Sprite } from 'pixi-svelte';

	import { getContext } from '../game/context';

	// cartoon milonga hall (2048 x 1143, tools/process_cartoon_background.py), scaled to cover the canvas
	const BACKGROUND_SIZE = { width: 2048, height: 1143 };

	const context = getContext();
	const canvas = $derived(context.stateLayoutDerived.canvasSizes());
	const coverScale = $derived(
		Math.max(canvas.width / BACKGROUND_SIZE.width, canvas.height / BACKGROUND_SIZE.height),
	);
</script>

<Rectangle {...canvas} backgroundColor={0x0c0a0a} zIndex={-3} />

<Sprite
	key="mmBackground"
	anchor={0.5}
	x={canvas.width / 2}
	y={canvas.height / 2}
	width={BACKGROUND_SIZE.width * coverScale}
	height={BACKGROUND_SIZE.height * coverScale}
	zIndex={-2}
/>
