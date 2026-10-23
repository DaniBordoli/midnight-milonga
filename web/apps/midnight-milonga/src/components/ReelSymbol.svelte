<script lang="ts">
	import { Tween } from 'svelte/motion';

	import { Container } from 'pixi-svelte';

	import Symbol from './Symbol.svelte';
	import SymbolWrap from './SymbolWrap.svelte';
	import { getContext } from '../game/context';
	import { getSymbolInfo, getSymbolX } from '../game/utils';
	import type { ReelSymbol } from '../game/stateGame.svelte';

	type Props = {
		reelIndex: number;
		reelSymbol: ReelSymbol;
	};

	// while a reel is anticipated, the stopped reels darken except their scatters, so the scatters that set
	// up the feature stand out
	const DIM_BRIGHTNESS = 0.4;

	const props: Props = $props();
	const context = getContext();
	const symbolInfo = $derived(
		getSymbolInfo({ rawSymbol: props.reelSymbol.rawSymbol, state: props.reelSymbol.symbolState }),
	);
	const dimmed = $derived(
		props.reelSymbol.rawSymbol.name !== 'S' &&
			!context.stateGame.board[props.reelIndex].reelState.anticipating &&
			context.stateGame.board.some((reel) => reel.reelState.anticipating),
	);
	const brightness = new Tween(1, { duration: 250 });
	$effect(() => {
		brightness.set(dimmed ? DIM_BRIGHTNESS : 1);
	});
	const tint = $derived(Math.round(brightness.current * 255) * 0x010101);
</script>

<SymbolWrap
	x={getSymbolX(props.reelIndex)}
	y={props.reelSymbol.symbolY()}
	animating={(symbolInfo.type === 'spine' || symbolInfo.type === 'spriteSheet') &&
		(props.reelSymbol.symbolState === 'land' || props.reelSymbol.symbolState === 'win')}
>
	<Container {tint}>
		<Symbol
			state={props.reelSymbol.symbolState}
			rawSymbol={props.reelSymbol.rawSymbol}
			oncomplete={() => {
				if (props.reelSymbol.symbolState === 'win') props.reelSymbol.oncomplete();
				if (props.reelSymbol.symbolState === 'land') props.reelSymbol.symbolState = 'static';
			}}
		/>
	</Container>
</SymbolWrap>
