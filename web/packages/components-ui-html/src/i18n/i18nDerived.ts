import { stateI18nDerived, stateUrlDerived } from 'state-shared';

// stake.us social mode: restricted words (bet, funds...) use Stake's replacement phrases
const social = (normal: string, socialText: string) =>
	stateUrlDerived.social() ? socialText : stateI18nDerived.translate(normal);

export const i18nDerived = {
	bet: () => social('BET', 'PLAY'),
	max: () => stateI18nDerived.translate('MAX'),
	betMenu: () => social('BET MENU', 'PLAY MENU'),
	selectYourBet: () => social('SELECT YOUR BET', 'SELECT YOUR PLAY AMOUNT'),
	confirm: () => stateI18nDerived.translate('CONFIRM'),
	masterVolume: () => stateI18nDerived.translate('MASTER VOLUME'),
	musicVolume: () => stateI18nDerived.translate('MUSIC VOLUME'),
	soundEffectVolume: () => stateI18nDerived.translate('SOUND EFFECT VOLUME'),
	autoSpins: () => stateI18nDerived.translate('AUTO SPINS'),
	numberOfRounds: () => stateI18nDerived.translate('NUMBER OF ROUNDS'),
	advanced: () => stateI18nDerived.translate('ADVANCED'),
	singleWinLimit: () => stateI18nDerived.translate('SINGLE WIN LIMIT'),
	lossLimit: () => stateI18nDerived.translate('LOSS LIMIT'),
	startAutoplay: () => stateI18nDerived.translate('START AUTOPLAY'),
	notification: () => stateI18nDerived.translate('NOTIFICATION'),
	autoSpinsStopInfo: () => stateI18nDerived.translate('AUTO PLAY HAS STOPPED DUE TO'),
	insufficientFunds: () =>
		social(
			'INSUFFICIENT FUNDS TO PLACE THIS BET. PLEASE ADD FUNDS TO YOUR ACCOUNT OR LOWER THE BET LEVEL.',
			'INSUFFICIENT BALANCE FOR THIS PLAY. PLEASE GET COINS OR LOWER THE PLAY AMOUNT.',
		),
	lossLimitReached: () => stateI18nDerived.translate('LOSS LIMIT REACHED'),
	singleWinLimitReached: () => stateI18nDerived.translate('SINGLE WIN LIMIT REACHED'),
	settings: () => stateI18nDerived.translate('SETTINGS'),
};
