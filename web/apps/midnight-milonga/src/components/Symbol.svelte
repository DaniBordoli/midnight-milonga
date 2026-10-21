<script lang="ts">
	import { GAME_FONT } from '../game/constants';
	import SymbolSprite from './SymbolSprite.svelte';
	import { getSymbolInfo } from '../game/utils';
	import type { SymbolState, RawSymbol } from '../game/types';
	import { BitmapText } from 'pixi-svelte';

	type Props = {
		x?: number;
		y?: number;
		state: SymbolState;
		rawSymbol: RawSymbol;
		oncomplete?: () => void;
		loop?: boolean;
	};

	const props: Props = $props();
	const symbolInfo = $derived(getSymbolInfo({ rawSymbol: props.rawSymbol, state: props.state }));
</script>

<!-- every Midnight Milonga symbol state is a sprite (no spine animations) -->
<SymbolSprite {symbolInfo} x={props.x} y={props.y} oncomplete={props.oncomplete} />

{#if props.rawSymbol.multiplier}
	<BitmapText
		anchor={0.5}
		x={props.x}
		y={props.y}
		text={`${props.rawSymbol.multiplier}X`}
		style={{
			fontFamily: GAME_FONT,
			fill: 0xf2d692,
			fontSize: 50,
		}}
	/>
{/if}
