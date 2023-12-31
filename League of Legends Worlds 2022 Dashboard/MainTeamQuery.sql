SELECT 
  [team] as Team, 
  [games_played] as NumberofGamesPlayed, 
  [wins] as Wins, 
  [loses] as Losses, 
  [average_game_duration] as AverageGameDuration,
  [kills] as Kills, 
  [deaths] as Deaths, 
  [kd] as KD, 
  [combined_kills_per_minute] as CombinedKillsPerMin, 
  [gold_percent_rating] as GoldPercentRating, 
  [gold_spent_difference] as GoldSpentDiff, 
  [early_game_rating] as EarlyGameRating, 
  [mid_late_rating] as MidLateRating, 
  [gold_diff_15] as GoldDiff@15, 
  [first_blood_rate] as FirstBloodRate, 
  [first_tower_rate] as FirstTowerRate, 
  [first_to_three_towers_rate] as FirsttoThreeTowersRate, 
  [turrent_plates_destroyed] as TurretPlatesDestroyed, 
  [rift_herald_rate] as RiftHeraldRate, 
  [first_dragon_rate] as FirstDragonRate, 
  [dragon_control_rate] as DragonControlRate, 
  [elder_dragon_rate] as ElderDragonRate, 
  [first_baron_rate] as FirstBaronRate, 
  [baron_control_rate] as BaronControlRate, 
  [lane_control] as LaneControl, 
  [jungle_control] as JungleControl, 
  [wards_per_minute] as WardsPerMin, 
  [control_wards_per_minute] as ControlWardsPerMin, 
  [wards_cleared_per_minute] as WardsClearedPerMin
FROM 
  [League2022Project].[dbo].[wc_teams_main]
