<script lang="ts">
	import type { Snippet } from 'svelte';

	type Props = {
		title: Snippet;
		description: Snippet;
		price: Snippet;
		button: Snippet;
		image?: string;
	};

	const props: Props = $props();
</script>

<div class="bonus-card-wrap">
	{#if props.image}
		<img class="image" src={props.image} alt="" draggable="false" />
	{/if}
	<div class="info">
		{@render props.title()}
		{@render props.description()}
		{@render props.price()}
	</div>
	{@render props.button()}
</div>

<style lang="scss">
	.bonus-card-wrap {
		padding: 0.5rem;
		flex-direction: column;
		display: flex;
		justify-content: space-between;

		border-radius: 6px;
		background: linear-gradient(180deg, rgba(46, 8, 16, 0.9), rgba(18, 12, 12, 0.9));
		border: var(--mm-border);
		text-align: left;
		min-width: 155px;
		max-width: 180px;
		gap: 0.5rem;
	}

	.image {
		display: block;
		width: 100%;
		aspect-ratio: 9 / 5;
		object-fit: cover;
		border-radius: 4px;
		border: var(--mm-border);
	}

	.info {
		display: flex;
		flex-direction: column;
		gap: 0.5em;
	}
</style>
