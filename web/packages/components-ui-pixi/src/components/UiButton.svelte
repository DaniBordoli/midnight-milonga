<script lang="ts">
	import { Rectangle, Sprite, Text } from 'pixi-svelte';
	import { Button, type ButtonProps } from 'components-pixi';

	import type { ButtonIcon } from '../types';
	import type { Snippet } from 'svelte';
	import { i18nDerived } from '../i18n/i18nDerived';
	import { UI_BASE_FONT_SIZE, UI_GOLD, UI_FONT_FAMILY } from '../constants';

	type Props = Omit<ButtonProps, 'children'> & {
		icon: ButtonIcon;
		sizes: { width: number; height: number };
		active?: boolean;
		children?: Snippet;
		variant?: 'dark' | 'light';
	};

	const { icon, active, variant: _variant, children: childrenFromParent, ...buttonProps }: Props = $props();

	// Midnight Milonga skin. Bar controls are a round Art Deco button with a gold line icon; menu-drawer
	// entries are a square plate with their name, so every menu action reads clearly.
	const ICON_KEYS: Partial<Record<ButtonIcon, string>> = {
		decrease: 'uiIconDecrease',
		increase: 'uiIconIncrease',
		menu: 'uiIconMenu',
		turbo: 'uiIconTurbo',
		autoSpin: 'uiIconAutoSpin',
	};
	const iconKey = $derived(ICON_KEYS[icon]);
	const scaleFor = (hovered: boolean, pressed: boolean) => (pressed ? 0.94 : hovered ? 1.04 : 1);
</script>

<Button {...buttonProps}>
	{#snippet children({ center, hovered, pressed })}
		{@const scale = scaleFor(hovered, pressed)}
		{@const alpha = buttonProps.disabled ? 0.45 : 1}
		{@const { width, height } = buttonProps.sizes}
		{#if iconKey}
			<!-- active (turbo / auto spin on): a gold halo behind the button and a fully lit icon; off: a dimmer icon -->
			{#if active}
				<Rectangle
					{...center}
					anchor={0.5}
					width={width * 1.3 * scale}
					height={height * 1.3 * scale}
					borderRadius={width * 0.65 * scale}
					backgroundColor={UI_GOLD}
					alpha={0.3 * alpha}
					blendMode="add"
				/>
			{/if}
			<Sprite key="uiButtonSmall" {...center} anchor={0.5} width={width * scale} height={height * scale} {alpha} />
			<Sprite
				key={iconKey}
				{...center}
				anchor={0.5}
				scale={(width * 0.42 * scale) / 128}
				tint={active ? 0xffe27a : 0xb8a67e}
				alpha={alpha}
			/>
		{:else}
			<Sprite
				key="uiButtonMenu"
				{...center}
				anchor={0.5}
				width={width * scale}
				height={height * scale}
				tint={active ? 0xfff2c2 : 0xffffff}
				{alpha}
			/>
			<Text
				{...center}
				anchor={0.5}
				{alpha}
				text={i18nDerived[icon]()}
				style={{
					align: 'center',
					wordWrap: true,
					wordWrapWidth: width * 0.7,
					fontFamily: UI_FONT_FAMILY,
					fontWeight: '400',
					fontSize: UI_BASE_FONT_SIZE * 0.46,
					fill: UI_GOLD,
				}}
			/>
		{/if}

		{@render childrenFromParent?.()}
	{/snippet}
</Button>
