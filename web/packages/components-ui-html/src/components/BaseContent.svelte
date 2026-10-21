<script lang="ts">
	import type { Snippet } from 'svelte';

	type Props = {
		maxWidth: '100%' | '500px';
		children: Snippet;
	};

	const props: Props = $props();
</script>

<div class="ui-popup-standard-content-wrap" style="--maxWidth: {props.maxWidth}; --zIndex: {100}">
	{@render props.children()}
</div>

<style lang="scss">
	.ui-popup-standard-content-wrap {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		z-index: var(--zIndex);
		max-width: var(--maxWidth);
		gap: 1rem;

		/* Art Deco panel: black lacquer, crimson glow, double gold border */
		padding: 1.5rem 2rem;
		border-radius: 4px;
		background:
			radial-gradient(ellipse at top, rgba(107, 20, 34, 0.35), transparent 60%),
			var(--mm-panel);
		border: var(--mm-border-selected);
		box-shadow:
			inset 0 0 0 4px var(--mm-panel),
			inset 0 0 0 5px var(--mm-gold-deep),
			0 0 24px rgba(242, 214, 146, 0.15);
	}
</style>
