Route116_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Route116_OnTransition
	map_script MAP_SCRIPT_ON_LOAD, Route116_OnLoad
	map_script MAP_SCRIPT_ON_FRAME_TABLE, Route116_OnFrame
	.byte 0

Route116_OnTransition:
	call_if_set FLAG_RECOVERED_DEVON_GOODS, Route116_EventScript_SetWandasBoyfriendPos
	call_if_eq VAR_SHOULD_END_ABNORMAL_WEATHER, 1, AbnormalWeather_EventScript_HideMapNamePopup
	call_if_eq VAR_ABNORMAL_WEATHER_LOCATION, ABNORMAL_WEATHER_ROUTE_116_NORTH, AbnormalWeather_StartGroudonWeather
	call_if_eq VAR_ABNORMAL_WEATHER_LOCATION, ABNORMAL_WEATHER_ROUTE_116_SOUTH, AbnormalWeather_StartGroudonWeather
	end

Route116_EventScript_SetWandasBoyfriendPos::
	setobjectxyperm LOCALID_ROUTE116_WANDAS_BF, 38, 10
	return

Route116_OnLoad:
	call_if_eq VAR_ABNORMAL_WEATHER_LOCATION, ABNORMAL_WEATHER_ROUTE_116_NORTH, AbnormalWeather_EventScript_PlaceTilesRoute116North
	call_if_eq VAR_ABNORMAL_WEATHER_LOCATION, ABNORMAL_WEATHER_ROUTE_116_SOUTH, AbnormalWeather_EventScript_PlaceTilesRoute116South
	end

Route116_OnFrame:
	map_script_2 VAR_SHOULD_END_ABNORMAL_WEATHER, 1, AbnormalWeather_EventScript_EndEventAndCleanup_1
	.2byte 0

Route116_EventScript_WandasBoyfriend::
	lock
	faceplayer
	goto_if_set FLAG_RECOVERED_DEVON_GOODS, Route116_EventScript_BoyfriendGruntLeftTunnel
	goto_if_set FLAG_DEVON_GOODS_STOLEN, Route116_EventScript_BoyfriendGruntInTunnel
	msgbox Route116_Text_WantToDigTunnel, MSGBOX_DEFAULT
	release
	end

Route116_EventScript_BoyfriendGruntLeftTunnel::
	msgbox Route116_Text_GoonHightailedItOutOfTunnel, MSGBOX_DEFAULT
	release
	end

Route116_EventScript_BoyfriendGruntInTunnel::
	msgbox Route116_Text_DiggingTunnelWhenGoonOrderedMeOut, MSGBOX_DEFAULT
	release
	end

Route116_EventScript_DevonEmployee::
	lock
	faceplayer
	goto_if_set FLAG_MET_DEVON_EMPLOYEE, Route116_EventScript_TryGiveRepeatBallAgain
	msgbox Route116_Text_ThankYouTokenOfAppreciation, MSGBOX_DEFAULT
	goto Route116_EventScript_GiveRepeatBall
	end

Route116_EventScript_GiveRepeatBall::
	setflag FLAG_MET_DEVON_EMPLOYEE
	giveitem ITEM_REPEAT_BALL
	goto_if_eq VAR_RESULT, FALSE, Route116_EventScript_NoRoomForRepeatBall
	msgbox Route116_Text_NewBallAvailableAtMart, MSGBOX_DEFAULT
	closemessage
	call_if_eq VAR_FACING, DIR_NORTH, Route116_EventScript_DevonEmployeeExit
	call_if_eq VAR_FACING, DIR_SOUTH, Route116_EventScript_DevonEmployeeExit
	call_if_eq VAR_FACING, DIR_WEST, Route116_EventScript_DevonEmployeeExit
	call_if_eq VAR_FACING, DIR_EAST, Route116_EventScript_DevonEmployeeExitEast
	removeobject VAR_LAST_TALKED
	clearflag FLAG_HIDE_RUSTBORO_CITY_DEVON_CORP_3F_EMPLOYEE
	setflag FLAG_RECEIVED_REPEAT_BALL
	release
	end

Route116_EventScript_DevonEmployeeExit::
	applymovement VAR_LAST_TALKED, Route116_Movement_DevonEmployeeExit
	waitmovement 0
	return

Route116_EventScript_DevonEmployeeExitEast::
	applymovement VAR_LAST_TALKED, Route116_Movement_DevonEmployeeExitEast
	waitmovement 0
	return

Route116_EventScript_TryGiveRepeatBallAgain::
	msgbox Route116_Text_TokenOfAppreciation, MSGBOX_DEFAULT
	goto Route116_EventScript_GiveRepeatBall
	end

Route116_EventScript_NoRoomForRepeatBall::
	msgbox Route116_Text_BagIsJamPacked, MSGBOX_DEFAULT
	release
	end

Route116_Movement_DevonEmployeeExit:
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	step_end

Route116_Movement_DevonEmployeeExitEast:
	walk_down
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	step_end

Route116_EventScript_RouteSignRustboro::
	msgbox Route116_Text_RouteSignRustboro, MSGBOX_SIGN
	end

Route116_EventScript_RusturfTunnelSign::
	msgbox Route116_Text_RusturfTunnelSign, MSGBOX_SIGN
	end

Route116_EventScript_TunnelersRestHouseSign::
	msgbox Route116_Text_TunnelersRestHouse, MSGBOX_SIGN
	end

Route116_EventScript_TrainerTipsBToStopEvolution::
	msgbox Route116_Text_TrainerTipsBToStopEvolution, MSGBOX_SIGN
	end

Route116_EventScript_TrainerTipsBagHasPockets::
	msgbox Route116_Text_TrainerTipsBagHasPockets, MSGBOX_SIGN
	end

Route116_EventScript_Briney::
	lock
	faceplayer
	msgbox Route116_Text_ScoundrelMadeOffWithPeeko, MSGBOX_DEFAULT
	setvar VAR_ROUTE116_STATE, 2
	release
	end

Route116_EventScript_BrineyTrigger::
	lockall
	applymovement LOCALID_ROUTE116_BRINEY, Common_Movement_WalkInPlaceFasterRight
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterLeft
	waitmovement 0
	msgbox Route116_Text_ScoundrelMadeOffWithPeeko, MSGBOX_DEFAULT
	setvar VAR_ROUTE116_STATE, 2
	releaseall
	end

Route116_EventScript_GlassesMan::
	lock
	faceplayer
	checkitem ITEM_BLACK_GLASSES
	goto_if_eq VAR_RESULT, TRUE, Route116_EventScript_PlayerHasGlasses
	specialvar VAR_RESULT, FoundBlackGlasses
	goto_if_eq VAR_RESULT, TRUE, Route116_EventScript_FoundGlassesNotOnPlayer
	msgbox Route116_Text_CanYouHelpMeFindGlasses, MSGBOX_DEFAULT
	release
	end

Route116_EventScript_FoundGlassesNotOnPlayer::
	msgbox Route116_Text_CantFindGlassesNotHere, MSGBOX_DEFAULT
	closemessage
	goto Route116_EventScript_GlassesManExit
	end

Route116_EventScript_PlayerHasGlasses::
	msgbox Route116_Text_CanYouHelpMeFindGlasses, MSGBOX_DEFAULT
	msgbox Route116_Text_MayISeeThoseGlasses, MSGBOX_DEFAULT
	specialvar VAR_RESULT, FoundBlackGlasses
	goto_if_eq VAR_RESULT, TRUE, Route116_EventScript_FoundGlassesOnPlayer
	msgbox Route116_Text_NotWhatImLookingFor, MSGBOX_DEFAULT
	release
	end

Route116_EventScript_FoundGlassesOnPlayer::
	msgbox Route116_Text_NotWhatImLookingForMaybeTheyArentHere, MSGBOX_DEFAULT
	closemessage
	goto Route116_EventScript_GlassesManExit
	end

Route116_EventScript_GlassesManExit::
	delay 20
	call_if_eq VAR_FACING, DIR_NORTH, Route116_EventScript_GlassesManExitNormal
	call_if_eq VAR_FACING, DIR_SOUTH, Route116_EventScript_GlassesManExitNormal
	call_if_eq VAR_FACING, DIR_WEST, Route116_EventScript_GlassesManExitNormal
	call_if_eq VAR_FACING, DIR_EAST, Route116_EventScript_GlassesManExitEast
	removeobject VAR_LAST_TALKED
	release
	end

Route116_EventScript_GlassesManExitNormal::
	applymovement VAR_LAST_TALKED, Route116_Movement_GlassesManExit
	waitmovement 0
	return

Route116_EventScript_GlassesManExitEast::
	applymovement VAR_LAST_TALKED, Route116_Movement_GlassesManExitEast
	waitmovement 0
	return

Route116_Movement_GlassesManExit:
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	step_end

Route116_Movement_GlassesManExitEast:
	walk_up
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	step_end

Route116_EventScript_Joey::
	trainerbattle_single TRAINER_JOEY, Route116_Text_JoeyIntro, Route116_Text_JoeyDefeat
	msgbox Route116_Text_JoeyPostBattle, MSGBOX_AUTOCLOSE
	end

Route116_EventScript_Jose::
	trainerbattle_single TRAINER_JOSE, Route116_Text_JoseIntro, Route116_Text_JoseDefeat
	msgbox Route116_Text_JosePostBattle, MSGBOX_AUTOCLOSE
	end

Route116_EventScript_Jerry::
	trainerbattle_single TRAINER_JERRY_1, Route116_Text_JerryIntro, Route116_Text_JerryDefeat, Route116_EventScript_TryRegisterJerryAfterBattle
	specialvar VAR_RESULT, ShouldTryRematchBattle
	goto_if_eq VAR_RESULT, TRUE, Route116_EventScript_RematchJerry
	setvar VAR_0x8004, TRAINER_JERRY_1
	specialvar VAR_RESULT, IsTrainerRegistered
	goto_if_eq VAR_RESULT, FALSE, Route116_EventScript_TryRegisterJerry
	msgbox Route116_Text_JerryPostBattle, MSGBOX_DEFAULT
	release
	end

Route116_EventScript_TryRegisterJerryAfterBattle::
	goto_if_set FLAG_HAS_MATCH_CALL, Route116_EventScript_RegisterJerryAfterBattle
	release
	end

Route116_EventScript_RegisterJerryAfterBattle::
	special PlayerFaceTrainerAfterBattle
	waitmovement 0
	msgbox Route116_Text_JerryRegister2, MSGBOX_DEFAULT
	register_matchcall TRAINER_JERRY_1
	release
	end

Route116_EventScript_TryRegisterJerry::
	goto_if_set FLAG_HAS_MATCH_CALL, Route116_EventScript_RegisterJerry
	msgbox Route116_Text_JerryPostBattle, MSGBOX_DEFAULT
	release
	end

Route116_EventScript_RegisterJerry::
	msgbox Route116_Text_JerryRegister1, MSGBOX_DEFAULT
	register_matchcall TRAINER_JERRY_1
	release
	end

Route116_EventScript_RematchJerry::
	trainerbattle_rematch TRAINER_JERRY_1, Route116_Text_JerryRematchIntro, Route116_Text_JerryRematchDefeat
	msgbox Route116_Text_JerryPostRematch, MSGBOX_AUTOCLOSE
	end

Route116_EventScript_Clark::
	trainerbattle_single TRAINER_CLARK, Route116_Text_ClarkIntro, Route116_Text_ClarkDefeat
	msgbox Route116_Text_ClarkPostBattle, MSGBOX_AUTOCLOSE
	end

Route116_EventScript_Janice::
	trainerbattle_single TRAINER_JANICE, Route116_Text_JaniceIntro, Route116_Text_JaniceDefeat
	msgbox Route116_Text_JanicePostBattle, MSGBOX_AUTOCLOSE
	end

Route116_EventScript_Karen::
	trainerbattle_single TRAINER_KAREN_1, Route116_Text_KarenIntro, Route116_Text_KarenDefeat, Route116_EventScript_TryRegisterKarenAfterBattle
	specialvar VAR_RESULT, ShouldTryRematchBattle
	goto_if_eq VAR_RESULT, TRUE, Route116_EventScript_RematchKaren
	setvar VAR_0x8004, TRAINER_KAREN_1
	specialvar VAR_RESULT, IsTrainerRegistered
	goto_if_eq VAR_RESULT, FALSE, Route116_EventScript_TryRegisterKaren
	msgbox Route116_Text_KarenPostBattle, MSGBOX_DEFAULT
	release
	end

Route116_EventScript_TryRegisterKarenAfterBattle::
	goto_if_set FLAG_HAS_MATCH_CALL, Route116_EventScript_RegisterKarenAfterBattle
	release
	end

Route116_EventScript_RegisterKarenAfterBattle::
	special PlayerFaceTrainerAfterBattle
	waitmovement 0
	msgbox Route116_Text_KarenRegister2, MSGBOX_DEFAULT
	register_matchcall TRAINER_KAREN_1
	release
	end

Route116_EventScript_TryRegisterKaren::
	goto_if_set FLAG_HAS_MATCH_CALL, Route116_EventScript_RegisterKaren
	msgbox Route116_Text_KarenPostBattle, MSGBOX_DEFAULT
	release
	end

Route116_EventScript_RegisterKaren::
	msgbox Route116_Text_KarenRegister1, MSGBOX_DEFAULT
	register_matchcall TRAINER_KAREN_1
	release
	end

Route116_EventScript_RematchKaren::
	trainerbattle_rematch TRAINER_KAREN_1, Route116_Text_KarenRematchIntro, Route116_Text_KarenRematchDefeat
	msgbox Route116_Text_KarenPostRematch, MSGBOX_AUTOCLOSE
	end

Route116_EventScript_Sarah::
	trainerbattle_single TRAINER_SARAH, Route116_Text_SarahIntro, Route116_Text_SarahDefeat
	msgbox Route116_Text_SarahPostBattle, MSGBOX_AUTOCLOSE
	end

Route116_EventScript_Dawson::
	trainerbattle_single TRAINER_DAWSON, Route116_Text_DawsonIntro, Route116_Text_DawsonDefeat
	msgbox Route116_Text_DawsonPostBattle, MSGBOX_AUTOCLOSE
	end

Route116_EventScript_Devan::
	trainerbattle_single TRAINER_DEVAN, Route116_Text_DevanIntro, Route116_Text_DevanDefeat
	msgbox Route116_Text_DevanPostBattle, MSGBOX_AUTOCLOSE
	end

Route116_EventScript_Johnson::
	trainerbattle_single TRAINER_JOHNSON, Route116_Text_JohnsonIntro, Route116_Text_JohnsonDefeat
	msgbox Route116_Text_JohnsonPostBattle, MSGBOX_AUTOCLOSE
	end

Route116_Text_ScoundrelMadeOffWithPeeko:
.string "{252}{25}{0}{0}{0}{244}{5}{1}{252}{25}{95}{2}{0}{244}{6}{1}{252}{25}{39}{0}{0}{244}{6}{1} {252}{25}{29}{2}{0}{244}{8}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{13}{0}{0}{244}{6}{1}{252}{25}{7}{0}{0}{244}{5}{1}{252}{25}{117}{1}{0}{244}{11}{1}{252}{25}{45}{2}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{123}{0}{0}{244}{7}{1}?\p{252}{25}{29}{2}{0}{244}{8}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{24}{2}{0}{244}{6}{1}{252}{25}{31}{0}{0}{244}{7}{1}{252}{25}{132}{0}{0}{244}{8}{1}{252}{25}{0}{0}{0}{244}{5}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{7}{0}{0}{244}{5}{1}{252}{25}{111}{1}{0}{244}{10}{1}{252}{25}{47}{2}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{64}{0}{0}{244}{7}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{79}{1}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{24}{2}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{248}{1}{0}{244}{6}{1}{252}{25}{233}{1}{0}{244}{6}{1} {252}{25}{1}{0}{0}{244}{6}{1}\n{252}{25}{0}{2}{0}{244}{6}{1}{252}{25}{134}{0}{0}{244}{7}{1}{252}{25}{10}{0}{0}{244}{7}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{32}{0}{0}{244}{7}{1}{252}{25}{41}{0}{0}{244}{6}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{46}{0}{0}{244}{7}{1}{252}{25}{96}{1}{0}{244}{8}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{233}{1}{0}{244}{6}{1}{252}{25}{0}{0}{0}{244}{5}{1}{252}{25}{13}{0}{0}{244}{6}{1}{252}{25}{38}{0}{0}{244}{7}{1}…\p{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{88}{1}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{42}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{39}{0}{0}{244}{6}{1}{252}{25}{105}{1}{0}{244}{5}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{39}{0}{0}{244}{6}{1}{252}{25}{65}{2}{0}{244}{8}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{35}{0}{0}{244}{8}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{132}{0}{0}{244}{8}{1}\n{252}{25}{0}{0}{0}{244}{5}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{7}{0}{0}{244}{5}{1}{252}{25}{154}{0}{0}{244}{7}{1}{252}{25}{46}{2}{0}{244}{5}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{9}{0}{0}{244}{6}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{29}{2}{0}{244}{8}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{32}{0}{0}{244}{7}{1}!\p{252}{25}{0}{0}{0}{244}{5}{1}{252}{25}{49}{0}{0}{244}{6}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{8}{0}{0}{244}{6}{1}! {252}{25}{132}{0}{0}{244}{8}{1}{252}{25}{0}{0}{0}{244}{5}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{7}{0}{0}{244}{5}{1}!$"

Route116_Text_WantToDigTunnel:
	.string "Nnn… Roar!\p"
	.string "I want to dig that tunnel!$"

Route116_Text_DiggingTunnelWhenGoonOrderedMeOut:
.string "{252}{25}{26}{1}{0}{244}{6}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{38}{0}{0}{244}{7}{1}… {252}{25}{0}{0}{0}{244}{5}{1}{252}{25}{49}{0}{0}{244}{6}{1}{252}{25}{8}{0}{0}{244}{6}{1}!\n{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{50}{0}{0}{244}{6}{1}{252}{25}{25}{0}{0}{244}{7}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{7}{0}{0}{244}{5}{1}{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{239}{0}{0}{244}{8}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{24}{2}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{155}{0}{0}{244}{8}{1}{252}{25}{39}{0}{0}{244}{6}{1}?\p{252}{25}{29}{2}{0}{244}{8}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{111}{1}{0}{244}{10}{1}{252}{25}{47}{2}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{141}{1}{0}{244}{6}{1}{252}{25}{25}{0}{0}{244}{7}{1}{252}{25}{166}{1}{0}{244}{6}{1}{252}{25}{0}{0}{0}{244}{5}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{123}{2}{0}{244}{7}{1}{252}{25}{92}{1}{0}{244}{7}{1}{252}{25}{42}{0}{0}{244}{6}{1}{252}{25}{39}{0}{0}{244}{6}{1}{252}{25}{19}{1}{0}{244}{7}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{32}{0}{0}{244}{7}{1}{252}{25}{79}{1}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{248}{1}{0}{244}{6}{1}{252}{25}{123}{0}{0}{244}{7}{1} {252}{25}{1}{0}{0}{244}{6}{1}\n{252}{25}{0}{2}{0}{244}{6}{1}{252}{25}{134}{0}{0}{244}{7}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{88}{1}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{10}{0}{0}{244}{7}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{105}{1}{0}{244}{5}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{39}{0}{0}{244}{6}{1}{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{79}{1}{0}{244}{6}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{6}{0}{0}{244}{4}{1}!\p{252}{25}{4}{0}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{166}{1}{0}{244}{6}{1}{252}{25}{0}{0}{0}{244}{5}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{123}{2}{0}{244}{7}{1}{252}{25}{134}{0}{0}{244}{7}{1}{252}{25}{0}{0}{0}{244}{5}{1}{252}{25}{32}{0}{0}{244}{7}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}\n{252}{25}{154}{0}{0}{244}{7}{1}{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{42}{0}{0}{244}{6}{1}{252}{25}{66}{1}{0}{244}{7}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{140}{0}{0}{244}{6}{1}{252}{25}{39}{0}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{32}{2}{0}{244}{7}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{8}{0}{0}{244}{6}{1}\l{252}{25}{35}{0}{0}{244}{8}{1}{252}{25}{42}{0}{0}{244}{6}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{44}{2}{0}{244}{7}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{13}{0}{0}{244}{6}{1}{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{26}{0}{0}{244}{7}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{34}{1}{0}{244}{7}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{92}{1}{0}{244}{7}{1}\p{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{35}{0}{0}{244}{8}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{7}{0}{0}{244}{5}{1}{252}{25}{84}{2}{0}{244}{7}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{202}{0}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{79}{0}{0}{244}{6}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{4}{0}{0}{244}{6}{1}{252}{25}{90}{1}{0}{244}{6}{1}\n{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{10}{0}{0}{244}{7}{1}{252}{25}{46}{1}{0}{244}{6}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{28}{2}{0}{244}{6}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{46}{0}{0}{244}{7}{1}{252}{25}{36}{2}{0}{244}{9}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{4}{0}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{141}{1}{0}{244}{6}{1}{252}{25}{25}{0}{0}{244}{7}{1}{252}{25}{166}{1}{0}{244}{6}{1}{252}{25}{0}{0}{0}{244}{5}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{123}{2}{0}{244}{7}{1}…\p{252}{25}{29}{2}{0}{244}{8}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{47}{2}{0}{244}{6}{1}{252}{25}{42}{0}{0}{244}{6}{1}{252}{25}{80}{1}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{88}{1}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{10}{0}{0}{244}{7}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{65}{2}{0}{244}{8}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{13}{0}{0}{244}{6}{1}{252}{25}{7}{0}{0}{244}{5}{1}{252}{25}{117}{1}{0}{244}{11}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{46}{1}{0}{244}{6}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{0}{0}{0}{244}{5}{1}{252}{25}{59}{1}{0}{244}{4}{1} {252}{25}{1}{0}{0}{244}{6}{1}\n{252}{25}{13}{0}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{0}{0}{0}{244}{5}{1}{252}{25}{32}{0}{0}{244}{7}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{26}{0}{0}{244}{7}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{4}{0}{0}{244}{6}{1}{252}{25}{13}{0}{0}{244}{6}{1}{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{106}{1}{0}{244}{6}{1}{252}{25}{42}{0}{0}{244}{6}{1}\l{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{26}{0}{0}{244}{7}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{34}{1}{0}{244}{7}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{24}{2}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{46}{0}{0}{244}{7}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{25}{0}{0}{244}{7}{1}$"

Route116_Text_GoonHightailedItOutOfTunnel:
.string "{252}{25}{26}{1}{0}{244}{6}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{38}{0}{0}{244}{7}{1}… {252}{25}{0}{0}{0}{244}{5}{1}{252}{25}{49}{0}{0}{244}{6}{1}{252}{25}{8}{0}{0}{244}{6}{1}!\p{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{88}{1}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{183}{0}{0}{244}{9}{1}{252}{25}{39}{0}{0}{244}{6}{1}{252}{25}{65}{2}{0}{244}{8}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{72}{1}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{13}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{166}{1}{0}{244}{6}{1}{252}{25}{0}{0}{0}{244}{5}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{123}{2}{0}{244}{7}{1}{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{32}{0}{0}{244}{7}{1}{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{106}{1}{0}{244}{6}{1}{252}{25}{42}{0}{0}{244}{6}{1}!\n{252}{25}{29}{2}{0}{244}{8}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{47}{2}{0}{244}{6}{1}{252}{25}{31}{0}{0}{244}{7}{1}{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{32}{0}{0}{244}{7}{1}{252}{25}{141}{1}{0}{244}{6}{1}{252}{25}{25}{0}{0}{244}{7}{1}{252}{25}{66}{1}{0}{244}{7}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{92}{1}{0}{244}{7}{1}{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{106}{1}{0}{244}{6}{1}{252}{25}{42}{0}{0}{244}{6}{1}!$"

Route116_Text_ThankYouTokenOfAppreciation:
	.string "Oh! It's you!\p"
	.string "You're that person who not only helped\n"
	.string "me in PETALBURG WOODS, but also got\l"
	.string "back my stolen package and then even\l"
	.string "graciously delivered it to SLATEPORT!\p"
	.string "CAPT. STERN informed us that the\n"
	.string "package arrived, too!\p"
	.string "I thank you very, very much!\p"
	.string "Why, if I were a rain cloud, I would\n"
	.string "shower you with gratitude and hail\l"
	.string "you as a hero!\p"
	.string "For you, the most wonderful TRAINER,\n"
	.string "I bear good news!\p"
	.string "Recently, our company developed\n"
	.string "a new kind of POKé BALL.\p"
	.string "As a token of our appreciation, this\n"
	.string "is our gift to our wonderful TRAINER!$"

Route116_Text_NewBallAvailableAtMart:
	.string "Our new POKé BALL will be available\n"
	.string "at the POKéMON MART in RUSTBORO.\p"
	.string "Please do try it out!\n"
	.string "Thank you and bye-bye!$"

Route116_Text_BagIsJamPacked:
	.string "Your BAG is jam-packed.\n"
	.string "I can't give you this REPEAT BALL.$"

Route116_Text_TokenOfAppreciation:
	.string "As a token of our appreciation for\n"
	.string "your delivering our package, I have\l"
	.string "a gift of a new kind of POKé BALL\l"
	.string "for our most wonderful TRAINER!$"

Route116_Text_CanYouHelpMeFindGlasses:
	.string "I dropped my glasses…\n"
	.string "Can you help me find them?$"

Route116_Text_MayISeeThoseGlasses:
	.string "Those glasses!\n"
	.string "May I see them for a second?$"

Route116_Text_NotWhatImLookingForMaybeTheyArentHere:
	.string "Hmm…\n"
	.string "These are BLACKGLASSES.\l"
	.string "They're not what I'm looking for…\p"
	.string "Maybe my glasses aren't around\n"
	.string "here…$"

Route116_Text_CantFindGlassesNotHere:
	.string "Hmm…\n"
	.string "I can't find my glasses anywhere…\l"
	.string "Maybe they're not around here…$"

Route116_Text_NotWhatImLookingFor:
	.string "Hmm…\n"
	.string "These are BLACKGLASSES.\l"
	.string "They're not what I'm looking for…$"

Route116_Text_RouteSignRustboro:
	.string "ROUTE 116\n"
	.string "{LEFT_ARROW} RUSTBORO CITY$"

Route116_Text_RusturfTunnelSign:
	.string "RUSTURF TUNNEL\n"
	.string "“Linking RUSTBORO and VERDANTURF\p"
	.string "“The tunnel project has been\n"
	.string "canceled.”$"

Route116_Text_TunnelersRestHouse:
	.string "TUNNELER'S REST HOUSE$"

Route116_Text_TrainerTipsBToStopEvolution:
	.string "TRAINER TIPS\p"
	.string "If you want to stop a POKéMON from\n"
	.string "evolving, press the B Button while it\l"
	.string "is trying to evolve.\l"
	.string "The startled POKéMON will stop.\p"
	.string "This is called an evolution cancel.$"

Route116_Text_TrainerTipsBagHasPockets:
	.string "TRAINER TIPS\p"
	.string "Your BAG has several POCKETS.\p"
	.string "Items you obtain are automatically\n"
	.string "placed in the appropriate POCKETS.\p"
	.string "No TRAINER can afford to be without\n"
	.string "a BAG of their own.$"

