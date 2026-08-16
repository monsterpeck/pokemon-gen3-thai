MtChimney_MapScripts::
	map_script MAP_SCRIPT_ON_RESUME, MtChimney_OnResume
	map_script MAP_SCRIPT_ON_TRANSITION, MtChimney_OnTransition
	.byte 0

MtChimney_OnTransition:
	setvar VAR_JAGGED_PASS_ASH_WEATHER, 1
	end

MtChimney_OnResume:
	setstepcallback STEP_CB_ASH
	end

MtChimney_EventScript_Archie::
	lock
	faceplayer
	call_if_unset FLAG_EVIL_LEADER_PLEASE_STOP, MtChimney_EventScript_ArchieGoStopTeamMagma
	call_if_set FLAG_EVIL_LEADER_PLEASE_STOP, MtChimney_EventScript_ArchieBusyFighting
	closemessage
	applymovement LOCALID_MT_CHIMNEY_ARCHIE, Common_Movement_FaceOriginalDirection
	waitmovement 0
	setflag FLAG_EVIL_LEADER_PLEASE_STOP
	release
	end

MtChimney_EventScript_ArchieGoStopTeamMagma::
	msgbox MtChimney_Text_ArchieGoStopTeamMagma, MSGBOX_DEFAULT
	return

MtChimney_EventScript_ArchieBusyFighting::
	msgbox MtChimney_Text_ArchieIHaveMyHandsFull, MSGBOX_DEFAULT
	return

MtChimney_EventScript_Maxie::
	lockall
	playbgm MUS_ENCOUNTER_MAGMA, FALSE
	msgbox MtChimney_Text_MeteoriteWillActivateVolcano, MSGBOX_DEFAULT
	applymovement LOCALID_MT_CHIMNEY_MAXIE, Common_Movement_FacePlayer
	waitmovement 0
	playse SE_PIN
	applymovement LOCALID_MT_CHIMNEY_MAXIE, Common_Movement_ExclamationMark
	waitmovement 0
	applymovement LOCALID_MT_CHIMNEY_MAXIE, Common_Movement_Delay48
	waitmovement 0
	msgbox MtChimney_Text_MaxieIntro, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_MAXIE_MT_CHIMNEY, MtChimney_Text_MaxieDefeat
	msgbox MtChimney_Text_MaxieYouHaventSeenLastOfMagma, MSGBOX_DEFAULT
	closemessage
	delay 30
	fadescreen FADE_TO_BLACK
	removeobject LOCALID_MT_CHIMNEY_MAXIE
	removeobject LOCALID_MT_CHIMNEY_MAGMA_GRUNT_1
	removeobject LOCALID_MT_CHIMNEY_TABITHA
	removeobject LOCALID_MT_CHIMNEY_MAGMA_GRUNT_2
	setflag FLAG_HIDE_MT_CHIMNEY_TEAM_MAGMA
	fadescreen FADE_FROM_BLACK
	setobjectxyperm LOCALID_MT_CHIMNEY_ARCHIE, 10, 12
	addobject LOCALID_MT_CHIMNEY_ARCHIE
	call_if_eq VAR_FACING, DIR_EAST, MtChimney_EventScript_ArchieApproachPlayerEast
	call_if_eq VAR_FACING, DIR_NORTH, MtChimney_EventScript_ArchieApproachPlayerNorth
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterLeft
	waitmovement 0
	msgbox MtChimney_Text_ArchieThankYou, MSGBOX_DEFAULT
	closemessage
	call_if_eq VAR_FACING, DIR_EAST, MtChimney_EventScript_ArchieExitEast
	call_if_eq VAR_FACING, DIR_NORTH, MtChimney_EventScript_ArchieExitNorth
	removeobject LOCALID_MT_CHIMNEY_ARCHIE
	setflag FLAG_HIDE_MT_CHIMNEY_TEAM_AQUA
	setflag FLAG_DEFEATED_EVIL_TEAM_MT_CHIMNEY
	clearflag FLAG_HIDE_FALLARBOR_HOUSE_PROF_COZMO
	setflag FLAG_HIDE_METEOR_FALLS_1F_1R_COZMO
	clearflag FLAG_HIDE_MT_CHIMNEY_LAVA_COOKIE_LADY
	releaseall
	end

MtChimney_EventScript_ArchieApproachPlayerEast::
	applymovement LOCALID_MT_CHIMNEY_ARCHIE, MtChimney_Movement_ArchieApproachPlayerEast
	waitmovement 0
	return

MtChimney_EventScript_ArchieApproachPlayerNorth::
	applymovement LOCALID_MT_CHIMNEY_ARCHIE, MtChimney_Movement_ArchieApproachPlayerNorth
	waitmovement 0
	return

MtChimney_EventScript_ArchieExitEast::
	applymovement LOCALID_MT_CHIMNEY_ARCHIE, MtChimney_Movement_ArchieExitEast
	waitmovement 0
	return

MtChimney_EventScript_ArchieExitNorth::
	applymovement LOCALID_MT_CHIMNEY_ARCHIE, MtChimney_Movement_ArchieExitNorth
	waitmovement 0
	return

MtChimney_EventScript_LavaCookieLady::
	lock
	faceplayer
	showmoneybox 0, 0
	msgbox MtChimney_Text_LavaCookiesJust200, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, MtChimney_EventScript_DeclineLavaCookie
	checkmoney 200
	goto_if_eq VAR_RESULT, FALSE, MtChimney_EventScript_NotEnoughMoney
	msgbox MtChimney_Text_ThankYouDear, MSGBOX_DEFAULT
	checkitemspace ITEM_LAVA_COOKIE
	call_if_eq VAR_RESULT, TRUE, MtChimney_EventScript_RemoveMoney
	giveitem ITEM_LAVA_COOKIE
	goto_if_eq VAR_RESULT, FALSE, MtChimney_EventScript_BagIsFull
	hidemoneybox
	release
	end

MtChimney_EventScript_BagIsFull::
	msgbox gText_TooBadBagIsFull, MSGBOX_DEFAULT
	hidemoneybox
	release
	end

MtChimney_EventScript_RemoveMoney::
	removemoney 200
	updatemoneybox
	return

MtChimney_EventScript_DeclineLavaCookie::
	msgbox MtChimney_Text_OhFineThen, MSGBOX_DEFAULT
	hidemoneybox
	release
	end

MtChimney_EventScript_NotEnoughMoney::
	msgbox MtChimney_Text_YouveNotGotTheMoney, MSGBOX_DEFAULT
	hidemoneybox
	release
	end

MtChimney_Movement_ArchieApproachPlayerEast:
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_right
	step_end

MtChimney_Movement_ArchieExitEast:
	walk_left
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	step_end

MtChimney_Movement_ArchieApproachPlayerNorth:
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_right
	walk_right
	step_end

MtChimney_Movement_ArchieExitNorth:
	walk_left
	walk_left
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	step_end

MtChimney_Movement_Unused1:
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_left
	walk_left
	walk_down
	walk_down
	walk_down
	walk_down
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_down
	step_end

MtChimney_Movement_Unused2:
	walk_down
	walk_down
	walk_down
	walk_down
	walk_left
	walk_left
	walk_left
	walk_down
	step_end

MtChimney_Movement_Unused3:
	walk_right
	walk_down
	walk_down
	walk_down
	walk_down
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_down
	walk_down
	walk_down
	walk_down
	step_end

MtChimney_Movement_Unused4:
	walk_fast_down
	walk_fast_down
	walk_fast_down
	walk_fast_down
	walk_fast_down
	walk_fast_down
	walk_fast_down
	walk_fast_down
	walk_fast_down
	walk_left
	walk_left
	walk_down
	walk_down
	walk_down
	walk_left
	walk_left
	walk_down
	walk_down
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_down
	step_end

MtChimney_Movement_Unused5:
	delay_16
	delay_16
	delay_16
	walk_down
	walk_down
	walk_down
	walk_left
	walk_left
	walk_left
	walk_down
	step_end

MtChimney_Movement_Unused6:
	delay_16
	walk_left
	walk_down
	walk_down
	walk_down
	walk_down
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_down
	walk_down
	walk_down
	walk_down
	step_end

MtChimney_Movement_Unused7:
	delay_16
	walk_left
	walk_left
	walk_down
	walk_down
	walk_down
	walk_left
	walk_left
	walk_down
	walk_down
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_down
	step_end

MtChimney_Movement_Unused8:
	delay_16
	walk_down
	walk_left
	walk_left
	walk_left
	walk_left
	walk_in_place_faster_down
	step_end

MtChimney_Movement_Unused9:
	walk_down
	walk_down
	walk_down
	walk_down
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_down
	walk_down
	walk_down
	walk_down
	step_end

MtChimney_Movement_Unused10:
	walk_down
	step_end

MtChimney_Movement_Unused11:
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	step_end

MtChimney_Movement_Unused12:
	delay_16
	delay_16
	walk_in_place_faster_left
	delay_16
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	step_end

MtChimney_Movement_Unused13:
	delay_16
	delay_16
	delay_16
	delay_16
	delay_16
	delay_16
	walk_in_place_faster_left
	delay_16
	walk_down
	walk_down
	step_end

MtChimney_Movement_Unused14:
	lock_facing_direction
	walk_fast_left
	unlock_facing_direction
	face_right
	step_end

MtChimney_Movement_Unused15:
	walk_left
	walk_in_place_faster_right
	delay_16
	step_end

MtChimney_EventScript_BusyAquaGrunt1::
	msgbox MtChimney_Text_MagmaOutnumbersUs, MSGBOX_SIGN
	end

MtChimney_EventScript_BusyAquaGrunt2::
	msgbox MtChimney_Text_LessHabitatForWaterPokemon, MSGBOX_SIGN
	end

MtChimney_EventScript_BusyAquaGrunt3::
	msgbox MtChimney_Text_MagmasNameSimilar, MSGBOX_SIGN
	end

MtChimney_EventScript_Tabitha::
	trainerbattle_single TRAINER_TABITHA_MT_CHIMNEY, MtChimney_Text_TabithaIntro, MtChimney_Text_TabithaDefeat
	msgbox MtChimney_Text_TabithaPostBattle, MSGBOX_AUTOCLOSE
	end

MtChimney_EventScript_Grunt2::
	trainerbattle_single TRAINER_GRUNT_MT_CHIMNEY_2, MtChimney_Text_Grunt2Intro, MtChimney_Text_Grunt2Defeat
	msgbox MtChimney_Text_Grunt2PostBattle, MSGBOX_AUTOCLOSE
	end

MtChimney_EventScript_BusyMagmaGrunt1::
	msgbox MtChimney_Text_TeamAquaAlwaysMessingWithPlans, MSGBOX_SIGN
	end

MtChimney_EventScript_BusyMagmaGrunt2::
	msgbox MtChimney_Text_MeteoritesPackAmazingPower, MSGBOX_SIGN
	end

MtChimney_EventScript_BusyMagmaGrunt3::
	msgbox MtChimney_Text_YouBetterNotMessWithUs, MSGBOX_SIGN
	end

MtChimney_EventScript_BusyMagmaGrunt4::
	msgbox MtChimney_Text_AquasNameSimilar, MSGBOX_SIGN
	end

MtChimney_EventScript_BusyMagmaGrunt5::
	msgbox MtChimney_Text_DouseThemInFire, MSGBOX_SIGN
	end

MtChimney_EventScript_BusyMagmaGrunt6::
	msgbox MtChimney_Text_KeepMakingMoreLand, MSGBOX_SIGN
	end

MtChimney_EventScript_MagmaPoochyena::
	msgbox MtChimney_Text_Bufoh, MSGBOX_SIGN
	end

MtChimney_EventScript_AquaPoochyena::
	msgbox MtChimney_Text_Bushaa, MSGBOX_SIGN
	end

MtChimney_EventScript_MeteoriteMachine::
	lockall
	goto_if_unset FLAG_DEFEATED_EVIL_TEAM_MT_CHIMNEY, MtChimney_EventScript_MachineOn
	goto_if_set FLAG_RECEIVED_METEORITE, MtChimney_EventScript_MachineOff
	msgbox MtChimney_Text_RemoveTheMeteorite, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, MtChimney_EventScript_LeaveMeteoriteAlone
	msgbox MtChimney_Text_PlayerRemovedMeteorite, MSGBOX_DEFAULT
	giveitem ITEM_METEORITE
	setflag FLAG_RECEIVED_METEORITE
	releaseall
	end

MtChimney_EventScript_LeaveMeteoriteAlone::
	msgbox MtChimney_Text_PlayerLeftMeteorite, MSGBOX_DEFAULT
	releaseall
	end

MtChimney_EventScript_MachineOff::
	msgbox MtChimney_Text_MachineMakesNoResponse, MSGBOX_DEFAULT
	releaseall
	end

MtChimney_EventScript_MachineOn::
	msgbox MtChimney_Text_MeteoriteFittedOnMachine, MSGBOX_DEFAULT
	releaseall
	end

MtChimney_EventScript_RouteSign::
	msgbox MtChimney_Text_RouteSign, MSGBOX_SIGN
	end

MtChimney_EventScript_Shelby::
	trainerbattle_single TRAINER_SHELBY_1, MtChimney_Text_ShelbyIntro, MtChimney_Text_ShelbyDefeat, MtChimney_EventScript_DefeatedShelby
	specialvar VAR_RESULT, ShouldTryRematchBattle
	goto_if_eq VAR_RESULT, TRUE, MtChimney_EventScript_RematchShelby
	msgbox MtChimney_Text_ShelbyPostBattle, MSGBOX_DEFAULT
	release
	end

MtChimney_EventScript_DefeatedShelby::
	special PlayerFaceTrainerAfterBattle
	waitmovement 0
	msgbox MtChimney_Text_ShelbyRegister, MSGBOX_DEFAULT
	register_matchcall TRAINER_SHELBY_1
	release
	end

MtChimney_EventScript_RematchShelby::
	trainerbattle_rematch TRAINER_SHELBY_1, MtChimney_Text_ShelbyRematchIntro, MtChimney_Text_ShelbyRematchDefeat
	msgbox MtChimney_Text_ShelbyPostRematch, MSGBOX_AUTOCLOSE
	end

MtChimney_EventScript_Melissa::
	trainerbattle_single TRAINER_MELISSA, MtChimney_Text_MelissaIntro, MtChimney_Text_MelissaDefeat
	msgbox MtChimney_Text_MelissaPostBattle, MSGBOX_AUTOCLOSE
	end

MtChimney_EventScript_Sheila::
	trainerbattle_single TRAINER_SHEILA, MtChimney_Text_SheilaIntro, MtChimney_Text_SheilaDefeat
	msgbox MtChimney_Text_SheilaPostBattle, MSGBOX_AUTOCLOSE
	end

MtChimney_EventScript_Shirley::
	trainerbattle_single TRAINER_SHIRLEY, MtChimney_Text_ShirleyIntro, MtChimney_Text_ShirleyDefeat
	msgbox MtChimney_Text_ShirleyPostBattle, MSGBOX_AUTOCLOSE
	end

MtChimney_EventScript_Grunt1::
	trainerbattle_single TRAINER_GRUNT_MT_CHIMNEY_1, MtChimney_Text_Grunt1Intro, MtChimney_Text_Grunt1Defeat
	msgbox MtChimney_Text_Grunt1PostBattle, MSGBOX_AUTOCLOSE
	end

MtChimney_EventScript_Sawyer::
	trainerbattle_single TRAINER_SAWYER_1, MtChimney_Text_SawyerIntro, MtChimney_Text_SawyerDefeat, MtChimney_EventScript_SawyerDefeated
	specialvar VAR_RESULT, ShouldTryRematchBattle
	goto_if_eq VAR_RESULT, TRUE, MtChimney_EventScript_SawyerRematch
	msgbox MtChimney_Text_SawyerPostBattle, MSGBOX_DEFAULT
	release
	end

MtChimney_EventScript_SawyerDefeated::
	special PlayerFaceTrainerAfterBattle
	waitmovement 0
	msgbox MtChimney_Text_SawyerRegister, MSGBOX_DEFAULT
	register_matchcall TRAINER_SAWYER_1
	release
	end

MtChimney_EventScript_SawyerRematch::
	trainerbattle_rematch TRAINER_SAWYER_1, MtChimney_Text_SawyerRematchIntro, MtChimney_Text_SawyerRematchDefeat
	msgbox MtChimney_Text_SawyerPostRematch, MSGBOX_AUTOCLOSE
	end

MtChimney_Text_MeteoriteWillActivateVolcano:
.string "{252}{25}{35}{0}{0}{244}{8}{1}{252}{25}{47}{2}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{154}{0}{0}{244}{7}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{248}{1}{0}{244}{6}{1}{252}{25}{4}{0}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{166}{1}{0}{244}{6}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{31}{0}{0}{244}{7}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{26}{0}{0}{244}{7}{1}…\p{252}{25}{94}{1}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{4}{0}{0}{244}{6}{1}{252}{25}{90}{1}{0}{244}{6}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{10}{0}{0}{244}{7}{1}{252}{25}{46}{1}{0}{244}{6}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{178}{0}{0}{244}{8}{1}{252}{25}{9}{0}{0}{244}{6}{1}{252}{25}{39}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{39}{0}{0}{244}{6}{1}{252}{25}{35}{0}{0}{244}{8}{1}{252}{25}{47}{2}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}\n{252}{25}{35}{0}{0}{244}{8}{1}{252}{25}{47}{2}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{32}{0}{0}{244}{7}{1}{252}{25}{7}{0}{0}{244}{5}{1}{252}{25}{151}{1}{0}{244}{7}{1}{252}{25}{9}{0}{0}{244}{6}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{220}{1}{0}{244}{7}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{9}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{15}{2}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{0}{0}{0}{244}{5}{1}{252}{25}{28}{0}{0}{244}{7}{1}{252}{25}{216}{0}{0}{244}{6}{1}\l{252}{25}{13}{0}{0}{244}{6}{1}{252}{25}{7}{0}{0}{244}{5}{1}{252}{25}{161}{1}{0}{244}{5}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{239}{0}{0}{244}{8}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{35}{2}{0}{244}{7}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{126}{0}{0}{244}{7}{1}…\p{252}{25}{35}{0}{0}{244}{8}{1}{252}{25}{47}{2}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{13}{0}{0}{244}{6}{1}{252}{25}{7}{0}{0}{244}{5}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{101}{0}{0}{244}{8}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{218}{1}{0}{244}{8}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{214}{0}{0}{244}{6}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{41}{0}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{32}{0}{0}{244}{7}{1}\n{252}{25}{4}{0}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{32}{0}{0}{244}{7}{1}{252}{25}{79}{1}{0}{244}{6}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{220}{1}{0}{244}{7}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{9}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{36}{0}{0}{244}{8}{1} {252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{106}{1}{0}{244}{6}{1}{252}{25}{42}{0}{0}{244}{6}{1}{252}{25}{0}{2}{0}{244}{6}{1}…\l{252}{25}{217}{0}{0}{244}{7}{1} {252}{25}{1}{0}{0}{244}{6}{1} {252}{25}{1}{0}{0}{244}{6}{1}…$"

MtChimney_Text_MaxieIntro:
.string "{252}{25}{44}{2}{0}{244}{7}{1}{252}{25}{26}{0}{0}{244}{7}{1}{252}{25}{216}{0}{0}{244}{6}{1}{252}{25}{214}{1}{0}{244}{7}{1}{252}{25}{45}{0}{0}{244}{6}{1}{252}{25}{7}{0}{0}{244}{5}{1}: {252}{25}{25}{1}{0}{244}{7}{1}{252}{25}{38}{0}{0}{244}{7}{1}?\n{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{8}{2}{0}{244}{7}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{4}{0}{0}{244}{6}{1}{252}{25}{10}{0}{0}{244}{7}{1}{252}{25}{40}{0}{0}{244}{5}{1}?\p… … … … … …\n… … … … … …\p{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{92}{1}{0}{244}{7}{1}{252}{25}{77}{0}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{0}{0}{0}{244}{5}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{50}{0}{0}{244}{6}{1}{252}{25}{78}{0}{0}{244}{6}{1}{252}{25}{70}{1}{0}{244}{7}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{202}{0}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{3}{2}{0}{244}{7}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{10}{0}{0}{244}{7}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{46}{0}{0}{244}{7}{1}{252}{25}{224}{0}{0}{244}{8}{1}{252}{25}{12}{0}{0}{244}{4}{1}\n{252}{25}{154}{0}{0}{244}{7}{1}{252}{25}{10}{0}{0}{244}{7}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{39}{0}{0}{244}{6}{1}{252}{25}{187}{1}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{46}{1}{0}{244}{6}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{9}{0}{0}{244}{6}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{126}{0}{0}{244}{7}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{10}{0}{0}{244}{7}{1}{252}{25}{42}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}\l{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{248}{1}{0}{244}{6}{1}{252}{25}{70}{1}{0}{244}{7}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{39}{0}{0}{244}{6}{1} {252}{25}{1}{0}{0}{244}{6}{1}\p{252}{25}{10}{0}{0}{244}{7}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{46}{0}{0}{244}{7}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{39}{0}{0}{244}{6}{1}{252}{25}{202}{0}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{81}{0}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{7}{0}{0}{244}{5}{1}\p{252}{25}{189}{2}{0}{244}{6}{1}! {252}{25}{52}{0}{0}{244}{7}{1}{252}{25}{25}{0}{0}{244}{7}{1}{252}{25}{13}{0}{0}{244}{6}{1}{252}{25}{7}{0}{0}{244}{5}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{25}{2}{0}{244}{6}{1}{252}{25}{25}{0}{0}{244}{7}{1}{252}{25}{9}{0}{0}{244}{6}{1}{252}{25}{42}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{12}{0}{0}{244}{4}{1}\n{252}{25}{35}{0}{0}{244}{8}{1}{252}{25}{42}{0}{0}{244}{6}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{126}{0}{0}{244}{7}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{84}{2}{0}{244}{7}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{213}{0}{0}{244}{6}{1}?\p{252}{25}{42}{2}{0}{244}{8}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{4}{0}{0}{244}{6}{1}{252}{25}{109}{1}{0}{244}{7}{1}{252}{25}{123}{0}{0}{244}{7}{1}\n{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{106}{1}{0}{244}{6}{1}{252}{25}{42}{0}{0}{244}{6}{1} {252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{46}{0}{0}{244}{7}{1}{252}{25}{79}{1}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{108}{0}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{134}{0}{0}{244}{7}{1}{252}{25}{121}{0}{0}{244}{6}{1}{252}{25}{80}{0}{0}{244}{6}{1}{252}{25}{26}{0}{0}{244}{7}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{49}{2}{0}{244}{7}{1}{252}{25}{39}{0}{0}{244}{6}{1}\l{252}{25}{15}{1}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{64}{0}{0}{244}{7}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{42}{1}{0}{244}{8}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{115}{1}{0}{244}{11}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{121}{0}{0}{244}{6}{1}{252}{25}{80}{0}{0}{244}{6}{1}{252}{25}{26}{0}{0}{244}{7}{1}{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{41}{0}{0}{244}{6}{1}{252}{25}{7}{0}{0}{244}{5}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{65}{0}{0}{244}{7}{1}{252}{25}{31}{0}{0}{244}{7}{1}{252}{25}{0}{0}{0}{244}{5}{1}{252}{25}{26}{0}{0}{244}{7}{1}\p{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{35}{0}{0}{244}{8}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{7}{0}{0}{244}{5}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{77}{1}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{88}{2}{0}{244}{8}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{15}{1}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{64}{0}{0}{244}{7}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{196}{0}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{101}{2}{0}{244}{10}{1}{252}{25}{26}{2}{0}{244}{7}{1}{252}{25}{18}{0}{0}{244}{8}{1}{252}{25}{154}{0}{0}{244}{7}{1}{252}{25}{164}{1}{0}{244}{6}{1}{252}{25}{25}{0}{0}{244}{7}{1}!\n{252}{25}{44}{2}{0}{244}{7}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{4}{1}{0}{244}{7}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{46}{0}{0}{244}{7}{1}{252}{25}{79}{1}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{111}{1}{0}{244}{10}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{69}{0}{0}{244}{8}{1}{252}{25}{25}{0}{0}{244}{7}{1}{252}{25}{9}{0}{0}{244}{6}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{151}{1}{0}{244}{7}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{121}{0}{0}{244}{6}{1}{252}{25}{80}{0}{0}{244}{6}{1}{252}{25}{26}{0}{0}{244}{7}{1}!\p{252}{25}{65}{2}{0}{244}{8}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{4}{1}{0}{244}{7}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{46}{0}{0}{244}{7}{1}{252}{25}{149}{1}{0}{244}{7}{1}{252}{25}{33}{0}{0}{244}{6}{1}{252}{25}{41}{0}{0}{244}{6}{1}{252}{25}{154}{0}{0}{244}{7}{1}{252}{25}{126}{0}{0}{244}{7}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{178}{1}{0}{244}{7}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{28}{0}{0}{244}{7}{1}\n{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{42}{1}{0}{244}{8}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{9}{0}{0}{244}{6}{1}{252}{25}{39}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{39}{0}{0}{244}{6}{1}{252}{25}{15}{1}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{72}{1}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{64}{0}{0}{244}{7}{1}{252}{25}{30}{0}{0}{244}{8}{1}\p{252}{25}{143}{2}{0}{244}{8}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{46}{0}{0}{244}{7}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{25}{0}{0}{244}{7}{1}{252}{25}{0}{2}{0}{244}{6}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{42}{1}{0}{244}{8}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{10}{0}{0}{244}{7}{1}{252}{25}{42}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{84}{1}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{42}{0}{0}{244}{6}{1}{252}{25}{46}{0}{0}{244}{7}{1}{252}{25}{96}{1}{0}{244}{8}{1}{252}{25}{6}{0}{0}{244}{4}{1}\n{252}{25}{9}{0}{0}{244}{6}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{152}{1}{0}{244}{8}{1}{252}{25}{44}{0}{0}{244}{8}{1}{252}{25}{17}{2}{0}{244}{6}{1}{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{41}{0}{0}{244}{6}{1}{252}{25}{7}{0}{0}{244}{5}{1}{252}{25}{0}{0}{0}{244}{5}{1}{252}{25}{32}{0}{0}{244}{7}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}!\p{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{41}{0}{0}{244}{6}{1}{252}{25}{7}{0}{0}{244}{5}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{42}{1}{0}{244}{8}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{88}{2}{0}{244}{8}{1}{252}{25}{30}{0}{0}{244}{8}{1} {252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{93}{1}{0}{244}{7}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{4}{0}{0}{244}{6}{1}{252}{25}{90}{1}{0}{244}{6}{1}{252}{25}{35}{0}{0}{244}{8}{1}{252}{25}{47}{2}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}\n{252}{25}{9}{0}{0}{244}{6}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{108}{0}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{154}{0}{0}{244}{7}{1}{252}{25}{46}{0}{0}{244}{7}{1}{252}{25}{47}{2}{0}{244}{6}{1}{252}{25}{31}{0}{0}{244}{7}{1}{252}{25}{4}{0}{0}{244}{6}{1}{252}{25}{46}{0}{0}{244}{7}{1}{252}{25}{41}{0}{0}{244}{6}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{248}{1}{0}{244}{6}{1}{252}{25}{4}{0}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{220}{1}{0}{244}{7}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{9}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{178}{0}{0}{244}{8}{1}…\p{252}{25}{0}{0}{0}{244}{5}{1}{252}{25}{110}{1}{0}{244}{6}{1}! {252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{76}{1}{0}{244}{7}{1}{252}{25}{114}{1}{0}{244}{10}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{8}{2}{0}{244}{7}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{93}{1}{0}{244}{7}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}\n{252}{25}{144}{2}{0}{244}{5}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{202}{0}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{132}{0}{0}{244}{8}{1}{252}{25}{39}{0}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{88}{2}{0}{244}{8}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{155}{0}{0}{244}{8}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{6}{0}{0}{244}{4}{1}\p{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{66}{1}{0}{244}{7}{1}{252}{25}{62}{1}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{27}{0}{0}{244}{6}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{7}{0}{0}{244}{5}{1}!\n{252}{25}{29}{2}{0}{244}{8}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{13}{0}{0}{244}{6}{1}{252}{25}{7}{0}{0}{244}{5}{1}{252}{25}{45}{0}{0}{244}{6}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{4}{0}{0}{244}{6}{1}{252}{25}{109}{1}{0}{244}{7}{1}{252}{25}{144}{2}{0}{244}{5}{1}{252}{25}{202}{0}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{33}{0}{0}{244}{6}{1}{252}{25}{41}{0}{0}{244}{6}{1}{252}{25}{9}{0}{0}{244}{6}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{40}{0}{0}{244}{5}{1}\l{252}{25}{25}{2}{0}{244}{6}{1}{252}{25}{25}{0}{0}{244}{7}{1}{252}{25}{9}{0}{0}{244}{6}{1}{252}{25}{42}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{33}{0}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{52}{2}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{104}{0}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{4}{0}{0}{244}{6}{1}{252}{25}{46}{0}{0}{244}{7}{1}{252}{25}{148}{2}{0}{244}{8}{1}{252}{25}{9}{0}{0}{244}{6}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{6}{0}{0}{244}{4}{1}!$"

MtChimney_Text_MaxieDefeat:
	.string "What?!\p"
	.string "I, MAXIE, was caught off guard?!$"

MtChimney_Text_MaxieYouHaventSeenLastOfMagma:
.string "{252}{25}{44}{2}{0}{244}{7}{1}{252}{25}{26}{0}{0}{244}{7}{1}{252}{25}{216}{0}{0}{244}{6}{1}{252}{25}{214}{1}{0}{244}{7}{1}{252}{25}{45}{0}{0}{244}{6}{1}{252}{25}{7}{0}{0}{244}{5}{1}: {252}{25}{35}{0}{0}{244}{8}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{57}{1}{0}{244}{7}{1}{252}{25}{178}{0}{0}{244}{8}{1}{252}{25}{55}{1}{0}{244}{6}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}\n{252}{25}{10}{0}{0}{244}{7}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{42}{0}{0}{244}{6}{1}{252}{25}{178}{0}{0}{244}{8}{1}{252}{25}{29}{2}{0}{244}{8}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{13}{0}{0}{244}{6}{1}{252}{25}{7}{0}{0}{244}{5}{1}{252}{25}{27}{0}{0}{244}{6}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{39}{0}{0}{244}{6}{1}{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{32}{0}{0}{244}{7}{1}\p{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{66}{1}{0}{244}{7}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{77}{1}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{52}{0}{0}{244}{7}{1}{252}{25}{25}{0}{0}{244}{7}{1}{252}{25}{80}{1}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{155}{0}{0}{244}{8}{1}{252}{25}{13}{0}{0}{244}{6}{1}{252}{25}{7}{0}{0}{244}{5}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{8}{2}{0}{244}{7}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{10}{0}{0}{244}{7}{1}{252}{25}{93}{2}{0}{244}{7}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{164}{1}{0}{244}{6}{1}{252}{25}{25}{0}{0}{244}{7}{1}{252}{25}{95}{1}{0}{244}{7}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{39}{0}{0}{244}{6}{1}\n{252}{25}{154}{0}{0}{244}{7}{1}{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{92}{1}{0}{244}{7}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{13}{0}{0}{244}{6}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{24}{2}{0}{244}{6}{1}{252}{25}{31}{0}{0}{244}{7}{1}{252}{25}{126}{0}{0}{244}{7}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{6}{0}{0}{244}{4}{1}\p{252}{25}{217}{0}{0}{244}{7}{1} {252}{25}{1}{0}{0}{244}{6}{1} {252}{25}{1}{0}{0}{244}{6}{1}…\p{252}{25}{202}{0}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{76}{1}{0}{244}{7}{1}{252}{25}{134}{0}{0}{244}{7}{1}{252}{25}{166}{1}{0}{244}{6}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{31}{0}{0}{244}{7}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{26}{0}{0}{244}{7}{1} {252}{25}{94}{1}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{92}{1}{0}{244}{7}{1}\n{252}{25}{224}{1}{0}{244}{6}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{84}{1}{0}{244}{6}{1}{252}{25}{42}{0}{0}{244}{6}{1}{252}{25}{65}{2}{0}{244}{8}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{6}{0}{0}{244}{4}{1}… {252}{25}{217}{0}{0}{244}{7}{1} {252}{25}{1}{0}{0}{244}{6}{1} {252}{25}{1}{0}{0}{244}{6}{1}…$"

MtChimney_Text_TabithaIntro:
	.string "Hehehe!\p"
	.string "So you've come all the way here!\p"
	.string "But you're too late!\n"
	.string "I've already delivered the METEORITE\l"
	.string "from METEOR FALLS to the BOSS!$"

MtChimney_Text_TabithaDefeat:
	.string "Hehehe…\p"
	.string "Even though I've lost, if our leader\n"
	.string "awakens that thing…$"

MtChimney_Text_TabithaPostBattle:
	.string "BOSS, hurry!\n"
	.string "Give it the METEORITE's energy!\p"
	.string "Hehehe…$"

MtChimney_Text_Grunt2Intro:
	.string "We of TEAM MAGMA are working hard for\n"
	.string "everyone's sake.\p"
	.string "Like, if that thing's power made more\n"
	.string "land, there'd be more places to live.\p"
	.string "Everyone'd be happy!$"

MtChimney_Text_Grunt2Defeat:
	.string "Hunh?\n"
	.string "What do you mean I lost?$"

MtChimney_Text_Grunt2PostBattle:
	.string "Our BOSS says, “It will make everyone\n"
	.string "happy.”\p"
	.string "But why does everyone keep getting\n"
	.string "in our way?$"

MtChimney_Text_Grunt1Intro:
	.string "If there were more land, I'd be able\n"
	.string "to get a big house of my own!\p"
	.string "I'm going to build it on hardened lava!$"

MtChimney_Text_Grunt1Defeat:
	.string "My dream of a big house…$"

MtChimney_Text_Grunt1PostBattle:
	.string "A kid like you, you ought to be\n"
	.string "splashing about in the waves!$"

MtChimney_Text_TeamAquaAlwaysMessingWithPlans:
	.string "That annoying TEAM AQUA…\n"
	.string "They always mess with our plans!$"

MtChimney_Text_MeteoritesPackAmazingPower:
	.string "METEORITES pack amazing power!$"

MtChimney_Text_YouBetterNotMessWithUs:
	.string "You'd better not mess with us!\p"
	.string "We're trying to awaken that thing\n"
	.string "for the benefit of everyone!$"

MtChimney_Text_AquasNameSimilar:
	.string "We're TEAM MAGMA!\p"
	.string "They're TEAM AQUA!\p"
	.string "It totally annoys me that they'd\n"
	.string "use a name like ours!$"

MtChimney_Text_DouseThemInFire:
	.string "Yeah!\n"
	.string "Douse them in fire!$"

MtChimney_Text_KeepMakingMoreLand:
	.string "We're going to keep making more land!$"

MtChimney_Text_Bufoh:
	.string "Bufoh!$"

MtChimney_Text_ArchieGoStopTeamMagma:
.string "{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{0}{0}{0}{244}{5}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{50}{0}{0}{244}{6}{1}{252}{25}{78}{0}{0}{244}{6}{1}: {252}{25}{183}{2}{0}{244}{7}{1}{252}{25}{38}{0}{0}{244}{7}{1} {PLAYER}!\n{252}{25}{204}{0}{0}{244}{8}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{106}{1}{0}{244}{6}{1}{252}{25}{42}{0}{0}{244}{6}{1}{252}{25}{80}{1}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{93}{1}{0}{244}{7}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{0}{0}{0}{244}{5}{1}{252}{25}{33}{0}{0}{244}{6}{1}{252}{25}{79}{1}{0}{244}{6}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{6}{0}{0}{244}{4}{1}!\p{252}{25}{209}{1}{0}{244}{7}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{80}{1}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{35}{0}{0}{244}{8}{1}{252}{25}{42}{0}{0}{244}{6}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{10}{0}{0}{244}{7}{1}{252}{25}{75}{2}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{47}{2}{0}{244}{6}{1}{252}{25}{28}{0}{0}{244}{7}{1}{252}{25}{68}{0}{0}{244}{6}{1}\n{252}{25}{126}{0}{0}{244}{7}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{111}{1}{0}{244}{10}{1}{252}{25}{47}{2}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{117}{1}{0}{244}{11}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{7}{0}{0}{244}{5}{1}{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{40}{0}{0}{244}{5}{1}!\p{252}{25}{35}{0}{0}{244}{8}{1}{252}{25}{42}{0}{0}{244}{6}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{44}{2}{0}{244}{7}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{111}{1}{0}{244}{10}{1}{252}{25}{47}{2}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{81}{1}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{35}{0}{0}{244}{8}{1}{252}{25}{47}{2}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{9}{0}{0}{244}{6}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}\n{252}{25}{166}{1}{0}{244}{6}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{31}{0}{0}{244}{7}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{26}{0}{0}{244}{7}{1}{252}{25}{154}{0}{0}{244}{7}{1}{252}{25}{9}{0}{0}{244}{6}{1}{252}{25}{0}{0}{0}{244}{5}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{39}{0}{0}{244}{6}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{85}{1}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{252}{1}{0}{244}{6}{1}{252}{25}{220}{1}{0}{244}{7}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{9}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{36}{0}{0}{244}{8}{1}!\p{252}{25}{117}{1}{0}{244}{11}{1}{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{31}{0}{0}{244}{7}{1}{252}{25}{31}{0}{0}{244}{7}{1}{252}{25}{88}{2}{0}{244}{8}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{220}{1}{0}{244}{7}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{9}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{36}{0}{0}{244}{8}{1}\n{252}{25}{13}{0}{0}{244}{6}{1}{252}{25}{7}{0}{0}{244}{5}{1}{252}{25}{32}{0}{0}{244}{7}{1}{252}{25}{7}{0}{0}{244}{5}{1}{252}{25}{151}{1}{0}{244}{7}{1}{252}{25}{239}{0}{0}{244}{8}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{6}{0}{0}{244}{4}{1}!$"

MtChimney_Text_ArchieIHaveMyHandsFull:
.string "{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{0}{0}{0}{244}{5}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{50}{0}{0}{244}{6}{1}{252}{25}{78}{0}{0}{244}{6}{1}: {252}{25}{183}{2}{0}{244}{7}{1}{252}{25}{38}{0}{0}{244}{7}{1}…\p{252}{25}{29}{2}{0}{244}{8}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{39}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{46}{0}{0}{244}{7}{1}{252}{25}{160}{1}{0}{244}{6}{1}{252}{25}{25}{0}{0}{244}{7}{1}{252}{25}{44}{2}{0}{244}{7}{1}{252}{25}{26}{0}{0}{244}{7}{1}{252}{25}{216}{0}{0}{244}{6}{1}{252}{25}{214}{1}{0}{244}{7}{1}{252}{25}{45}{0}{0}{244}{6}{1}{252}{25}{7}{0}{0}{244}{5}{1}\n{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{66}{1}{0}{244}{7}{1}{252}{25}{117}{1}{0}{244}{11}{1}{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{76}{1}{0}{244}{7}{1}{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{92}{1}{0}{244}{7}{1}!\p{252}{25}{4}{0}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{44}{1}{0}{244}{7}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{29}{2}{0}{244}{8}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{93}{1}{0}{244}{7}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{46}{2}{0}{244}{5}{1}{252}{25}{31}{0}{0}{244}{7}{1}{252}{25}{19}{1}{0}{244}{7}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{49}{2}{0}{244}{7}{1}{252}{25}{26}{0}{0}{244}{7}{1}{252}{25}{223}{1}{0}{244}{5}{1}\n{252}{25}{45}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{10}{0}{0}{244}{7}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{35}{0}{0}{244}{8}{1}{252}{25}{105}{1}{0}{244}{5}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{24}{2}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{31}{0}{0}{244}{7}{1}{252}{25}{31}{0}{0}{244}{7}{1}{252}{25}{178}{0}{0}{244}{8}{1}!$"

MtChimney_Text_ArchieThankYou:
.string "{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{0}{0}{0}{244}{5}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{50}{0}{0}{244}{6}{1}{252}{25}{78}{0}{0}{244}{6}{1}: {PLAYER}!\n{252}{25}{9}{0}{0}{244}{6}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{31}{0}{0}{244}{7}{1}{252}{25}{4}{0}{0}{244}{6}{1}{252}{25}{13}{0}{0}{244}{6}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{8}{0}{0}{244}{6}{1}!\p{252}{25}{92}{1}{0}{244}{7}{1}{252}{25}{42}{0}{0}{244}{6}{1}{252}{25}{39}{0}{0}{244}{6}{1}{252}{25}{10}{0}{0}{244}{7}{1}{252}{25}{42}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{62}{1}{0}{244}{6}{1}{252}{25}{42}{0}{0}{244}{6}{1}{252}{25}{39}{0}{0}{244}{6}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{46}{0}{0}{244}{7}{1}{252}{25}{22}{1}{0}{244}{6}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{9}{0}{0}{244}{6}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{8}{0}{0}{244}{6}{1} {252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{196}{0}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{46}{0}{0}{244}{7}{1}{252}{25}{160}{1}{0}{244}{6}{1}{252}{25}{25}{0}{0}{244}{7}{1}\n{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{33}{0}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{117}{1}{0}{244}{11}{1}{252}{25}{41}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{39}{0}{0}{244}{6}{1}{252}{25}{106}{1}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{9}{0}{0}{244}{6}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{126}{0}{0}{244}{7}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{92}{1}{0}{244}{7}{1}!\p{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{66}{1}{0}{244}{7}{1}… {252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{8}{0}{0}{244}{6}{1}…\n{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{248}{1}{0}{244}{6}{1}{252}{25}{73}{1}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{39}{0}{0}{244}{6}{1}{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{46}{0}{0}{244}{7}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{24}{2}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{69}{1}{0}{244}{8}{1}?\p{252}{25}{62}{1}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{27}{0}{0}{244}{6}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{7}{0}{0}{244}{5}{1} {252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{76}{1}{0}{244}{7}{1}{252}{25}{101}{2}{0}{244}{10}{1}{252}{25}{26}{2}{0}{244}{7}{1}{252}{25}{18}{0}{0}{244}{8}{1}{252}{25}{46}{0}{0}{244}{7}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{8}{0}{0}{244}{6}{1}\p{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{13}{0}{0}{244}{6}{1}{252}{25}{7}{0}{0}{244}{5}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{100}{1}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{7}{0}{0}{244}{5}{1}{252}{25}{48}{2}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{41}{0}{0}{244}{6}{1}{252}{25}{7}{0}{0}{244}{5}{1}{252}{25}{26}{0}{0}{244}{7}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{79}{1}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}\n{252}{25}{126}{0}{0}{244}{7}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{66}{1}{0}{244}{7}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{32}{0}{0}{244}{7}{1}\p{PLAYER} {252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{106}{1}{0}{244}{6}{1}{252}{25}{42}{0}{0}{244}{6}{1}{252}{25}{35}{0}{0}{244}{8}{1}{252}{25}{31}{0}{0}{244}{7}{1}{252}{25}{24}{2}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{4}{0}{0}{244}{6}{1}{252}{25}{46}{0}{0}{244}{7}{1}{252}{25}{76}{1}{0}{244}{7}{1}!$"

MtChimney_Text_MagmaOutnumbersUs:
	.string "Darn… TEAM MAGMA outnumbers us!\n"
	.string "We can't keep up with them!$"

MtChimney_Text_LessHabitatForWaterPokemon:
	.string "If they expand the land, there'll be\n"
	.string "less habitats for WATER POKéMON!$"

MtChimney_Text_MagmasNameSimilar:
	.string "We're TEAM AQUA!\p"
	.string "They're TEAM MAGMA!\p"
	.string "It burns me up that they'd use such\n"
	.string "a confusing name!$"

MtChimney_Text_Bushaa:
	.string "Bushaa!$"

MtChimney_Text_LavaCookiesJust200:
	.string "LAVA COOKIES are MT. CHIMNEY's local\n"
	.string "specialty.\p"
	.string "Try one. It's just ¥200.$"

MtChimney_Text_ThankYouDear:
	.string "Thank you, dear!$"

MtChimney_Text_YouveNotGotTheMoney:
	.string "Oh, dear. You can't buy a thing if\n"
	.string "you've not got the money.$"

MtChimney_Text_OhFineThen:
	.string "Oh, fine then.$"

MtChimney_Text_MeteoriteFittedOnMachine:
	.string "A METEORITE is fitted on a mysterious\n"
	.string "machine…\p"
	.string "The machine seems to be storing\n"
	.string "energy in the METEORITE.$"

MtChimney_Text_RemoveTheMeteorite:
	.string "A METEORITE is fitted on a mysterious\n"
	.string "machine…\p"
	.string "Do you want to remove the METEORITE?$"

MtChimney_Text_PlayerRemovedMeteorite:
.string "{PLAYER} {252}{25}{118}{1}{0}{244}{11}{1}{252}{25}{166}{1}{0}{244}{6}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{31}{0}{0}{244}{7}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{26}{0}{0}{244}{7}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{13}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{8}{0}{0}{244}{6}{1}\n{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{10}{0}{0}{244}{7}{1}{252}{25}{46}{1}{0}{244}{6}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{28}{2}{0}{244}{6}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{214}{0}{0}{244}{6}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{47}{2}{0}{244}{6}{1}{252}{25}{31}{0}{0}{244}{7}{1}{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{106}{1}{0}{244}{6}{1}{252}{25}{42}{0}{0}{244}{6}{1}$"

MtChimney_Text_PlayerLeftMeteorite:
	.string "{PLAYER} left the METEORITE where\n"
	.string "it was.$"

MtChimney_Text_MachineMakesNoResponse:
	.string "This mysterious machine…\n"
	.string "It makes no response whatsoever.$"

MtChimney_Text_RouteSign:
	.string "{DOWN_ARROW} JAGGED PATH\n"
	.string "LAVARIDGE TOWN AHEAD$"

MtChimney_Text_ShelbyIntro:
	.string "I've been to the hot springs and\n"
	.string "refreshed my tired bones.\l"
	.string "Right now I'm feeling strong!$"

MtChimney_Text_ShelbyDefeat:
	.string "Oh, my goodness.\n"
	.string "Now, aren't you something!$"

MtChimney_Text_ShelbyPostBattle:
	.string "Well, well, I've lost. I can't call\n"
	.string "myself an EXPERT now, can I?$"

MtChimney_Text_ShelbyRegister:
	.string "Thank you, child. It was fun, as if\n"
	.string "I were battling my own grandchild.\p"
	.string "Please, come see me again for\n"
	.string "a rematch.$"

MtChimney_Text_ShelbyRematchIntro:
	.string "If you can mesh your heart with those\n"
	.string "of your POKéMON, why, you should be\l"
	.string "able to achieve great things.$"

MtChimney_Text_ShelbyRematchDefeat:
	.string "Oh, my goodness.\n"
	.string "Now, aren't you something!$"

MtChimney_Text_ShelbyPostRematch:
	.string "Perhaps your heart has become one\n"
	.string "with the hearts of your POKéMON.$"

MtChimney_Text_MelissaIntro:
	.string "I've got the fire in me, baby.\n"
	.string "I can't stand it! I have to battle!$"

MtChimney_Text_MelissaDefeat:
	.string "Ooh, that was a scorching-hot match!$"

MtChimney_Text_MelissaPostBattle:
	.string "The heat of MT. CHIMNEY warms\n"
	.string "me up, baby!$"

MtChimney_Text_SheilaIntro:
	.string "I've finally made it to MT. CHIMNEY.\n"
	.string "I want to make my POKéMON battle!$"

MtChimney_Text_SheilaDefeat:
	.string "The way you battle…\n"
	.string "It's like a MT. CHIMNEY eruption!$"

MtChimney_Text_SheilaPostBattle:
	.string "Like I said, I've finally made it to\n"
	.string "MT. CHIMNEY. It would be a shame if\l"
	.string "I only do a little sightseeing…\p"
	.string "I want to get in some battles and buy\n"
	.string "COOKIES as souvenirs.$"

MtChimney_Text_ShirleyIntro:
	.string "Since I bathed in the hot springs,\n"
	.string "I've been feeling great!\l"
	.string "I'm sure I'm going to win!$"

MtChimney_Text_ShirleyDefeat:
	.string "Yowch!\n"
	.string "I'm getting a chill out of the water.$"

MtChimney_Text_ShirleyPostBattle:
	.string "I'll have to take another dip in the\n"
	.string "hot springs. Want to join me?\p"
	.string "Just joking!$"

MtChimney_Text_SawyerIntro:
	.string "This is one fine mountain! Plenty of\n"
	.string "hot people around for company!$"

MtChimney_Text_SawyerDefeat:
	.string "Oh, you're a real firebrand, too!$"

MtChimney_Text_SawyerPostBattle:
	.string "I think I need a dip in LAVARIDGE\n"
	.string "HOT SPRING with the locals!$"

MtChimney_Text_SawyerRegister:
	.string "I like little fireballs like you.\n"
	.string "Let me register you in my POKéNAV.$"

MtChimney_Text_SawyerRematchIntro:
	.string "I'm happily surrounded by hot people\n"
	.string "around these parts. I won't lose!$"

MtChimney_Text_SawyerRematchDefeat:
	.string "Gosh, you're still the same\n"
	.string "firebrand as before!$"

MtChimney_Text_SawyerPostRematch:
	.string "Actually, it really is hot here.\n"
	.string "I'm overdressed for these parts.$"

