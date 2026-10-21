<script lang="ts">
	import { Sprite, Text } from 'pixi-svelte';

	import { UI_BASE_FONT_SIZE, UI_GOLD, UI_FONT_FAMILY } from '../constants';

	type Props = {
		label: string;
		value: string;
		tiled?: boolean;
		stacked?: boolean;
	};

	const props: Props = $props();

	// Midnight Milonga skin: gold caption, ivory amount, on the Art Deco info panel (art ratio 209 / 994)
	const labelStyle = {
		fontFamily: UI_FONT_FAMILY,
		fontWeight: '400',
		fontSize: UI_BASE_FONT_SIZE * 0.8,
		fill: UI_GOLD,
	} as const;

	const valueStyle = {
		fontFamily: UI_FONT_FAMILY,
		fontWeight: '400',
		fontSize: UI_BASE_FONT_SIZE,
		fill: 0xfaf3e0,
	} as const;

	const PANEL_WIDTH = UI_BASE_FONT_SIZE * 3 * (326 / 73);
	const PANEL_HEIGHT = PANEL_WIDTH * (209 / 994);
</script>

{#if props.stacked}
	{#if props.tiled}
		<Sprite y={-20} anchor={{ x: 0.5, y: 0 }} key="uiPanel" width={PANEL_WIDTH} height={PANEL_HEIGHT} />
	{/if}
	<Text anchor={{ x: 0.5, y: 0 }} text={props.label} style={labelStyle} />
	<Text anchor={{ x: 0.5, y: 0 }} text={props.value} style={valueStyle} y={UI_BASE_FONT_SIZE * 0.85} />
{:else}
	{#if props.tiled}
		<Sprite x={-90} anchor={{ x: 0, y: 0.5 }} key="uiPanel" width={PANEL_WIDTH} height={PANEL_HEIGHT} />
	{/if}
	<Text anchor={{ x: 0, y: 0.5 }} text={props.label} style={labelStyle} />
	<Text
		anchor={{ x: 1, y: 0.5 }}
		text={props.value}
		style={valueStyle}
		x={UI_BASE_FONT_SIZE * 10}
	/>
{/if}
