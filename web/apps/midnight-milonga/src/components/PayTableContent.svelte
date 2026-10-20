<script lang="ts">
	import { stateUrlDerived } from 'state-shared';

	import config from '../game/config';

	// Paytable built from the math config, so the values shown always match the published math.
	const social = stateUrlDerived.social();
	const amountWord = social ? 'play amount' : 'bet';

	const images: Record<string, string> = {
		W: new URL('../../assets/sprites/milonga/w.png', import.meta.url).href,
		H1: new URL('../../assets/sprites/milonga/h1.png', import.meta.url).href,
		H2: new URL('../../assets/sprites/milonga/h2.png', import.meta.url).href,
		H3: new URL('../../assets/sprites/milonga/h3.png', import.meta.url).href,
		H4: new URL('../../assets/sprites/milonga/h4.png', import.meta.url).href,
		L1: new URL('../../assets/sprites/milonga/l1.png', import.meta.url).href,
		L2: new URL('../../assets/sprites/milonga/l2.png', import.meta.url).href,
		L3: new URL('../../assets/sprites/milonga/l3.png', import.meta.url).href,
		L4: new URL('../../assets/sprites/milonga/l4.png', import.meta.url).href,
		BM: new URL('../../assets/sprites/milonga/bm.png', import.meta.url).href,
		BF: new URL('../../assets/sprites/milonga/bf.png', import.meta.url).href,
		S: new URL('../../assets/sprites/milonga/s.png', import.meta.url).href,
	};
	const names: Record<string, string> = {
		H1: 'Bandoneón',
		H2: 'Rose',
		H3: 'Fedora',
		H4: 'Champagne',
		L1: 'Spade',
		L2: 'Heart',
		L3: 'Diamond',
		L4: 'Club',
		W: 'Golden Wild (all-wild ways)',
	};
	const order = ['W', 'H1', 'H2', 'H3', 'H4', 'L1', 'L2', 'L3', 'L4'];

	type PayEntry = Record<string, number>;
	const pays = (symbol: string) =>
		((config.symbols as Record<string, { paytable?: PayEntry[] }>)[symbol]?.paytable ?? [])
			.map((entry) => Object.entries(entry)[0])
			.sort((a, b) => Number(b[0]) - Number(a[0]));
</script>

<div class="paytable">
	<h2>PAYTABLE</h2>
	<p>
		Values are multiples of the total {amountWord}, per way. Wins {social ? 'count' : 'pay'} left to right on adjacent
		reels, starting from the leftmost reel, for 3 or more matching symbols.
	</p>

	<div class="grid">
		{#each order as symbol}
			<div class="card">
				<img src={images[symbol]} alt={names[symbol]} />
				<div>
					<div class="name">{names[symbol]}</div>
					{#each pays(symbol) as [kind, value]}
						<div class="pay"><span>{kind}</span><span>{value}x</span></div>
					{/each}
				</div>
			</div>
		{/each}
	</div>

	<h3>SPECIAL SYMBOLS</h3>
	<div class="specials">
		<div class="card wide">
			<img src={images.BM} alt="Bailarín" />
			<div>
				<div class="name">Bailarín (Wild)</div>
				Appears on reels 1 and 2. Substitutes for all symbols except the Entrada.
			</div>
		</div>
		<div class="card wide">
			<img src={images.BF} alt="Bailarina" />
			<div>
				<div class="name">Bailarina (Wild)</div>
				Appears on reels 4 and 5. Substitutes for all symbols except the Entrada.
			</div>
		</div>
		<div class="card wide">
			<img src={images.S} alt="Entrada" />
			<div>
				<div class="name">Entrada (Scatter)</div>
				3, 4 or 5 Entradas anywhere trigger La Pista free spins.
			</div>
		</div>
	</div>
</div>

<style lang="scss">
	.paytable {
		text-align: left;
		max-width: 900px;
		margin: 0 auto;
	}
	h2,
	h3 {
		color: #f2d692;
		letter-spacing: 0.1em;
		margin: 0.6rem 0;
	}
	p {
		font-size: 0.85rem;
		opacity: 0.85;
	}
	.grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(190px, 1fr));
		gap: 0.6rem;
	}
	.specials {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
		gap: 0.6rem;
	}
	.card {
		display: flex;
		gap: 0.6rem;
		align-items: center;
		background: rgba(0, 0, 0, 0.45);
		border: 1px solid rgba(222, 184, 98, 0.45);
		border-radius: 10px;
		padding: 0.5rem;
		font-size: 0.8rem;
	}
	img {
		width: 64px;
		height: 64px;
		border-radius: 8px;
		flex-shrink: 0;
	}
	.name {
		font-weight: bold;
		color: #f2d692;
		margin-bottom: 0.2rem;
	}
	.pay {
		display: flex;
		justify-content: space-between;
		gap: 1rem;
		min-width: 80px;
	}
</style>
