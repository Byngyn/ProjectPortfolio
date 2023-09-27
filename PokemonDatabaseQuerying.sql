-- In this project, we will be using SQL queries for exploratory data analysis
-- When assembling a Pokémon team, understanding their key stats like attack, defense, and typing is crucial.
-- This knowledge forms the foundation for creating a championship-winning team.
-- By employing queries, we can identify which Pokémon excel in various attributes and abilities.

-- Full Table
Select *
From PortfolioProject..Pokemon$
order by 1;

-- Order the pokemon total stats with the highest being at the top
-- From this table at a glance, we can see at glance which pokemon have the highest total stats
Select #, Name, Total, Generation, Legendary
From PortfolioProject..Pokemon$
order by Total desc;

-- Now, order the same stats but with pokemon from a specific generation, like generation 1
-- This is useful for certain tournament rulesets that ban certain pokemon
Select #, Name, Total, Generation, Legendary
From PortfolioProject..Pokemon$
Where Generation like 1
order by Total desc;

-- However, total stats isn't a clear indicator if a pokemon are good, some are specialized
-- Now, lets group the offensive and defensive stats together and see the respective rankings
Select #, Name, Attack + "Sp# Atk" as TotalOffense
From PortfolioProject..Pokemon$
order by TotalOffense desc;

Select #, Name, Defense + "Sp# Def" as TotalDefense
From PortfolioProject..Pokemon$
order by TotalDefense desc;

-- Typing is important because pokemon can be super effective or not very effective to others
-- Now, let's explore typings, and count the total amount of pokemon for each type
-- Find the total amount of pokemon for each type 1
Select "Type 1", COUNT("Type 1") as AmountOfType1
From PortfolioProject..Pokemon$
Group by "Type 1"
Order by AmountOfType1 desc;

-- Find the total amount of pokemon for each type 2
Select "Type 2", COUNT("Type 2") as AmountOfType2
From PortfolioProject..Pokemon$
Group by "Type 2"
Order by AmountOfType2 desc;

-- Some pokemon have a typing, but it is in type 2 instead of type 1
-- So, clean the data by combining the two and call the column Typing
With PokemonTyping (Name, Typing, Total, HP, Attack, Defense, Speed, Generation, Legendary)
As 
(Select Name, Concat("Type 1", ' ', "Type 2") As Typing, Total, HP, Attack, Defense, Speed, Generation, Legendary
From PortfolioProject..Pokemon$)
Select * From PokemonTyping
Order by 1;

-- Using the white space created, we can filter out only dual typings and single typings
With PokemonTyping ("#", Name, Typing, Total, HP, Attack, Defense, "Sp# Atk", "Sp# Def", Speed, Generation, Legendary)
As 
(Select "#", Name, Concat("Type 1", ' ', "Type 2") As Typing, Total, HP, Attack, Defense, "Sp# Atk", "Sp# Def", Speed, Generation, Legendary
From PortfolioProject..Pokemon$)
Select * From PokemonTyping
Where Typing not like '% '
--Where Typing like '% ' for single typings

--We can create a temp table for the cleaned pokemon typing list
DROP Table if exists #PokemonTyping;
Create Table #PokemonTyping
(
"#" numeric, 
Name nvarchar(255), 
Typing nvarchar(255), 
Total numeric, 
HP numeric, 
Attack numeric, 
Defense numeric, 
"Sp# Atk" numeric, 
"Sp# Def" numeric, 
Speed numeric, 
Generation numeric, 
Legendary numeric
)
Insert into #PokemonTyping
Select "#", Name, Concat("Type 1", ' ', "Type 2") As Typing, Total, HP, Attack, Defense, "Sp# Atk", "Sp# Def", Speed, Generation, Legendary
From PortfolioProject..Pokemon$
Select * From #PokemonTyping

-- Finally, we can accurately count the amount of pokemon for each unique typing
Select "Typing", COUNT("Typing") as TotalAmount
From #PokemonTyping
Group by "Typing"
Order by TotalAmount desc; 