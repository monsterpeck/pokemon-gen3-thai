Route128_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Route128_OnTransition
	map_script MAP_SCRIPT_ON_FRAME_TABLE, Route128_OnFrame
	.byte 0

Route128_OnTransition:
	call_if_set FLAG_SYS_WEATHER_CTRL, Common_EventScript_SetAbnormalWeather
	end

Route128_OnFrame:
	map_script_2 VAR_ROUTE128_STATE, 1, Route128_EventScript_KyogreAwakenedScene
	.2byte 0

Route128_EventScript_KyogreAwakenedScene::
	lockall
	delay 20
	applymovement LOCALID_ROUTE128_ARCHIE, Route128_Movement_ArchieLookAround
	waitmovement 0
	msgbox Route128_Text_ArchieWhatHappened, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_ROUTE128_ARCHIE, Route128_Movement_ArchieBackUp
	waitmovement 0
	msgbox Route128_Text_ArchieIOnlyWanted, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_ROUTE128_MAXIE, Route128_Movement_MaxieApproachArchie
	waitmovement 0
	applymovement LOCALID_ROUTE128_ARCHIE, Common_Movement_WalkInPlaceFasterUp
	waitmovement 0
	msgbox Route128_Text_MaxieDoYouUnderstandNow, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_ROUTE128_MAXIE, Route128_Movement_MaxieApproachPlayer
	waitmovement 0
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterUp
	waitmovement 0
	msgbox Route128_Text_MaxieResposibilityFallsToArchieAndMe, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_ROUTE128_ARCHIE, Route128_Movement_ArchieRunLeft
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterLeft
	applymovement LOCALID_ROUTE128_MAXIE, Route128_Movement_MaxieWalkLeft
	waitmovement 0
	msgbox Route128_Text_MaxieThisDefiesBelief, MSGBOX_DEFAULT
	closemessage
	delay 40
	applymovement LOCALID_ROUTE128_MAXIE, Route128_Movement_MaxieExit
	applymovement LOCALID_ROUTE128_ARCHIE, Route128_Movement_ArchieExit
	waitmovement 0
	removeobject LOCALID_ROUTE128_MAXIE
	removeobject LOCALID_ROUTE128_ARCHIE
	delay 100
	setfieldeffectargument 0, 1
	dofieldeffect FLDEFF_NPCFLY_OUT
	waitfieldeffect FLDEFF_NPCFLY_OUT
	addobject LOCALID_ROUTE128_STEVEN
	applymovement LOCALID_ROUTE128_STEVEN, Route128_Movement_StevenApproachPlayer
	waitmovement 0
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterRight
	waitmovement 0
	msgbox Route128_Text_StevenWhatIsHappening, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_ROUTE128_STEVEN, Route128_Movement_StevenWalkUp
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterUp
	waitmovement 0
	msgbox Route128_Text_StevenWholeWorldWillDrown, MSGBOX_DEFAULT
	applymovement LOCALID_ROUTE128_STEVEN, Common_Movement_WalkInPlaceFasterDown
	waitmovement 0
	msgbox Route128_Text_StevenImGoingToSootopolis, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_ROUTE128_STEVEN, Common_Movement_WalkInPlaceFasterDown
	waitmovement 0
	delay 50
	setfieldeffectargument 0, 1
	dofieldeffect FLDEFF_NPCFLY_OUT
	delay 15
	removeobject LOCALID_ROUTE128_STEVEN
	waitfieldeffect FLDEFF_NPCFLY_OUT
	clearflag FLAG_HIDE_MAP_NAME_POPUP
	setvar VAR_ROUTE128_STATE, 2
	releaseall
	end

Route128_Movement_Unused1:
	walk_fast_left
	step_end

Route128_Movement_Unused2:
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	step_end

Route128_Movement_StevenWalkUp:
	walk_up
	step_end

Route128_Movement_StevenApproachPlayer:
	walk_fast_left
	step_end

Route128_Movement_ArchieLookAround:
	walk_fast_down
	walk_in_place_faster_left
	delay_16
	walk_in_place_faster_right
	delay_16
	delay_16
	walk_in_place_faster_down
	step_end

Route128_Movement_ArchieBackUp:
	lock_facing_direction
	walk_slow_up
	delay_16
	unlock_facing_direction
	step_end

Route128_Movement_ArchieRunLeft:
	walk_fast_left
	walk_fast_left
	walk_fast_left
	walk_in_place_faster_right
	step_end

Route128_Movement_ArchieExit:
	delay_16
	delay_16
	walk_fast_up
	walk_fast_left
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_up
	step_end

Route128_Movement_MaxieWalkLeft:
	walk_left
	walk_left
	delay_8
	delay_4
	step_end

Route128_Movement_MaxieApproachArchie:
	walk_left
	walk_in_place_faster_down
	step_end

Route128_Movement_MaxieExit:
	walk_fast_left
	walk_fast_left
	walk_fast_left
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_up
	step_end

Route128_Movement_MaxieApproachPlayer:
	walk_right
	walk_in_place_faster_down
	step_end

Route128_EventScript_Isaiah::
	trainerbattle_single TRAINER_ISAIAH_1, Route128_Text_IsaiahIntro, Route128_Text_IsaiahDefeat, Route128_EventScript_RegisterIsaiah
	specialvar VAR_RESULT, ShouldTryRematchBattle
	goto_if_eq VAR_RESULT, TRUE, Route128_EventScript_RematchIsaiah
	msgbox Route128_Text_IsaiahPostBattle, MSGBOX_DEFAULT
	release
	end

Route128_EventScript_RegisterIsaiah::
	special PlayerFaceTrainerAfterBattle
	waitmovement 0
	msgbox Route128_Text_IsaiahRegister, MSGBOX_DEFAULT
	register_matchcall TRAINER_ISAIAH_1
	release
	end

Route128_EventScript_RematchIsaiah::
	trainerbattle_rematch TRAINER_ISAIAH_1, Route128_Text_IsaiahRematchIntro, Route128_Text_IsaiahRematchDefeat
	msgbox Route128_Text_IsaiahPostRematch, MSGBOX_AUTOCLOSE
	end

Route128_EventScript_Katelyn::
	trainerbattle_single TRAINER_KATELYN_1, Route128_Text_KatelynIntro, Route128_Text_KatelynDefeat, Route128_EventScript_RegisterKatelyn
	specialvar VAR_RESULT, ShouldTryRematchBattle
	goto_if_eq VAR_RESULT, TRUE, Route128_EventScript_RematchKatelyn
	msgbox Route128_Text_KatelynPostBattle, MSGBOX_DEFAULT
	release
	end

Route128_EventScript_RegisterKatelyn::
	special PlayerFaceTrainerAfterBattle
	waitmovement 0
	msgbox Route128_Text_KatelynRegister, MSGBOX_DEFAULT
	register_matchcall TRAINER_KATELYN_1
	release
	end

Route128_EventScript_RematchKatelyn::
	trainerbattle_rematch TRAINER_KATELYN_1, Route128_Text_KatelynRematchIntro, Route128_Text_KatelynRematchDefeat
	msgbox Route128_Text_KatelynPostRematch, MSGBOX_AUTOCLOSE
	end

Route128_EventScript_Alexa::
	trainerbattle_single TRAINER_ALEXA, Route128_Text_AlexaIntro, Route128_Text_AlexaDefeat
	msgbox Route128_Text_AlexaPostBattle, MSGBOX_AUTOCLOSE
	end

Route128_EventScript_Ruben::
	trainerbattle_single TRAINER_RUBEN, Route128_Text_RubenIntro, Route128_Text_RubenDefeat
	msgbox Route128_Text_RubenPostBattle, MSGBOX_AUTOCLOSE
	end

Route128_EventScript_Wayne::
	trainerbattle_single TRAINER_WAYNE, Route128_Text_WayneIntro, Route128_Text_WayneDefeat
	msgbox Route128_Text_WaynePostBattle, MSGBOX_AUTOCLOSE
	end

Route128_EventScript_Harrison::
	trainerbattle_single TRAINER_HARRISON, Route128_Text_HarrisonIntro, Route128_Text_HarrisonDefeat
	msgbox Route128_Text_HarrisonPostBattle, MSGBOX_AUTOCLOSE
	end

Route128_EventScript_Carlee::
	trainerbattle_single TRAINER_CARLEE, Route128_Text_CarleeIntro, Route128_Text_CarleeDefeat
	msgbox Route128_Text_CarleePostBattle, MSGBOX_AUTOCLOSE
	end

Route128_Text_ArchieWhatHappened:
	.string "ARCHIE: What happened…\n"
	.string "What is this wretched scene…\p"
	.string "Did I…make a horrible mistake?$"

Route128_Text_ArchieIOnlyWanted:
	.string "I…\n"
	.string "I only wanted…$"

Route128_Text_MaxieDoYouUnderstandNow:
	.string "MAXIE: Do you understand now,\n"
	.string "ARCHIE?\p"
	.string "Do you finally see how disastrous\n"
	.string "your dream turned out to be?\p"
	.string "We have to hurry! We have to do\n"
	.string "something before the situation goes\l"
	.string "completely out of control!$"

Route128_Text_MaxieResposibilityFallsToArchieAndMe:
	.string "MAXIE: {PLAYER}, don't say anything.\p"
	.string "I know that I have no right to be\n"
	.string "critical of ARCHIE…\p"
	.string "But the way things are now, I doubt\n"
	.string "that we humans will be capable of\l"
	.string "doing anything about it.\p"
	.string "But neither can we stand by and\n"
	.string "just watch helplessly.\p"
	.string "The responsibility for putting an end\n"
	.string "to this falls to ARCHIE and me…$"

Route128_Text_MaxieThisDefiesBelief:
.string "{252}{25}{44}{2}{0}{244}{7}{1}{252}{25}{26}{0}{0}{244}{7}{1}{252}{25}{216}{0}{0}{244}{6}{1}{252}{25}{214}{1}{0}{244}{7}{1}{252}{25}{45}{0}{0}{244}{6}{1}{252}{25}{7}{0}{0}{244}{5}{1}: {252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{76}{1}{0}{244}{7}{1}{252}{25}{69}{1}{0}{244}{8}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{31}{1}{0}{244}{6}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{41}{0}{0}{244}{6}{1}{252}{25}{39}{0}{0}{244}{6}{1}…\p{252}{25}{0}{0}{0}{244}{5}{1}{252}{25}{32}{0}{0}{244}{7}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{160}{1}{0}{244}{6}{1}{252}{25}{10}{0}{0}{244}{7}{1}{252}{25}{31}{0}{0}{244}{7}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{35}{0}{0}{244}{8}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{41}{0}{0}{244}{6}{1}{252}{25}{35}{0}{0}{244}{8}{1}{252}{25}{42}{0}{0}{244}{6}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{88}{2}{0}{244}{8}{1}{252}{25}{30}{0}{0}{244}{8}{1}…\p{252}{25}{35}{0}{0}{244}{8}{1}{252}{25}{47}{2}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{9}{0}{0}{244}{6}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{44}{2}{0}{244}{7}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{46}{0}{0}{244}{7}{1}{252}{25}{22}{1}{0}{244}{6}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{31}{1}{0}{244}{6}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{13}{0}{0}{244}{6}{1}{252}{25}{78}{0}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1} {252}{25}{1}{0}{0}{244}{6}{1}\n{252}{25}{117}{1}{0}{244}{11}{1}{252}{25}{4}{0}{0}{244}{6}{1}{252}{25}{109}{1}{0}{244}{7}{1}{252}{25}{45}{0}{0}{244}{6}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{148}{1}{0}{244}{7}{1}{252}{25}{41}{0}{0}{244}{6}{1}{252}{25}{29}{0}{0}{244}{6}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{15}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{65}{0}{0}{244}{7}{1}{252}{25}{41}{2}{0}{244}{8}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{28}{0}{0}{244}{7}{1}{252}{25}{41}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{39}{0}{0}{244}{6}{1}…$"

Route128_Text_StevenWhatIsHappening:
	.string "STEVEN: {PLAYER}{KUN}!\n"
	.string "What is happening?$"

Route128_Text_StevenWholeWorldWillDrown:
.string "{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{77}{1}{0}{244}{6}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{8}{0}{0}{244}{6}{1}…\p{252}{25}{46}{0}{0}{244}{7}{1}{252}{25}{47}{2}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{10}{0}{0}{244}{7}{1}{252}{25}{47}{1}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{10}{0}{0}{244}{7}{1}{252}{25}{42}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{105}{1}{0}{244}{5}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{33}{0}{0}{244}{6}{1}{252}{25}{25}{0}{0}{244}{7}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{33}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}\n{252}{25}{113}{2}{0}{244}{7}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{164}{1}{0}{244}{6}{1}{252}{25}{25}{0}{0}{244}{7}{1}{252}{25}{34}{0}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{46}{0}{0}{244}{7}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{43}{0}{0}{244}{7}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{41}{0}{0}{244}{6}{1}{252}{25}{0}{2}{0}{244}{6}{1}{252}{25}{26}{0}{0}{244}{7}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{41}{0}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{28}{0}{0}{244}{7}{1}{252}{25}{30}{0}{0}{244}{8}{1}\p{252}{25}{94}{1}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{76}{1}{0}{244}{7}{1}{252}{25}{46}{0}{0}{244}{7}{1}{252}{25}{160}{1}{0}{244}{6}{1}{252}{25}{25}{0}{0}{244}{7}{1} {252}{25}{0}{0}{0}{244}{5}{1}{252}{25}{49}{0}{0}{244}{6}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{15}{2}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{143}{2}{0}{244}{8}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{46}{0}{0}{244}{7}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{25}{0}{0}{244}{7}{1}\n…{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{76}{1}{0}{244}{7}{1}{252}{25}{81}{0}{0}{244}{6}{1} {252}{25}{0}{0}{0}{244}{5}{1}{252}{25}{41}{0}{0}{244}{6}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{143}{2}{0}{244}{8}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{4}{0}{0}{244}{6}{1}{252}{25}{31}{0}{0}{244}{7}{1}{252}{25}{13}{0}{0}{244}{6}{1}{252}{25}{7}{0}{0}{244}{5}{1}{252}{25}{13}{0}{0}{244}{6}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{97}{2}{0}{244}{11}{1}\p{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{11}{0}{0}{244}{8}{1}{252}{25}{34}{0}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{9}{0}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{25}{0}{0}{244}{7}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{217}{0}{0}{244}{7}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{178}{0}{0}{244}{8}{1}{252}{25}{111}{1}{0}{244}{10}{1}{252}{25}{47}{2}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{72}{1}{0}{244}{6}{1}\n{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{13}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{46}{0}{0}{244}{7}{1}{252}{25}{12}{1}{0}{244}{8}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{19}{1}{0}{244}{7}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{223}{1}{0}{244}{5}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{7}{0}{0}{244}{5}{1}…\p{252}{25}{154}{0}{0}{244}{7}{1}{252}{25}{65}{2}{0}{244}{8}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{111}{1}{0}{244}{10}{1}{252}{25}{47}{2}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{50}{0}{0}{244}{6}{1}{252}{25}{25}{0}{0}{244}{7}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{7}{0}{0}{244}{5}{1}{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{239}{0}{0}{244}{8}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{24}{2}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{69}{1}{0}{244}{8}{1}?\p{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{125}{0}{0}{244}{6}{1}{252}{25}{39}{0}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{24}{2}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{26}{0}{0}{244}{7}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{178}{0}{0}{244}{8}{1}{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{32}{0}{0}{244}{7}{1}{252}{25}{0}{2}{0}{244}{6}{1}{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{76}{1}{0}{244}{7}{1}{252}{25}{134}{0}{0}{244}{7}{1}{252}{25}{32}{0}{0}{244}{7}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{7}{0}{0}{244}{5}{1}{252}{25}{0}{0}{0}{244}{5}{1}{252}{25}{39}{0}{0}{244}{6}{1}{252}{25}{15}{0}{0}{244}{6}{1}{252}{25}{104}{2}{0}{244}{8}{1}\n…{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{19}{1}{0}{244}{7}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{223}{1}{0}{244}{5}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{7}{0}{0}{244}{5}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{13}{0}{0}{244}{6}{1}{252}{25}{134}{0}{0}{244}{7}{1}{252}{25}{113}{1}{0}{244}{11}{1}{252}{25}{26}{0}{0}{244}{7}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{31}{0}{0}{244}{7}{1}…$"

Route128_Text_StevenImGoingToSootopolis:
	.string "{PLAYER}{KUN}…\n"
	.string "I don't know what you intend to do,\l"
	.string "but don't do anything reckless.\p"
	.string "Okay.\n"
	.string "I'm going to SOOTOPOLIS.$"

