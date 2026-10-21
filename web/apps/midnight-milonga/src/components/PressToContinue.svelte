<script lang="ts">
	import { MainContainer, OnPressFullScreen } from 'components-layout';
	import { OnHotkey } from 'components-shared';
	import { Text } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { SYMBOL_SIZE, GAME_FONT } from '../game/constants';

	type Props = {
		onpress: () => void;
	};

	const props: Props = $props();
	const context = getContext();
</script>

<MainContainer alignVertical="bottom">
	<Text
		anchor={{ x: 0.5, y: 1 }}
		x={context.stateLayoutDerived.mainLayout().width * 0.5}
		y={context.stateLayoutDerived.mainLayout().height - SYMBOL_SIZE * 0.25}
		text="PRESS ANYWHERE TO CONTINUE"
		style={{
			fontFamily: GAME_FONT,
			fontSize: SYMBOL_SIZE * 0.3,
			fontWeight: '400',
			fill: 0xf2d692,
			letterSpacing: 4,
			dropShadow: { color: 0x000000, blur: 6, distance: 0, alpha: 0.9 },
		}}
	/>
</MainContainer>
<OnHotkey hotkey="Space" onpress={() => props.onpress()} />
<OnPressFullScreen onpress={() => props.onpress()} />
