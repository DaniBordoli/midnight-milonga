<script lang="ts">
	import type { Snippet } from 'svelte';

	type Props = {
		children: Snippet;
	};

	const props: Props = $props();
</script>

<div class="ui-modal-title-wrap">
	{@render props.children()}
</div>

<style lang="scss">
	/* gold Federo title between two short gold rules */
	.ui-modal-title-wrap {
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 0.75rem;
		text-align: center;
		font-family: var(--mm-font-display);
		font-size: 1.35rem;
		letter-spacing: 0.12em;
		color: var(--mm-gold);

		&::before,
		&::after {
			content: '';
			width: 2.5rem;
			height: 1px;
			background: linear-gradient(90deg, transparent, var(--mm-gold));
		}
		&::after {
			transform: scaleX(-1);
		}
	}
</style>
