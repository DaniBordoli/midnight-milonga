<script lang="ts">
	import type { Snippet } from 'svelte';

	type Props = {
		children: Snippet;
	};

	const props: Props = $props();
</script>

<div class="base-button-content">
	{@render props.children()}
</div>

<style lang="scss">
	.base-button-content {
		position: absolute;
		color: var(--mm-gold);
		font-family: var(--mm-font-display);
		letter-spacing: 0.05em;
		width: 100%;
		height: 100%;
		display: flex;
		justify-content: center;
		align-items: center;
	}
</style>
