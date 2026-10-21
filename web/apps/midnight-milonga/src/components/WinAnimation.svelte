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

	// Big win: title plate popping in over pulsing gold sparkles, amount underneath.
	// Only the "BIG WIN" plate exists for now, so higher tiers reuse it a bit larger.
	const props: Props = $props();
	const tier = $derived(['big', 'super', 'mega', 'epic', 'max'].findIndex((t) => props.animationMap.intro.startsWith(t)));
	const PLATE = { width: SYMBOL_SIZE * 4.6, height: SYMBOL_SIZE * 4.6 * (307 / 910) };

	const pop = new Tween(0.3, { duration: 550, easing: backOut });
	let pulse = $state(0);
	const timer = setInterval(() => (pulse += 0.08), 16);
	onMount(() => pop.set(1 + Math.max(tier, 0) * 0.06));
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
	<Sprite key="fxBigWin" anchor={0.5} {...PLATE} />
</Container>
<Container y={SYMBOL_SIZE * 0.85}>
	{@render props.children()}
</Container>
