<script lang="ts">
	import { Sprite, SpriteSheet, type SpriteProps } from 'pixi-svelte';

	import { getSymbolInfo } from '../game/utils';
	import { SYMBOL_SIZE } from '../game/constants';
	import { onMount } from 'svelte';

	// frames per tick at 60 fps: 16 frames in about 2 seconds
	const WIN_ANIMATION_SPEED = 16 / 120;

	type Props = {
		x?: number;
		y?: number;
		symbolInfo: ReturnType<typeof getSymbolInfo>;
		oncomplete?: () => void;
	};

	const props: Props = $props();
	// a still is done as soon as it shows; the win animation reports when it has played through
	const animated = $derived(props.symbolInfo.type === 'spriteSheet');

	onMount(() => {
		if (!animated) props.oncomplete?.();
	});

	$effect(() => {
		props.symbolInfo;
		if (!animated) props.oncomplete?.();
	});
</script>

{#if animated}
	<!-- win animation: 16 frames over about 2 seconds, played once while the win is shown -->
	<SpriteSheet
		x={props.x}
		y={props.y}
		anchor={0.5}
		key={props.symbolInfo.assetKey}
		width={SYMBOL_SIZE * props.symbolInfo.sizeRatios.width}
		height={SYMBOL_SIZE * props.symbolInfo.sizeRatios.height}
		animationSpeed={WIN_ANIMATION_SPEED}
		loop={false}
		onComplete={() => props.oncomplete?.()}
		play
	/>
{:else}
	<Sprite
		x={props.x}
		y={props.y}
		anchor={0.5}
		key={props.symbolInfo.assetKey}
		width={SYMBOL_SIZE * props.symbolInfo.sizeRatios.width}
		height={SYMBOL_SIZE * props.symbolInfo.sizeRatios.height}
	/>
{/if}
