<script lang="ts">
	import { onDestroy } from 'svelte';

	import { Container, Rectangle, Sprite } from 'pixi-svelte';
	import { FadeContainer, LoadingProgress } from 'components-pixi';
	import { MainContainer } from 'components-layout';

	import { getContext } from '../game/context';
	import { SYMBOL_SIZE } from '../game/constants';
	import TransitionAnimation from './TransitionAnimation.svelte';
	import PressToContinue from './PressToContinue.svelte';

	type Props = {
		onloaded: () => void;
	};

	// Own loading screen: Stake does not allow the Stake Engine loader, logo or splash screen.
	const props: Props = $props();
	const context = getContext();

	const BACKGROUND = { width: 2048, height: 1143 };
	// art aspects from tools/process_cartoon_loading.py: logo 1209 x 497, bar frame 689 x 118
	const TITLE = { width: SYMBOL_SIZE * 4.6, height: SYMBOL_SIZE * 4.6 * (497 / 1209) };
	const BAR = { width: SYMBOL_SIZE * 4.2, height: SYMBOL_SIZE * 4.2 * (118 / 689) };

	const canvas = $derived(context.stateLayoutDerived.canvasSizes());
	const coverScale = $derived(Math.max(canvas.width / BACKGROUND.width, canvas.height / BACKGROUND.height));

	let loadingType = $state<'start' | 'transition'>('start');
	let spin = $state(0);
	const timer = setInterval(() => (spin += 0.06), 16);
	onDestroy(() => clearInterval(timer));
</script>

<FadeContainer show={loadingType === 'start'}>
	<Sprite
		key="fxLoadingBg"
		anchor={0.5}
		x={canvas.width / 2}
		y={canvas.height / 2}
		width={BACKGROUND.width * coverScale}
		height={BACKGROUND.height * coverScale}
	/>
	<Rectangle {...canvas} backgroundColor={0x000000} backgroundAlpha={0.35} />

	<MainContainer>
		<Container
			x={context.stateLayoutDerived.mainLayout().width * 0.5}
			y={context.stateLayoutDerived.mainLayout().height * 0.42}
		>
			<Sprite key="fxTitle" anchor={0.5} y={-SYMBOL_SIZE * 0.6} {...TITLE} />
			{#if !context.stateApp.loaded}
				<Sprite
					key="fxLoadingRose"
					anchor={0.5}
					y={SYMBOL_SIZE * 1.15}
					width={SYMBOL_SIZE * 0.9}
					height={SYMBOL_SIZE * 0.9}
					rotation={spin}
				/>
				<LoadingProgress x={-BAR.width / 2} y={SYMBOL_SIZE * 1.9} width={BAR.width} height={BAR.height}>
					{#snippet background(sizes)}
						<Rectangle {...sizes} backgroundColor={0x120c0c} backgroundAlpha={0.9} borderRadius={8} />
					{/snippet}
					{#snippet progress(sizes)}
						<Rectangle {...sizes} backgroundColor={0xdeb862} borderRadius={8} />
					{/snippet}
					{#snippet frame(sizes)}
						<Sprite key="fxLoadingBar" {...sizes} />
					{/snippet}
				</LoadingProgress>
			{/if}
		</Container>
	</MainContainer>
</FadeContainer>

<FadeContainer show={loadingType === 'start' && context.stateApp.loaded}>
	<PressToContinue onpress={() => (loadingType = 'transition')} />
</FadeContainer>

<FadeContainer show={loadingType === 'transition'}>
	<TransitionAnimation oncomplete={props.onloaded} />
</FadeContainer>
