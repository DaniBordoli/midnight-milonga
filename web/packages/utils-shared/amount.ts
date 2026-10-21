import { stateI18n } from 'state-shared';

import { BOOK_AMOUNT_MULTIPLIER } from 'constants-shared/bet';
import { stateBet } from 'state-shared';

// social-casino coins: shown as "10.00 SC" (amount first), never with a currency symbol
const NO_LOCALISATION_CURRENCY_MAP: Record<string, string> = {
	XGC: 'GC',
	XSC: 'SC',
	XEC: 'SC',
};

// decimals a currency normally shows (USD/EUR 2, JPY 0); coins always 2
export const currencyDecimals = (currency: string = stateBet.currency) => {
	if (currency in NO_LOCALISATION_CURRENCY_MAP) return 2;
	try {
		return new Intl.NumberFormat('en', { style: 'currency', currency }).resolvedOptions().maximumFractionDigits ?? 2;
	} catch {
		return 2;
	}
};

// bookEventAmount: is the amount or win numbers in the events of books, e.g. the amount in setTotalWin bookEvent
// {
// 	"index": 3,
// 	"type": "setTotalWin",
// 	"amount": 100
// },
// if betting on $1,   100 bookEventAmount equals to $1.    betAmountMultiplier is (100 / BOOK_AMOUNT_MULTIPLIER =) 1
// if betting on $1,    50 bookEventAmount equals to $0.5.  betAmountMultiplier is ( 50 / BOOK_AMOUNT_MULTIPLIER =) 0.5
// if betting on $0.5, 100 bookEventAmount equals to $0.5.  betAmountMultiplier is (100 / BOOK_AMOUNT_MULTIPLIER =) 1
// if betting on $0.5,  50 bookEventAmount equals to $0.25. betAmountMultiplier is ( 50 / BOOK_AMOUNT_MULTIPLIER =) 0.5

export const bookEventAmountToBetAmountMultiplier = (bookEventAmount: number) =>
	bookEventAmount / BOOK_AMOUNT_MULTIPLIER;

export const bookEventAmountToNormalisedAmount = (bookEventAmount: number) => {
	const betAmountMultiplier = bookEventAmountToBetAmountMultiplier(bookEventAmount);
	return stateBet.wageredBetAmount * betAmountMultiplier;
};

export const numberToFloat = (value: number) => Number.parseFloat(`${value}`);

// Amounts keep the currency's own decimals (JPY has none). A non-zero amount smaller than the currency's
// smallest unit (a sub-cent payout) shows the extra decimals it needs instead of rounding to 0 or 0.01.
export const numberToCurrencyString = (value: number) => {
	const decimals = currencyDecimals();
	const subUnit = value !== 0 && Math.abs(value) < 10 ** -decimals;
	const maximumFractionDigits = subUnit ? 6 : decimals;

	if (stateBet.currency in NO_LOCALISATION_CURRENCY_MAP) {
		const amount = stateI18n.i18n.number(numberToFloat(value), { minimumFractionDigits: decimals, maximumFractionDigits });
		return `${amount} ${NO_LOCALISATION_CURRENCY_MAP[stateBet.currency]}`;
	}

	return stateI18n.i18n.number(value, {
		minimumFractionDigits: decimals,
		maximumFractionDigits,
		style: 'currency',
		currency: stateBet.currency,
	});
};

export const bookEventAmountToCurrencyString = (bookEventAmount: number) => {
	const normalisedAmount = bookEventAmountToNormalisedAmount(bookEventAmount);
	return numberToCurrencyString(normalisedAmount);
};
