<script lang="ts" module>
	export type EmitterEventFeatureBanner = {
		type: 'featureBanner';
		title: string;
		subtitle?: string;
	};
</script>

<script lang="ts">
	import { Container, Rectangle, Text } from 'pixi-svelte';
	import { FadeContainer } from 'components-pixi';
	import { MainContainer } from 'components-layout';
	import { waitForTimeout } from 'utils-shared/wait';

	import { getContext } from '../game/context';
	import { SYMBOL_SIZE } from '../game/constants';

	// Placeholder banner for El Abrazo / La Rosa Roja until the final animations exist.
	const context = getContext();
	const BANNER = { width: SYMBOL_SIZE * 4.6, height: SYMBOL_SIZE * 1.5 };

	let show = $state(false);
	let title = $state('');
	let subtitle = $state('');

	context.eventEmitter.subscribeOnMount({
		featureBanner: async (emitterEvent) => {
			title = emitterEvent.title;
			subtitle = emitterEvent.subtitle ?? '';
			show = true;
			await waitForTimeout(1100);
			show = false;
			await waitForTimeout(250);
		},
	});
</script>

<FadeContainer {show}>
	<MainContainer>
		<Container x={context.stateGameDerived.boardLayout().x} y={context.stateGameDerived.boardLayout().y}>
			<Rectangle
				x={-BANNER.width / 2}
				y={-BANNER.height / 2}
				width={BANNER.width}
				height={BANNER.height}
				backgroundColor={0x120c0c}
				backgroundAlpha={0.88}
				borderColor={0xdeb862}
				borderWidth={4}
				borderRadius={18}
			/>
			<Text
				anchor={0.5}
				y={subtitle ? -SYMBOL_SIZE * 0.22 : 0}
				text={title}
				style={{
					fontFamily: 'Georgia, serif',
					fontSize: SYMBOL_SIZE * 0.5,
					fontWeight: '700',
					fill: 0xf2d692,
					letterSpacing: 4,
				}}
			/>
			{#if subtitle}
				<Text
					anchor={0.5}
					y={SYMBOL_SIZE * 0.36}
					text={subtitle}
					style={{ fontFamily: 'Georgia, serif', fontSize: SYMBOL_SIZE * 0.3, fill: 0xece5d8 }}
				/>
			{/if}
		</Container>
	</MainContainer>
</FadeContainer>
