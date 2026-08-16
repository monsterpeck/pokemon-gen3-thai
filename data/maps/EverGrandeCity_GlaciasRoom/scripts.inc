EverGrandeCity_GlaciasRoom_MapScripts::
	map_script MAP_SCRIPT_ON_FRAME_TABLE, EverGrandeCity_GlaciasRoom_OnFrame
	map_script MAP_SCRIPT_ON_LOAD, EverGrandeCity_GlaciasRoom_OnLoad
	map_script MAP_SCRIPT_ON_WARP_INTO_MAP_TABLE, EverGrandeCity_GlaciasRoom_OnWarp
	.byte 0

EverGrandeCity_GlaciasRoom_OnWarp:
	map_script_2 VAR_TEMP_1, 0, EverGrandeCity_GlaciasRoom_EventScript_PlayerTurnNorth
	.2byte 0

EverGrandeCity_GlaciasRoom_EventScript_PlayerTurnNorth::
	turnobject LOCALID_PLAYER, DIR_NORTH
	end

EverGrandeCity_GlaciasRoom_OnFrame:
	map_script_2 VAR_ELITE_4_STATE, 2, EverGrandeCity_GlaciasRoom_EventScript_WalkInCloseDoor
	.2byte 0

EverGrandeCity_GlaciasRoom_EventScript_WalkInCloseDoor::
	lockall
	call PokemonLeague_EliteFour_EventScript_WalkInCloseDoor
	setvar VAR_ELITE_4_STATE, 3
	releaseall
	end

EverGrandeCity_GlaciasRoom_OnLoad:
	call_if_set FLAG_DEFEATED_ELITE_4_GLACIA, EverGrandeCity_GlaciasRoom_EventScript_ResetAdvanceToNextRoom
	call_if_eq VAR_ELITE_4_STATE, 3, EverGrandeCity_GlaciasRoom_EventScript_CloseDoor
	end

EverGrandeCity_GlaciasRoom_EventScript_ResetAdvanceToNextRoom::
	call PokemonLeague_EliteFour_EventScript_ResetAdvanceToNextRoom
	return

EverGrandeCity_GlaciasRoom_EventScript_CloseDoor::
	call PokemonLeague_EliteFour_EventScript_CloseDoor
	return

EverGrandeCity_GlaciasRoom_EventScript_Glacia::
	lock
	faceplayer
	goto_if_set FLAG_DEFEATED_ELITE_4_GLACIA, EverGrandeCity_GlaciasRoom_EventScript_PostBattleSpeech
	playbgm MUS_ENCOUNTER_ELITE_FOUR, FALSE
	msgbox EverGrandeCity_GlaciasRoom_Text_IntroSpeech, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_GLACIA, EverGrandeCity_GlaciasRoom_Text_Defeat
	goto EverGrandeCity_GlaciasRoom_EventScript_Defeated
	end

EverGrandeCity_GlaciasRoom_EventScript_PostBattleSpeech::
	msgbox EverGrandeCity_GlaciasRoom_Text_PostBattleSpeech, MSGBOX_DEFAULT
	release
	end

EverGrandeCity_GlaciasRoom_EventScript_Defeated::
	setflag FLAG_DEFEATED_ELITE_4_GLACIA
	call PokemonLeague_EliteFour_SetAdvanceToNextRoomMetatiles
	msgbox EverGrandeCity_GlaciasRoom_Text_PostBattleSpeech, MSGBOX_DEFAULT
	release
	end

EverGrandeCity_GlaciasRoom_Text_IntroSpeech:
.string "{252}{25}{77}{0}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{123}{0}{0}{244}{7}{1}{252}{25}{93}{1}{0}{244}{7}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{46}{2}{0}{244}{5}{1}{252}{25}{31}{0}{0}{244}{7}{1} {252}{25}{29}{2}{0}{244}{8}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{31}{1}{0}{244}{6}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{35}{0}{0}{244}{8}{1}{252}{25}{78}{0}{0}{244}{6}{1}{252}{25}{38}{0}{0}{244}{7}{1}\n{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{82}{1}{0}{244}{7}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{167}{0}{0}{244}{6}{1}{252}{25}{13}{0}{0}{244}{6}{1}{252}{25}{149}{1}{0}{244}{7}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{28}{0}{0}{244}{7}{1}{252}{25}{35}{0}{0}{244}{8}{1}\p{252}{25}{29}{2}{0}{244}{8}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{64}{0}{0}{244}{7}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{28}{0}{0}{244}{7}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{13}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{25}{0}{0}{244}{7}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{41}{0}{0}{244}{6}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{45}{2}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{0}{0}{0}{244}{5}{1}{252}{25}{49}{0}{0}{244}{6}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{15}{2}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}\n{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{42}{1}{0}{244}{8}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{25}{2}{0}{244}{6}{1}{252}{25}{25}{0}{0}{244}{7}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{41}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{35}{2}{0}{244}{7}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{44}{0}{0}{244}{8}{1}{252}{25}{7}{0}{0}{244}{5}{1}{252}{25}{97}{2}{0}{244}{11}{1}{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{1}{2}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}\p{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{66}{1}{0}{244}{7}{1}{252}{25}{154}{0}{0}{244}{7}{1}{252}{25}{72}{1}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{29}{2}{0}{244}{8}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{35}{0}{0}{244}{8}{1}{252}{25}{31}{0}{0}{244}{7}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{132}{0}{0}{244}{8}{1}{252}{25}{39}{0}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}\n{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{28}{0}{0}{244}{7}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{18}{2}{0}{244}{5}{1}{252}{25}{83}{1}{0}{244}{6}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{24}{2}{0}{244}{6}{1}{252}{25}{31}{0}{0}{244}{7}{1}{252}{25}{0}{0}{0}{244}{5}{1}{252}{25}{32}{0}{0}{244}{7}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{9}{0}{0}{244}{6}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{35}{0}{0}{244}{8}{1}{252}{25}{42}{0}{0}{244}{6}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{9}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}\p{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{106}{1}{0}{244}{6}{1}{252}{25}{42}{0}{0}{244}{6}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{29}{0}{0}{244}{6}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{79}{1}{0}{244}{6}{1}{252}{25}{7}{0}{0}{244}{5}{1}?\p{252}{25}{94}{1}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{29}{2}{0}{244}{8}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{92}{1}{0}{244}{7}{1}{252}{25}{142}{2}{0}{244}{6}{1}{252}{25}{24}{2}{0}{244}{6}{1}{252}{25}{31}{0}{0}{244}{7}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{29}{0}{0}{244}{6}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{77}{1}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{4}{2}{0}{244}{7}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{111}{1}{0}{244}{10}{1}{252}{25}{47}{2}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}\n{252}{25}{10}{0}{0}{244}{7}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{69}{1}{0}{244}{8}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{77}{0}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{123}{0}{0}{244}{7}{1}{252}{25}{104}{0}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{36}{2}{0}{244}{9}{1}{252}{25}{8}{0}{0}{244}{6}{1}!$"

EverGrandeCity_GlaciasRoom_Text_Defeat:
	.string "You and your POKéMON…\n"
	.string "How hot your spirits burn!\p"
	.string "The all-consuming heat overwhelms.\p"
	.string "It's no surprise that my icy skills\n"
	.string "failed to harm you.$"

EverGrandeCity_GlaciasRoom_Text_PostBattleSpeech:
	.string "Advance to the next room.\p"
	.string "And there, confirm the truly fearsome\n"
	.string "side of the POKéMON LEAGUE.$"

