<script lang="ts">
	import type { Snippet } from 'svelte';
	import { onDestroy, onMount } from 'svelte';
	import { Tween } from 'svelte/motion';
	import { backOut } from 'svelte/easing';

	import { Container, Sprite } from 'pixi-svelte';

	import { SYMBOL_SIZE } from '../game/constants';

	type Props = {
		// kept from the sample big-win spine: the intro name tells the tier (big, super, mega, epic, max)
		animationMap: { intro: string; idle: string; outro: string };
		children: Snippet;
	};

	// Big win: the tier's title plate popping in over pulsing gold sparkles, amount underneath.
	const props: Props = $props();
	// key and width/height ratio of each tier's plate image
	const PLATES = [
		{ tier: 'big', key: 'fxBigWin', ratio: 307 / 910 },
		{ tier: 'super', key: 'fxSuperWin', ratio: 282 / 975 },
		{ tier: 'mega', key: 'fxMegaWin', ratio: 302 / 975 },
		{ tier: 'epic', key: 'fxEpicWin', ratio: 301 / 975 },
		{ tier: 'max', key: 'fxMaxWin', ratio: 335 / 1003 },
	];
	const plate = $derived(PLATES.find((p) => props.animationMap.intro.startsWith(p.tier)) ?? PLATES[0]);
	const PLATE_WIDTH = SYMBOL_SIZE * 4.6;

	const pop = new Tween(0.3, { duration: 550, easing: backOut });
	let pulse = $state(0);
	const timer = setInterval(() => (pulse += 0.08), 16);
	onMount(() => pop.set(1));
	onDestroy(() => clearInterval(timer));
</script>

<Container scale={pop.current} y={-SYMBOL_SIZE * 0.55}>
	<Sprite
		key="fxSparkles"
		anchor={0.5}
		width={SYMBOL_SIZE * 5.2}
		height={SYMBOL_SIZE * 5.2}
		alpha={0.55 + 0.35 * Math.sin(pulse)}
		rotation={pulse * 0.05}
		blendMode="add"
	/>
	<Sprite key={plate.key} anchor={0.5} width={PLATE_WIDTH} height={PLATE_WIDTH * plate.ratio} />
</Container>
<Container y={SYMBOL_SIZE * 0.85}>
	{@render props.children()}
</Container>
