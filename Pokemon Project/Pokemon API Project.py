#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Initial Setup
import requests
import pandas as pd
import numpy as np
import string

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_colwidth', 500)


# In[2]:


#Initial get request
movelist_url = 'https://pokeapi.co/api/v2/move?offset=20&limit=100000'
response = requests.get(movelist_url)

# Normalize Data
data = response.json()
movelist_data = pd.json_normalize(data)

movelist = []
for moves in movelist_data['results']:
    for move in moves:
        move_name = move['name']
        
        move_url = move['url']
        move_response = requests.get(move_url)
        move_response = move_response.json()
        
        move_accuracy = move_response['accuracy']
        move_class = move_response['damage_class']['name']
        move_power = move_response['power']
        move_pp = move_response['pp']
        move_priority = move_response['priority']
        move_type = move_response['type']['name']
        
        case = {'name': move_name,
                'accuracy': move_accuracy, 
                'class':move_class,
                'power':move_power,
                'pp':move_pp,
                'priority':move_priority,
                'type': move_type
           }
        movelist.append(case)
        
movelist


# In[3]:


movelist_df = pd.DataFrame.from_dict(movelist)
movelist_df


# In[4]:


#Initial get request
abilites_url = 'https://pokeapi.co/api/v2/ability?offset=20&limit=1000'
response = requests.get(abilites_url)

# Normalize Data
data = response.json()
abilitylist_data = pd.json_normalize(data)

abilitylist = []
for abilities in abilitylist_data['results']:
    for ability in abilities:
        ability_name = ability['name']
        
        ability_url = ability['url']
        ability_response = requests.get(ability_url)
        ability_response = ability_response.json()
        
        # getting description
        ability_desc = ability_response['effect_entries']
    
        #appending to list
        case = {'name': ability_name,
                'effect': ability_desc
               }
        abilitylist.append(case)

abilitylist_df = pd.DataFrame.from_dict(abilitylist)
abilitylist_df


# In[5]:


#Initial get request
types_url = 'https://pokeapi.co/api/v2/type'
response = requests.get(types_url)

# Normalize Data
data = response.json()
types_data = pd.json_normalize(data)

types_data
typelist = []
for types in types_data['results']:
    for type in types:
        type_name = type['name']
        
        type_url = type['url']
        type_response = requests.get(type_url)
        type_response = type_response.json()
        
        double_damage_from_str = ""
        for x in type_response['damage_relations']['double_damage_from']:
            name = x['name']
            double_damage_from_str = double_damage_from_str + name + " "
    
        double_damage_to_str = ""
        for x in type_response['damage_relations']['double_damage_to']:
            name = x['name']
            double_damage_to_str = double_damage_to_str + name + " "
    
        half_damage_from_str = ""
        for x in type_response['damage_relations']['half_damage_from']:
            name = x['name']
            half_damage_from_str = half_damage_from_str + name + " "
    
        half_damage_to_str = ""
        for x in type_response['damage_relations']['half_damage_to']:
            name = x['name']
            half_damage_to_str = half_damage_to_str + name + " "
    
        #appending to list
        case = {'type': type_name,
                'double_damage_from': double_damage_from_str,
                'double_damage_to': double_damage_to_str,
                'half_damage_from_str': half_damage_from_str,
                'half_damage_to_str': half_damage_to_str
               }
        typelist.append(case)

typelist_df = pd.DataFrame.from_dict(typelist)
typelist_df


# In[6]:


pokemon_url = 'https://pokeapi.co/api/v2/pokemon?limit=898&offset=0'
response = requests.get(pokemon_url)

# Normalize Data
data = response.json()
pokemon_data = pd.json_normalize(data)
pokemon_data 

pokemonmovelist = []
for pokemons in pokemon_data['results']:
    for pokemon in pokemons:
        pokemon_name = pokemon['name']
        
        pokemon_url = pokemon['url']
        pokemon_response = requests.get(pokemon_url)
        pokemon_response = pokemon_response.json()
        
        moves = pokemon_response['moves']
        
        pokemon_movelist = ""
        for i in moves:
            pokemon_move = i['move']['name']
            pokemon_movelist = pokemon_movelist + pokemon_move + " "
            
        case = {'name': pokemon_name,
                'moves': pokemon_movelist}
        pokemonmovelist.append(case)
    
pokemonmovelist_df = pd.DataFrame.from_dict(pokemonmovelist)
pokemonmovelist_df


# In[7]:


pokemonabilitylist = []
for pokemons in pokemon_data['results']:
    for pokemon in pokemons:
        pokemon_name = pokemon['name']
        
        pokemon_url = pokemon['url']
        pokemon_response = requests.get(pokemon_url)
        pokemon_response = pokemon_response.json()
        
        abilities = pokemon_response['abilities']
        
        pokemon_abilitylist = ""
        for i in abilities:
            pokemon_ability = i['ability']['name']
            pokemon_abilitylist = pokemon_abilitylist + pokemon_ability + " "
        
        case = {'name': pokemon_name,
                'abilities': pokemon_abilitylist}
        pokemonabilitylist.append(case)
    
pokemonabilitylist_df = pd.DataFrame.from_dict(pokemonabilitylist)
pokemonabilitylist_df


# In[8]:


pokemonstatlist = []
for pokemons in pokemon_data['results']:
    for pokemon in pokemons:
        pokemon_name = pokemon['name']
        pokemon_url = pokemon['url']
        pokemon_response = requests.get(pokemon_url)
        pokemon_response = pokemon_response.json()
        
        stats = pokemon_response['stats']
        
        stat_str = ""
        for i in stats:
            stat = i['base_stat']
            statname = i['stat']['name']
            stat_str = stat_str + statname + ":" + str(stat) + " "
        
        case = {'name': pokemon_name,
                'stats': stat_str}
        pokemonstatlist.append(case)

pokemonstatlist_df = pd.DataFrame.from_dict(pokemonstatlist)
pokemonstatlist_df


# In[9]:


pokemontypelist = []
for pokemons in pokemon_data['results']:
    for pokemon in pokemons:
        pokemon_name = pokemon['name']
        
        pokemon_url = pokemon['url']
        pokemon_response = requests.get(pokemon_url)
        pokemon_response = pokemon_response.json()
        
        types = pokemon_response['types']
        
        pokemon_typelist = ""
        for i in types:
            pokemon_type = i['type']['name']
            pokemon_typelist = pokemon_typelist + pokemon_type + " "
        
        case = {'name': pokemon_name,
                'type': pokemon_typelist}
        pokemontypelist.append(case)
    
pokemontypelist_df = pd.DataFrame.from_dict(pokemontypelist)
pokemontypelist_df


# In[10]:


# movelist_df.to_csv('movelist.csv', index=False)
abilitylist_df.to_csv('abilitylist.csv', index=False)
typelist_df.to_csv('typelist.csv', index=False)
pokemonstatlist_df.to_csv('pokemonstatlist.csv', index=False)
pokemonabilitylist_df.to_csv('pokemonabilitylist.csv', index=False)
pokemonmovelist_df.to_csv('pokemonmovelist.csv', index=False)
pokemontypelist_df.to_csv('pokemontypelist.csv', index=False)


# In[ ]:




