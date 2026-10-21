<script lang="ts">
	import { onMount } from 'svelte';
	import { Tween } from 'svelte/motion';
	import { cubicInOut } from 'svelte/easing';

	import { Rectangle } from 'pixi-svelte';
	import { waitForTimeout } from 'utils-shared/wait';

	import { getContext } from '../game/context';

	type Props = {
		// called when the screen is fully black: switch what is underneath here
		oncomplete: () => void;
		// called after fading back in: the parent can unmount the transition now
		onfinish?: () => void;
	};

	// Fade to black and back (replaces the sample spine transition).
	const props: Props = $props();
	const context = getContext();
	const alpha = new Tween(0, { duration: 350, easing: cubicInOut });

	onMount(async () => {
		await alpha.set(1);
		await waitForTimeout(150);
		props.oncomplete();
		await alpha.set(0);
		props.onfinish?.();
	});
</script>

{#if alpha.current > 0.001}
	<Rectangle {...context.stateLayoutDerived.canvasSizes()} backgroundColor={0x000000} alpha={alpha.current} zIndex={100} />
{/if}
