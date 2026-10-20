<script lang="ts">
	import { stateUrlDerived } from 'state-shared';

	import config from '../game/config';

	// Game rules required by Stake: features, modes with cost, RTP and max win, UI guide and general disclaimer.
	// Social mode (stake.us) wording avoids restricted words (bet, buy, pay, cost, stake, cash...).
	const social = stateUrlDerived.social();
	const t = (normal: string, socialText: string) => (social ? socialText : normal);

	const percent = (rtp: number) => `${(rtp * 100).toFixed(2)}%`;
	const maxWin = (value: number) => `${value.toLocaleString('en-US')}x`;
	const modes = [
		{ name: 'Base game', key: 'base' as const, text: t('Standard spin at 1x the bet.', 'Standard spin at 1x the play amount.') },
		{
			name: 'Noche de Gala',
			key: 'ante' as const,
			text: t(
				`Spins at ${config.betModes.ante.cost}x the bet with twice the chance of triggering La Pista. Stays active until turned off.`,
				`Spins played for ${config.betModes.ante.cost}x the play amount with twice the chance of reaching La Pista. Stays on until turned off.`,
			),
		},
		{
			name: 'La Pista',
			key: 'bonus' as const,
			text: t(
				`Instantly triggers La Pista free spins for ${config.betModes.bonus.cost}x the bet.`,
				`Goes straight to La Pista free spins, played for ${config.betModes.bonus.cost}x the play amount.`,
			),
		},
		{
			name: 'La Última Tanda',
			key: 'super' as const,
			text: t(
				`Instantly triggers free spins for ${config.betModes.super.cost}x the bet. The Compás starts at x5 and the first free spin always has an Abrazo.`,
				`Goes straight to free spins, played for ${config.betModes.super.cost}x the play amount. The Compás starts at x5 and the first free spin always has an Abrazo.`,
			),
		},
	];
</script>

<div class="rules">
	<h2>GAME RULES</h2>

	<h3>HOW TO WIN</h3>
	<p>
		Midnight Milonga is played on 5 reels and 4 rows with 1024 ways. Wins are formed by 3 or more matching
		symbols on adjacent reels, starting from the leftmost reel. Each win equals the symbol value times the
		number of ways, as a multiple of the total {t('bet', 'play amount')}. Wins of different symbols are added.
	</p>

	<h3>WILDS</h3>
	<p>
		The Bailarín appears on reels 1 and 2 and the Bailarina on reels 4 and 5. Both are Wild and substitute for
		all symbols except the Entrada. Ways made only of Wilds {t('pay', 'win')} as the Golden Wild.
	</p>

	<h3>EL ABRAZO</h3>
	<p>
		When the Bailarín and the Bailarina land in the same spin, they dance together and the Bailarín's row becomes
		Wild on all 5 reels. Entradas in that row stay in place.
	</p>

	<h3>LA ROSA ROJA</h3>
	<p>
		In the base game, a red rose may be thrown on any winning spin and multiply the total win of that spin by
		x2, x3, x5 or x10.
	</p>

	<h3>LA PISTA · FREE SPINS</h3>
	<p>
		3, 4 or 5 Entradas award 10, 12 or 15 free spins. During free spins, 3 or more Entradas award 5 more free
		spins.
	</p>
	<p>
		<strong>Compás:</strong> a multiplier applied to every win during free spins. It starts at x1 and increases
		by 1 with every Abrazo, including the spin where the Abrazo lands. It does not reset during the free spins.
	</p>

	<h3>GAME MODES</h3>
	<table>
		<thead>
			<tr><th>Mode</th><th>Description</th><th>RTP</th><th>Max win</th></tr>
		</thead>
		<tbody>
			{#each modes as mode}
				<tr>
					<td>{mode.name}</td>
					<td>{mode.text}</td>
					<td>{percent(config.betModes[mode.key].rtp)}</td>
					<td>{maxWin(config.betModes[mode.key].max_win)}</td>
				</tr>
			{/each}
		</tbody>
	</table>
	<p>
		Max win is {maxWin(config.betModes.base.max_win)} the {t('bet', 'play amount')} in every mode. When it is
		reached, the round ends and the max win is awarded.
	</p>

	<h3>HOW TO PLAY</h3>
	<ul>
		<li><strong>{t('BET', 'SPIN')} button / space bar:</strong> starts a spin.</li>
		<li><strong>+ and -:</strong> change the {t('bet', 'play amount')}.</li>
		<li><strong>{t('BUY BONUS', 'PLAY BONUS')}:</strong> opens the game modes. Every option asks for confirmation.</li>
		<li><strong>AUTO SPIN:</strong> plays several spins in a row after you confirm the settings.</li>
		<li><strong>TURBO:</strong> faster spins and animations.</li>
		<li><strong>MENU:</strong> paytable, game rules, settings and sound on/off.</li>
	</ul>

	<h3>GENERAL DISCLAIMER</h3>
	<p class="disclaimer">
		Malfunction voids all wins and plays. A consistent internet connection is required. In the event of a
		disconnection, reload the game to finish any uncompleted rounds. The expected return is calculated over many
		plays. The game display is not representative of any physical device and is for illustrative purposes only.
		Winnings are settled according to the amount received from the Remote Game Server and not from events within
		the web browser. TM and © 2026 Engine.
	</p>
</div>

<style lang="scss">
	.rules {
		text-align: left;
		max-width: 900px;
		margin: 0 auto;
		font-size: 0.85rem;
		line-height: 1.35;
	}
	h2,
	h3 {
		color: #f2d692;
		letter-spacing: 0.1em;
		margin: 0.9rem 0 0.3rem;
	}
	table {
		width: 100%;
		border-collapse: collapse;
		font-size: 0.8rem;
	}
	th,
	td {
		border-bottom: 1px solid rgba(222, 184, 98, 0.35);
		padding: 0.35rem;
		text-align: left;
		vertical-align: top;
	}
	th {
		color: #f2d692;
	}
	ul {
		padding-left: 1.2rem;
	}
	.disclaimer {
		opacity: 0.85;
		font-size: 0.75rem;
	}
</style>
