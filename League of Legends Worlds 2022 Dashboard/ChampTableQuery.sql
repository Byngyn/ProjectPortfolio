-- Cleaning Champ Table

SELECT 
	champion as ChampionName,
	sum_total as Picks,
	win_total as Wins,
	lose_total as Losses,
	winrate_total as WinRate,
	pick_rate as PickRate,
	sum_blue_side as BlueSidePicks,
	win_blue_side as BlueSideWins,
	lose_blue_side as BlueSideLosses,
	winrate_blue_side as BlueSideWinRate,
	sum_red_side as RedSidePicks,
	win_red_side as RedSideWins,
	lose_red_side as RedSideLosses,
	winrate_red_side as RedSideWinRate,
	sum_bans as Bans,
	ban_rate as BanRate,
	sum_pick_ban as PicksAndBans,
	pick_ban_rate as PickBanRate
FROM wc_champions