<script lang="ts">
	import type { Snippet } from 'svelte';
	import { SvelteDate } from 'svelte/reactivity';

	import { Container, Text, REM } from 'pixi-svelte';
	import { WHITE } from 'constants-shared/colors';

	import { UI_FONT_FAMILY } from '../constants';

	type Props = {
		name?: string;
		// drawn after the clock in place of the name (e.g. the game logo)
		children?: Snippet;
	};

	const props: Props = $props();
	const reactiveDate = new SvelteDate();
	const clock = $derived(
		reactiveDate.toLocaleTimeString('en-US', {
			hour: 'numeric',
			minute: 'numeric',
			hour12: false,
		}),
	);
	const textProps = {
		style: {
			fontFamily: UI_FONT_FAMILY,
			fontSize: REM * 1.5,
			fontWeight: '400',
			lineHeight: REM * 2,
			fill: WHITE,
		},
	} as const;

	let clockSizes = $state({ width: 0, height: 0 });

	$effect(() => {
		const interval = setInterval(() => {
			reactiveDate.setTime(Date.now());
		}, 1000);

		return () => {
			clearInterval(interval);
		};
	});
</script>

<Text text={clock} onresize={(value) => (clockSizes = value)} {...textProps} />
{#if props.children}
	<Container x={clockSizes.width + REM * 0.75}>
		{@render props.children()}
	</Container>
{:else}
	<Text text={props.name ?? ''} x={clockSizes.width + 5} {...textProps} />
{/if}
