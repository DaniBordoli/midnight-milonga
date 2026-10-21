<script lang="ts">
	import { stateBet, stateUrlDerived } from 'state-shared';
	import { getContext } from '../game/context';
	import { onMount } from 'svelte';

	const context = getContext();

	onMount(() => {
		if (stateBet.betToResume?.active && stateBet.betToResume.mode) {
			stateBet.activeBetModeKey = stateBet.betToResume.mode;
		}
		// a replay waits for the player's PLAY press (ReplayControls)
		if (!stateUrlDerived.replay()) context.eventEmitter.broadcast({ type: 'resumeBet' });
	});
</script>
