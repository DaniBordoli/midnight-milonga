<script lang="ts">
	import { onDestroy } from 'svelte';
	import { Tween } from 'svelte/motion';

	import { Sprite } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import type { Reel } from '../game/stateGame.svelte';
	import { REEL_PADDING, SYMBOL_SIZE, BOARD_DIMENSIONS } from '../game/constants';

	type Props = {
		reel: Reel;
		oncomplete: () => void;
	};

	// Golden spotlight column over the anticipated reel: fades in, pulses and trembles while spinning, fades out
	// on stop (the stopped reels dim meanwhile, see ReelSymbol).
	const SHAKE = SYMBOL_SIZE * 0.025;
	const props: Props = $props();
	const context = getContext();
	const fade = new Tween(0, { duration: 250 });
	let pulse = $state(0);
	let finished = false;
	const timer = setInterval(() => (pulse += 0.12), 16);
	fade.set(1);

	$effect(() => {
		if (props.reel.reelState.motion === 'stopped' && !finished) {
			finished = true;
			fade.set(0).then(() => props.oncomplete());
		}
	});
	onDestroy(() => clearInterval(timer));
</script>

<Sprite
	key="fxAnticipation"
	anchor={0.5}
	blendMode="add"
	alpha={fade.current * (0.75 + 0.25 * Math.sin(pulse))}
	width={SYMBOL_SIZE * (1.15 + 0.05 * Math.sin(pulse))}
	height={SYMBOL_SIZE * (BOARD_DIMENSIONS.y + 0.4)}
	x={context.stateGameDerived.boardLayout().x -
		context.stateGameDerived.boardLayout().width * 0.5 +
		(props.reel.reelIndex + REEL_PADDING) * SYMBOL_SIZE +
		SHAKE * Math.sin(pulse * 4.3) * Math.cos(pulse * 1.7)}
	y={context.stateGameDerived.boardLayout().y}
/>
