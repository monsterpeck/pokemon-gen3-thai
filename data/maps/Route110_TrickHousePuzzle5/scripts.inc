Route110_TrickHousePuzzle5_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Route110_TrickHousePuzzle5_OnTransition
	.byte 0

Route110_TrickHousePuzzle5_OnTransition:
	setvar VAR_TEMP_1, 0
	setvar VAR_TEMP_2, 0
	setvar VAR_TEMP_3, 0
	setvar VAR_TEMP_4, 0
	setvar VAR_TEMP_5, 0
	setvar VAR_TEMP_8, 0
	end

Route110_TrickHousePuzzle5_EventScript_Scroll::
	lockall
	goto_if_eq VAR_TRICK_HOUSE_PUZZLE_5_STATE, 0, Route110_TrickHousePuzzle5_EventScript_FoundScroll
	goto Route110_TrickHousePuzzle_EventScript_ReadScrollAgain
	end

Route110_TrickHousePuzzle5_EventScript_FoundScroll::
	setvar VAR_TRICK_HOUSE_PUZZLE_5_STATE, 1
	goto Route110_TrickHousePuzzle_EventScript_FoundScroll
	end

Route110_TrickHousePuzzle5_EventScript_Mechadoll1::
	lockall
	applymovement LOCALID_MECHADOLL_1, Common_Movement_FacePlayer
	waitmovement 0
	goto_if_eq VAR_TEMP_1, 1, Route110_TrickHousePuzzle5_EventScript_CorrectGoThrough
	setvar VAR_TEMP_9, 0
	goto Route110_TrickHousePuzzle5_EventScript_Mechadoll1Activate
	end

Route110_TrickHousePuzzle5_EventScript_Mechadoll2::
	lockall
	applymovement LOCALID_MECHADOLL_2, Common_Movement_FacePlayer
	waitmovement 0
	goto_if_eq VAR_TEMP_2, 1, Route110_TrickHousePuzzle5_EventScript_CorrectGoThrough
	setvar VAR_TEMP_9, 0
	goto Route110_TrickHousePuzzle5_EventScript_Mechadoll2Activate
	end

Route110_TrickHousePuzzle5_EventScript_Mechadoll3::
	lockall
	applymovement LOCALID_MECHADOLL_3, Common_Movement_FacePlayer
	waitmovement 0
	goto_if_eq VAR_TEMP_3, 1, Route110_TrickHousePuzzle5_EventScript_CorrectGoThrough
	setvar VAR_TEMP_9, 0
	goto Route110_TrickHousePuzzle5_EventScript_Mechadoll3Activate
	end

Route110_TrickHousePuzzle5_EventScript_Mechadoll4::
	lockall
	applymovement LOCALID_MECHADOLL_4, Common_Movement_FacePlayer
	waitmovement 0
	goto_if_eq VAR_TEMP_4, 1, Route110_TrickHousePuzzle5_EventScript_CorrectGoThrough
	setvar VAR_TEMP_9, 0
	goto Route110_TrickHousePuzzle5_EventScript_Mechadoll4Activate
	end

Route110_TrickHousePuzzle5_EventScript_Mechadoll5::
	lockall
	applymovement LOCALID_MECHADOLL_5, Common_Movement_FacePlayer
	waitmovement 0
	goto_if_eq VAR_TEMP_5, 1, Route110_TrickHousePuzzle5_EventScript_CorrectGoThrough
	setvar VAR_TEMP_9, 0
	goto Route110_TrickHousePuzzle5_EventScript_Mechadoll5Activate
	end

Route110_TrickHousePuzzle5_EventScript_Mechadoll1Trigger0::
	lockall
	setvar VAR_TEMP_9, 0
	goto Route110_TrickHousePuzzle5_EventScript_Mechadoll1Activate
	end

Route110_TrickHousePuzzle5_EventScript_Mechadoll1Trigger1::
	lockall
	setvar VAR_TEMP_9, 1
	goto Route110_TrickHousePuzzle5_EventScript_Mechadoll1Activate
	end

Route110_TrickHousePuzzle5_EventScript_Mechadoll1Trigger2::
	lockall
	setvar VAR_TEMP_9, 2
	goto Route110_TrickHousePuzzle5_EventScript_Mechadoll1Activate
	end

Route110_TrickHousePuzzle5_EventScript_Mechadoll1Trigger3::
	lockall
	setvar VAR_TEMP_9, 3
	goto Route110_TrickHousePuzzle5_EventScript_Mechadoll1Activate
	end

Route110_TrickHousePuzzle5_EventScript_Mechadoll1Trigger4::
	lockall
	setvar VAR_TEMP_9, 4
	goto Route110_TrickHousePuzzle5_EventScript_Mechadoll1Activate
	end

Route110_TrickHousePuzzle5_EventScript_Mechadoll2Trigger0::
	lockall
	setvar VAR_TEMP_9, 0
	goto Route110_TrickHousePuzzle5_EventScript_Mechadoll2Activate
	end

Route110_TrickHousePuzzle5_EventScript_Mechadoll2Trigger1::
	lockall
	setvar VAR_TEMP_9, 1
	goto Route110_TrickHousePuzzle5_EventScript_Mechadoll2Activate
	end

Route110_TrickHousePuzzle5_EventScript_Mechadoll2Trigger2::
	lockall
	setvar VAR_TEMP_9, 2
	goto Route110_TrickHousePuzzle5_EventScript_Mechadoll2Activate
	end

Route110_TrickHousePuzzle5_EventScript_Mechadoll2Trigger3::
	lockall
	setvar VAR_TEMP_9, 3
	goto Route110_TrickHousePuzzle5_EventScript_Mechadoll2Activate
	end

Route110_TrickHousePuzzle5_EventScript_Mechadoll2Trigger4::
	lockall
	setvar VAR_TEMP_9, 4
	goto Route110_TrickHousePuzzle5_EventScript_Mechadoll2Activate
	end

Route110_TrickHousePuzzle5_EventScript_Mechadoll2Trigger5::
	lockall
	setvar VAR_TEMP_9, 5
	goto Route110_TrickHousePuzzle5_EventScript_Mechadoll2Activate
	end

Route110_TrickHousePuzzle5_EventScript_Mechadoll3Trigger0::
	lockall
	setvar VAR_TEMP_9, 0
	goto Route110_TrickHousePuzzle5_EventScript_Mechadoll3Activate
	end

Route110_TrickHousePuzzle5_EventScript_Mechadoll3Trigger1::
	lockall
	setvar VAR_TEMP_9, 1
	goto Route110_TrickHousePuzzle5_EventScript_Mechadoll3Activate
	end

Route110_TrickHousePuzzle5_EventScript_Mechadoll3Trigger2::
	lockall
	setvar VAR_TEMP_9, 2
	goto Route110_TrickHousePuzzle5_EventScript_Mechadoll3Activate
	end

Route110_TrickHousePuzzle5_EventScript_Mechadoll3Trigger3::
	lockall
	setvar VAR_TEMP_9, 3
	goto Route110_TrickHousePuzzle5_EventScript_Mechadoll3Activate
	end

Route110_TrickHousePuzzle5_EventScript_Mechadoll3Trigger4::
	lockall
	setvar VAR_TEMP_9, 4
	goto Route110_TrickHousePuzzle5_EventScript_Mechadoll3Activate
	end

Route110_TrickHousePuzzle5_EventScript_Mechadoll4Trigger0::
	lockall
	setvar VAR_TEMP_9, 0
	goto Route110_TrickHousePuzzle5_EventScript_Mechadoll4Activate
	end

Route110_TrickHousePuzzle5_EventScript_Mechadoll4Trigger1::
	lockall
	setvar VAR_TEMP_9, 1
	goto Route110_TrickHousePuzzle5_EventScript_Mechadoll4Activate
	end

Route110_TrickHousePuzzle5_EventScript_Mechadoll4Trigger2::
	lockall
	setvar VAR_TEMP_9, 2
	goto Route110_TrickHousePuzzle5_EventScript_Mechadoll4Activate
	end

Route110_TrickHousePuzzle5_EventScript_Mechadoll4Trigger3::
	lockall
	setvar VAR_TEMP_9, 3
	goto Route110_TrickHousePuzzle5_EventScript_Mechadoll4Activate
	end

Route110_TrickHousePuzzle5_EventScript_Mechadoll4Trigger4::
	lockall
	setvar VAR_TEMP_9, 4
	goto Route110_TrickHousePuzzle5_EventScript_Mechadoll4Activate
	end

@ Unused
Route110_TrickHousePuzzle5_EventScript_Mechadoll4Trigger5::
	lockall
	setvar VAR_TEMP_9, 5
	goto Route110_TrickHousePuzzle5_EventScript_Mechadoll4Activate
	end

Route110_TrickHousePuzzle5_EventScript_Mechadoll5Trigger0::
	lockall
	setvar VAR_TEMP_9, 0
	goto Route110_TrickHousePuzzle5_EventScript_Mechadoll5Activate
	end

Route110_TrickHousePuzzle5_EventScript_Mechadoll1Activate::
	setvar VAR_TEMP_1, 1
	setvar VAR_TEMP_8, LOCALID_MECHADOLL_1
	playse SE_PIN
	applymovement LOCALID_MECHADOLL_1, Common_Movement_ExclamationMark
	waitmovement 0
	applymovement LOCALID_MECHADOLL_1, Common_Movement_Delay48
	waitmovement 0
	call_if_eq VAR_TEMP_9, 1, Route110_TrickHousePuzzle5_EventScript_MechadollWalkLeft1
	call_if_eq VAR_TEMP_9, 2, Route110_TrickHousePuzzle5_EventScript_MechadollWalkLeft2
	call_if_eq VAR_TEMP_9, 3, Route110_TrickHousePuzzle5_EventScript_MechadollWalkLeft3
	call_if_eq VAR_TEMP_9, 4, Route110_TrickHousePuzzle5_EventScript_MechadollWalkLeft4
	msgbox Route110_TrickHousePuzzle5_Text_Mechadoll1Intro, MSGBOX_DEFAULT
	random 3
	switch VAR_RESULT
	case 0, Route110_TrickHousePuzzle5_EventScript_Mechadoll1Quiz1
	case 1, Route110_TrickHousePuzzle5_EventScript_Mechadoll1Quiz2
	case 2, Route110_TrickHousePuzzle5_EventScript_Mechadoll1Quiz3
	end

Route110_TrickHousePuzzle5_EventScript_Mechadoll2Activate::
	setvar VAR_TEMP_2, 1
	setvar VAR_TEMP_8, LOCALID_MECHADOLL_2
	playse SE_PIN
	applymovement LOCALID_MECHADOLL_2, Common_Movement_ExclamationMark
	waitmovement 0
	applymovement LOCALID_MECHADOLL_2, Common_Movement_Delay48
	waitmovement 0
	call_if_eq VAR_TEMP_9, 1, Route110_TrickHousePuzzle5_EventScript_MechadollWalkRight1
	call_if_eq VAR_TEMP_9, 2, Route110_TrickHousePuzzle5_EventScript_MechadollWalkRight2
	call_if_eq VAR_TEMP_9, 3, Route110_TrickHousePuzzle5_EventScript_MechadollWalkRight3
	call_if_eq VAR_TEMP_9, 4, Route110_TrickHousePuzzle5_EventScript_MechadollWalkRight4
	call_if_eq VAR_TEMP_9, 5, Route110_TrickHousePuzzle5_EventScript_MechadollWalkRight5
	msgbox Route110_TrickHousePuzzle5_Text_Mechadoll2Intro, MSGBOX_DEFAULT
	random 3
	switch VAR_RESULT
	case 0, Route110_TrickHousePuzzle5_EventScript_Mechadoll2Quiz1
	case 1, Route110_TrickHousePuzzle5_EventScript_Mechadoll2Quiz2
	case 2, Route110_TrickHousePuzzle5_EventScript_Mechadoll2Quiz3
	end

Route110_TrickHousePuzzle5_EventScript_Mechadoll3Activate::
	setvar VAR_TEMP_3, 1
	setvar VAR_TEMP_8, LOCALID_MECHADOLL_3
	playse SE_PIN
	applymovement LOCALID_MECHADOLL_3, Common_Movement_ExclamationMark
	waitmovement 0
	applymovement LOCALID_MECHADOLL_3, Common_Movement_Delay48
	waitmovement 0
	call_if_eq VAR_TEMP_9, 1, Route110_TrickHousePuzzle5_EventScript_MechadollWalkLeft1
	call_if_eq VAR_TEMP_9, 2, Route110_TrickHousePuzzle5_EventScript_MechadollWalkLeft2
	call_if_eq VAR_TEMP_9, 3, Route110_TrickHousePuzzle5_EventScript_MechadollWalkLeft3
	call_if_eq VAR_TEMP_9, 4, Route110_TrickHousePuzzle5_EventScript_MechadollWalkLeft4
	msgbox Route110_TrickHousePuzzle5_Text_Mechadoll3Intro, MSGBOX_DEFAULT
	random 3
	switch VAR_RESULT
	case 0, Route110_TrickHousePuzzle5_EventScript_Mechadoll3Quiz1
	case 1, Route110_TrickHousePuzzle5_EventScript_Mechadoll3Quiz2
	case 2, Route110_TrickHousePuzzle5_EventScript_Mechadoll3Quiz3
	end

Route110_TrickHousePuzzle5_EventScript_Mechadoll4Activate::
	setvar VAR_TEMP_4, 1
	setvar VAR_TEMP_8, LOCALID_MECHADOLL_4
	playse SE_PIN
	applymovement LOCALID_MECHADOLL_4, Common_Movement_ExclamationMark
	waitmovement 0
	applymovement LOCALID_MECHADOLL_4, Common_Movement_Delay48
	waitmovement 0
	call_if_eq VAR_TEMP_9, 1, Route110_TrickHousePuzzle5_EventScript_MechadollWalkLeft1
	call_if_eq VAR_TEMP_9, 2, Route110_TrickHousePuzzle5_EventScript_MechadollWalkLeft2
	call_if_eq VAR_TEMP_9, 3, Route110_TrickHousePuzzle5_EventScript_MechadollWalkLeft3
	call_if_eq VAR_TEMP_9, 4, Route110_TrickHousePuzzle5_EventScript_MechadollWalkLeft4
	msgbox Route110_TrickHousePuzzle5_Text_Mechadoll4Intro, MSGBOX_DEFAULT
	random 3
	switch VAR_RESULT
	case 0, Route110_TrickHousePuzzle5_EventScript_Mechadoll4Quiz1
	case 1, Route110_TrickHousePuzzle5_EventScript_Mechadoll4Quiz2
	case 2, Route110_TrickHousePuzzle5_EventScript_Mechadoll4Quiz3
	end

Route110_TrickHousePuzzle5_EventScript_Mechadoll5Activate::
	setvar VAR_TEMP_5, 1
	setvar VAR_TEMP_8, LOCALID_MECHADOLL_5
	playse SE_PIN
	applymovement LOCALID_MECHADOLL_5, Common_Movement_ExclamationMark
	waitmovement 0
	applymovement LOCALID_MECHADOLL_5, Common_Movement_Delay48
	waitmovement 0
	msgbox Route110_TrickHousePuzzle5_Text_Mechadoll5Intro, MSGBOX_DEFAULT
	random 3
	switch VAR_RESULT
	case 0, Route110_TrickHousePuzzle5_EventScript_Mechadoll5Quiz1
	case 1, Route110_TrickHousePuzzle5_EventScript_Mechadoll5Quiz2
	case 2, Route110_TrickHousePuzzle5_EventScript_Mechadoll5Quiz3
	end

Route110_TrickHousePuzzle5_EventScript_Mechadoll1Quiz1::
	msgbox Route110_TrickHousePuzzle5_Text_Mechadoll1Quiz1, MSGBOX_DEFAULT
	multichoice 0, 0, MULTI_MECHADOLL1_Q1, TRUE
	switch VAR_RESULT
	case 2, Route110_TrickHousePuzzle5_EventScript_CorrectAnswer
	goto Route110_TrickHousePuzzle5_EventScript_IncorrectAnswer
	end

Route110_TrickHousePuzzle5_EventScript_Mechadoll1Quiz2::
	msgbox Route110_TrickHousePuzzle5_Text_Mechadoll1Quiz2, MSGBOX_DEFAULT
	multichoice 0, 0, MULTI_MECHADOLL1_Q2, TRUE
	switch VAR_RESULT
	case 0, Route110_TrickHousePuzzle5_EventScript_CorrectAnswer
	goto Route110_TrickHousePuzzle5_EventScript_IncorrectAnswer
	end

Route110_TrickHousePuzzle5_EventScript_Mechadoll1Quiz3::
	msgbox Route110_TrickHousePuzzle5_Text_Mechadoll1Quiz3, MSGBOX_DEFAULT
	multichoice 0, 0, MULTI_MECHADOLL1_Q3, TRUE
	switch VAR_RESULT
	case 0, Route110_TrickHousePuzzle5_EventScript_CorrectAnswer
	goto Route110_TrickHousePuzzle5_EventScript_IncorrectAnswer
	end

Route110_TrickHousePuzzle5_EventScript_Mechadoll2Quiz1::
	msgbox Route110_TrickHousePuzzle5_Text_Mechadoll2Quiz1, MSGBOX_DEFAULT
	multichoice 0, 0, MULTI_MECHADOLL2_Q1, TRUE
	switch VAR_RESULT
	case 1, Route110_TrickHousePuzzle5_EventScript_CorrectAnswer
	goto Route110_TrickHousePuzzle5_EventScript_IncorrectAnswer
	end

Route110_TrickHousePuzzle5_EventScript_Mechadoll2Quiz2::
	msgbox Route110_TrickHousePuzzle5_Text_Mechadoll2Quiz2, MSGBOX_DEFAULT
	multichoice 0, 0, MULTI_MECHADOLL2_Q2, TRUE
	switch VAR_RESULT
	case 2, Route110_TrickHousePuzzle5_EventScript_CorrectAnswer
	goto Route110_TrickHousePuzzle5_EventScript_IncorrectAnswer
	end

Route110_TrickHousePuzzle5_EventScript_Mechadoll2Quiz3::
	msgbox Route110_TrickHousePuzzle5_Text_Mechadoll2Quiz3, MSGBOX_DEFAULT
	multichoice 0, 0, MULTI_MECHADOLL2_Q3, TRUE
	switch VAR_RESULT
	case 0, Route110_TrickHousePuzzle5_EventScript_CorrectAnswer
	goto Route110_TrickHousePuzzle5_EventScript_IncorrectAnswer
	end

Route110_TrickHousePuzzle5_EventScript_Mechadoll3Quiz1::
	msgbox Route110_TrickHousePuzzle5_Text_Mechadoll3Quiz1, MSGBOX_DEFAULT
	multichoice 0, 0, MULTI_MECHADOLL3_Q1, TRUE
	switch VAR_RESULT
	case 0, Route110_TrickHousePuzzle5_EventScript_CorrectAnswer
	goto Route110_TrickHousePuzzle5_EventScript_IncorrectAnswer
	end

Route110_TrickHousePuzzle5_EventScript_Mechadoll3Quiz2::
	msgbox Route110_TrickHousePuzzle5_Text_Mechadoll3Quiz2, MSGBOX_DEFAULT
	multichoice 0, 0, MULTI_MECHADOLL3_Q2, TRUE
	switch VAR_RESULT
	case 2, Route110_TrickHousePuzzle5_EventScript_CorrectAnswer
	goto Route110_TrickHousePuzzle5_EventScript_IncorrectAnswer
	end

Route110_TrickHousePuzzle5_EventScript_Mechadoll3Quiz3::
	msgbox Route110_TrickHousePuzzle5_Text_Mechadoll3Quiz3, MSGBOX_DEFAULT
	multichoice 0, 0, MULTI_MECHADOLL3_Q3, TRUE
	switch VAR_RESULT
	case 1, Route110_TrickHousePuzzle5_EventScript_CorrectAnswer
	goto Route110_TrickHousePuzzle5_EventScript_IncorrectAnswer
	end

Route110_TrickHousePuzzle5_EventScript_Mechadoll4Quiz1::
	msgbox Route110_TrickHousePuzzle5_Text_Mechadoll4Quiz1, MSGBOX_DEFAULT
	multichoice 0, 0, MULTI_MECHADOLL4_Q1, TRUE
	switch VAR_RESULT
	case 0, Route110_TrickHousePuzzle5_EventScript_CorrectAnswer
	goto Route110_TrickHousePuzzle5_EventScript_IncorrectAnswer
	end

Route110_TrickHousePuzzle5_EventScript_Mechadoll4Quiz2::
	msgbox Route110_TrickHousePuzzle5_Text_Mechadoll4Quiz2, MSGBOX_DEFAULT
	multichoice 0, 0, MULTI_MECHADOLL4_Q2, TRUE
	switch VAR_RESULT
	case 0, Route110_TrickHousePuzzle5_EventScript_CorrectAnswer
	goto Route110_TrickHousePuzzle5_EventScript_IncorrectAnswer
	end

Route110_TrickHousePuzzle5_EventScript_Mechadoll4Quiz3::
	msgbox Route110_TrickHousePuzzle5_Text_Mechadoll4Quiz3, MSGBOX_DEFAULT
	multichoice 0, 0, MULTI_MECHADOLL4_Q3, TRUE
	switch VAR_RESULT
	case 1, Route110_TrickHousePuzzle5_EventScript_CorrectAnswer
	goto Route110_TrickHousePuzzle5_EventScript_IncorrectAnswer
	end

Route110_TrickHousePuzzle5_EventScript_Mechadoll5Quiz1::
	msgbox Route110_TrickHousePuzzle5_Text_Mechadoll5Quiz1, MSGBOX_DEFAULT
	multichoice 0, 0, MULTI_MECHADOLL5_Q1, TRUE
	switch VAR_RESULT
	case 1, Route110_TrickHousePuzzle5_EventScript_CorrectAnswer
	goto Route110_TrickHousePuzzle5_EventScript_IncorrectAnswer
	end

Route110_TrickHousePuzzle5_EventScript_Mechadoll5Quiz2::
	msgbox Route110_TrickHousePuzzle5_Text_Mechadoll5Quiz2, MSGBOX_DEFAULT
	multichoice 0, 0, MULTI_MECHADOLL5_Q2, TRUE
	switch VAR_RESULT
	case 0, Route110_TrickHousePuzzle5_EventScript_CorrectAnswer
	goto Route110_TrickHousePuzzle5_EventScript_IncorrectAnswer
	end

Route110_TrickHousePuzzle5_EventScript_Mechadoll5Quiz3::
	msgbox Route110_TrickHousePuzzle5_Text_Mechadoll5Quiz3, MSGBOX_DEFAULT
	multichoice 0, 0, MULTI_MECHADOLL5_Q3, TRUE
	switch VAR_RESULT
	case 2, Route110_TrickHousePuzzle5_EventScript_CorrectAnswer
	goto Route110_TrickHousePuzzle5_EventScript_IncorrectAnswer
	end

Route110_TrickHousePuzzle5_EventScript_IncorrectAnswer::
	waitse
	playse SE_FAILURE
	msgbox Route110_TrickHousePuzzle5_Text_DisappointmentError, MSGBOX_DEFAULT
	applymovement LOCALID_MECHADOLL_1, Route110_TrickHousePuzzle5_Movement_MechadollShake
	applymovement LOCALID_MECHADOLL_2, Route110_TrickHousePuzzle5_Movement_MechadollShake
	applymovement LOCALID_MECHADOLL_3, Route110_TrickHousePuzzle5_Movement_MechadollShake
	applymovement LOCALID_MECHADOLL_4, Route110_TrickHousePuzzle5_Movement_MechadollShake
	applymovement LOCALID_MECHADOLL_5, Route110_TrickHousePuzzle5_Movement_MechadollShake
	msgbox Route110_TrickHousePuzzle5_Text_Wahahahaha, MSGBOX_DEFAULT
	waitmovement 0
	msgbox Route110_TrickHousePuzzle5_Text_WaitForNextChallenge, MSGBOX_DEFAULT
	closemessage
	warp MAP_ROUTE110_TRICK_HOUSE_PUZZLE5, 0, 21
	waitstate
	releaseall
	end

Route110_TrickHousePuzzle5_EventScript_CorrectAnswer::
	waitse
	playse SE_SUCCESS
	goto Route110_TrickHousePuzzle5_EventScript_CorrectGoThrough
	end

Route110_TrickHousePuzzle5_EventScript_CorrectGoThrough::
	msgbox Route110_TrickHousePuzzle5_Text_CorrectGoThrough, MSGBOX_DEFAULT
	releaseall
	end

@ Absurd redundancy in movement scripts that could be resolved by using VAR_TEMP_8 for applymovement instead
@ Many of the below movement scripts arent even used, see below
@   Mechadoll 2 is the only mechadoll to walk right, all the other WalkRight scripts are unused
@   Mechadoll 5 never walks, all the Mechadoll5Walk scripts are unused
@   No mechadoll walks left 5 paces, all the WalkLeft5 scripts are unused
Route110_TrickHousePuzzle5_EventScript_MechadollWalkLeft1::
	call_if_eq VAR_TEMP_8, LOCALID_MECHADOLL_1, Route110_TrickHousePuzzle5_EventScript_Mechadoll1WalkLeft1
	call_if_eq VAR_TEMP_8, LOCALID_MECHADOLL_2, Route110_TrickHousePuzzle5_EventScript_Mechadoll2WalkLeft1
	call_if_eq VAR_TEMP_8, LOCALID_MECHADOLL_3, Route110_TrickHousePuzzle5_EventScript_Mechadoll3WalkLeft1
	call_if_eq VAR_TEMP_8, LOCALID_MECHADOLL_4, Route110_TrickHousePuzzle5_EventScript_Mechadoll4WalkLeft1
	call_if_eq VAR_TEMP_8, LOCALID_MECHADOLL_5, Route110_TrickHousePuzzle5_EventScript_Mechadoll5WalkLeft1
	return

Route110_TrickHousePuzzle5_EventScript_MechadollWalkLeft2::
	call_if_eq VAR_TEMP_8, LOCALID_MECHADOLL_1, Route110_TrickHousePuzzle5_EventScript_Mechadoll1WalkLeft2
	call_if_eq VAR_TEMP_8, LOCALID_MECHADOLL_2, Route110_TrickHousePuzzle5_EventScript_Mechadoll2WalkLeft2
	call_if_eq VAR_TEMP_8, LOCALID_MECHADOLL_3, Route110_TrickHousePuzzle5_EventScript_Mechadoll3WalkLeft2
	call_if_eq VAR_TEMP_8, LOCALID_MECHADOLL_4, Route110_TrickHousePuzzle5_EventScript_Mechadoll4WalkLeft2
	call_if_eq VAR_TEMP_8, LOCALID_MECHADOLL_5, Route110_TrickHousePuzzle5_EventScript_Mechadoll5WalkLeft2
	return

Route110_TrickHousePuzzle5_EventScript_MechadollWalkLeft3::
	call_if_eq VAR_TEMP_8, LOCALID_MECHADOLL_1, Route110_TrickHousePuzzle5_EventScript_Mechadoll1WalkLeft3
	call_if_eq VAR_TEMP_8, LOCALID_MECHADOLL_2, Route110_TrickHousePuzzle5_EventScript_Mechadoll2WalkLeft3
	call_if_eq VAR_TEMP_8, LOCALID_MECHADOLL_3, Route110_TrickHousePuzzle5_EventScript_Mechadoll3WalkLeft3
	call_if_eq VAR_TEMP_8, LOCALID_MECHADOLL_4, Route110_TrickHousePuzzle5_EventScript_Mechadoll4WalkLeft3
	call_if_eq VAR_TEMP_8, LOCALID_MECHADOLL_5, Route110_TrickHousePuzzle5_EventScript_Mechadoll5WalkLeft3
	return

Route110_TrickHousePuzzle5_EventScript_MechadollWalkLeft4::
	call_if_eq VAR_TEMP_8, LOCALID_MECHADOLL_1, Route110_TrickHousePuzzle5_EventScript_Mechadoll1WalkLeft4
	call_if_eq VAR_TEMP_8, LOCALID_MECHADOLL_2, Route110_TrickHousePuzzle5_EventScript_Mechadoll2WalkLeft4
	call_if_eq VAR_TEMP_8, LOCALID_MECHADOLL_3, Route110_TrickHousePuzzle5_EventScript_Mechadoll3WalkLeft4
	call_if_eq VAR_TEMP_8, LOCALID_MECHADOLL_4, Route110_TrickHousePuzzle5_EventScript_Mechadoll4WalkLeft4
	call_if_eq VAR_TEMP_8, LOCALID_MECHADOLL_5, Route110_TrickHousePuzzle5_EventScript_Mechadoll5WalkLeft4
	return

Route110_TrickHousePuzzle5_EventScript_MechadollWalkLeft5::
	call_if_eq VAR_TEMP_8, LOCALID_MECHADOLL_1, Route110_TrickHousePuzzle5_EventScript_Mechadoll1WalkLeft5
	call_if_eq VAR_TEMP_8, LOCALID_MECHADOLL_2, Route110_TrickHousePuzzle5_EventScript_Mechadoll2WalkLeft5
	call_if_eq VAR_TEMP_8, LOCALID_MECHADOLL_3, Route110_TrickHousePuzzle5_EventScript_Mechadoll3WalkLeft5
	call_if_eq VAR_TEMP_8, LOCALID_MECHADOLL_4, Route110_TrickHousePuzzle5_EventScript_Mechadoll4WalkLeft5
	call_if_eq VAR_TEMP_8, LOCALID_MECHADOLL_5, Route110_TrickHousePuzzle5_EventScript_Mechadoll5WalkLeft5
	return

Route110_TrickHousePuzzle5_EventScript_MechadollWalkRight1::
	call_if_eq VAR_TEMP_8, LOCALID_MECHADOLL_1, Route110_TrickHousePuzzle5_EventScript_Mechadoll1WalkRight1
	call_if_eq VAR_TEMP_8, LOCALID_MECHADOLL_2, Route110_TrickHousePuzzle5_EventScript_Mechadoll2WalkRight1
	call_if_eq VAR_TEMP_8, LOCALID_MECHADOLL_3, Route110_TrickHousePuzzle5_EventScript_Mechadoll3WalkRight1
	call_if_eq VAR_TEMP_8, LOCALID_MECHADOLL_4, Route110_TrickHousePuzzle5_EventScript_Mechadoll4WalkRight1
	call_if_eq VAR_TEMP_8, LOCALID_MECHADOLL_5, Route110_TrickHousePuzzle5_EventScript_Mechadoll5WalkRight1
	return

Route110_TrickHousePuzzle5_EventScript_MechadollWalkRight2::
	call_if_eq VAR_TEMP_8, LOCALID_MECHADOLL_1, Route110_TrickHousePuzzle5_EventScript_Mechadoll1WalkRight2
	call_if_eq VAR_TEMP_8, LOCALID_MECHADOLL_2, Route110_TrickHousePuzzle5_EventScript_Mechadoll2WalkRight2
	call_if_eq VAR_TEMP_8, LOCALID_MECHADOLL_3, Route110_TrickHousePuzzle5_EventScript_Mechadoll3WalkRight2
	call_if_eq VAR_TEMP_8, LOCALID_MECHADOLL_4, Route110_TrickHousePuzzle5_EventScript_Mechadoll4WalkRight2
	call_if_eq VAR_TEMP_8, LOCALID_MECHADOLL_5, Route110_TrickHousePuzzle5_EventScript_Mechadoll5WalkRight2
	return

Route110_TrickHousePuzzle5_EventScript_MechadollWalkRight3::
	call_if_eq VAR_TEMP_8, LOCALID_MECHADOLL_1, Route110_TrickHousePuzzle5_EventScript_Mechadoll1WalkRight3
	call_if_eq VAR_TEMP_8, LOCALID_MECHADOLL_2, Route110_TrickHousePuzzle5_EventScript_Mechadoll2WalkRight3
	call_if_eq VAR_TEMP_8, LOCALID_MECHADOLL_3, Route110_TrickHousePuzzle5_EventScript_Mechadoll3WalkRight3
	call_if_eq VAR_TEMP_8, LOCALID_MECHADOLL_4, Route110_TrickHousePuzzle5_EventScript_Mechadoll4WalkRight3
	call_if_eq VAR_TEMP_8, LOCALID_MECHADOLL_5, Route110_TrickHousePuzzle5_EventScript_Mechadoll5WalkRight3
	return

Route110_TrickHousePuzzle5_EventScript_MechadollWalkRight4::
	call_if_eq VAR_TEMP_8, LOCALID_MECHADOLL_1, Route110_TrickHousePuzzle5_EventScript_Mechadoll1WalkRight4
	call_if_eq VAR_TEMP_8, LOCALID_MECHADOLL_2, Route110_TrickHousePuzzle5_EventScript_Mechadoll2WalkRight4
	call_if_eq VAR_TEMP_8, LOCALID_MECHADOLL_3, Route110_TrickHousePuzzle5_EventScript_Mechadoll3WalkRight4
	call_if_eq VAR_TEMP_8, LOCALID_MECHADOLL_4, Route110_TrickHousePuzzle5_EventScript_Mechadoll4WalkRight4
	call_if_eq VAR_TEMP_8, LOCALID_MECHADOLL_5, Route110_TrickHousePuzzle5_EventScript_Mechadoll5WalkRight4
	return

Route110_TrickHousePuzzle5_EventScript_MechadollWalkRight5::
	call_if_eq VAR_TEMP_8, LOCALID_MECHADOLL_1, Route110_TrickHousePuzzle5_EventScript_Mechadoll1WalkRight5
	call_if_eq VAR_TEMP_8, LOCALID_MECHADOLL_2, Route110_TrickHousePuzzle5_EventScript_Mechadoll2WalkRight5
	call_if_eq VAR_TEMP_8, LOCALID_MECHADOLL_3, Route110_TrickHousePuzzle5_EventScript_Mechadoll3WalkRight5
	call_if_eq VAR_TEMP_8, LOCALID_MECHADOLL_4, Route110_TrickHousePuzzle5_EventScript_Mechadoll4WalkRight5
	call_if_eq VAR_TEMP_8, LOCALID_MECHADOLL_5, Route110_TrickHousePuzzle5_EventScript_Mechadoll5WalkRight5
	return

Route110_TrickHousePuzzle5_EventScript_Mechadoll1WalkLeft1::
	applymovement LOCALID_MECHADOLL_1, Route110_TrickHousePuzzle5_Movement_WalkLeft1
	waitmovement 0
	return

Route110_TrickHousePuzzle5_EventScript_Mechadoll2WalkLeft1::
	applymovement LOCALID_MECHADOLL_2, Route110_TrickHousePuzzle5_Movement_WalkLeft1
	waitmovement 0
	return

Route110_TrickHousePuzzle5_EventScript_Mechadoll3WalkLeft1::
	applymovement LOCALID_MECHADOLL_3, Route110_TrickHousePuzzle5_Movement_WalkLeft1
	waitmovement 0
	return

Route110_TrickHousePuzzle5_EventScript_Mechadoll4WalkLeft1::
	applymovement LOCALID_MECHADOLL_4, Route110_TrickHousePuzzle5_Movement_WalkLeft1
	waitmovement 0
	return

Route110_TrickHousePuzzle5_EventScript_Mechadoll5WalkLeft1::
	applymovement LOCALID_MECHADOLL_5, Route110_TrickHousePuzzle5_Movement_WalkLeft1
	waitmovement 0
	return

Route110_TrickHousePuzzle5_EventScript_Mechadoll1WalkLeft2::
	applymovement LOCALID_MECHADOLL_1, Route110_TrickHousePuzzle5_Movement_WalkLeft2
	waitmovement 0
	return

Route110_TrickHousePuzzle5_EventScript_Mechadoll2WalkLeft2::
	applymovement LOCALID_MECHADOLL_2, Route110_TrickHousePuzzle5_Movement_WalkLeft2
	waitmovement 0
	return

Route110_TrickHousePuzzle5_EventScript_Mechadoll3WalkLeft2::
	applymovement LOCALID_MECHADOLL_3, Route110_TrickHousePuzzle5_Movement_WalkLeft2
	waitmovement 0
	return

Route110_TrickHousePuzzle5_EventScript_Mechadoll4WalkLeft2::
	applymovement LOCALID_MECHADOLL_4, Route110_TrickHousePuzzle5_Movement_WalkLeft2
	waitmovement 0
	return

Route110_TrickHousePuzzle5_EventScript_Mechadoll5WalkLeft2::
	applymovement LOCALID_MECHADOLL_5, Route110_TrickHousePuzzle5_Movement_WalkLeft2
	waitmovement 0
	return

Route110_TrickHousePuzzle5_EventScript_Mechadoll1WalkLeft3::
	applymovement LOCALID_MECHADOLL_1, Route110_TrickHousePuzzle5_Movement_WalkLeft3
	waitmovement 0
	return

Route110_TrickHousePuzzle5_EventScript_Mechadoll2WalkLeft3::
	applymovement LOCALID_MECHADOLL_2, Route110_TrickHousePuzzle5_Movement_WalkLeft3
	waitmovement 0
	return

Route110_TrickHousePuzzle5_EventScript_Mechadoll3WalkLeft3::
	applymovement LOCALID_MECHADOLL_3, Route110_TrickHousePuzzle5_Movement_WalkLeft3
	waitmovement 0
	return

Route110_TrickHousePuzzle5_EventScript_Mechadoll4WalkLeft3::
	applymovement LOCALID_MECHADOLL_4, Route110_TrickHousePuzzle5_Movement_WalkLeft3
	waitmovement 0
	return

Route110_TrickHousePuzzle5_EventScript_Mechadoll5WalkLeft3::
	applymovement LOCALID_MECHADOLL_5, Route110_TrickHousePuzzle5_Movement_WalkLeft3
	waitmovement 0
	return

Route110_TrickHousePuzzle5_EventScript_Mechadoll1WalkLeft4::
	applymovement LOCALID_MECHADOLL_1, Route110_TrickHousePuzzle5_Movement_WalkLeft4
	waitmovement 0
	return

Route110_TrickHousePuzzle5_EventScript_Mechadoll2WalkLeft4::
	applymovement LOCALID_MECHADOLL_2, Route110_TrickHousePuzzle5_Movement_WalkLeft4
	waitmovement 0
	return

Route110_TrickHousePuzzle5_EventScript_Mechadoll3WalkLeft4::
	applymovement LOCALID_MECHADOLL_3, Route110_TrickHousePuzzle5_Movement_WalkLeft4
	waitmovement 0
	return

Route110_TrickHousePuzzle5_EventScript_Mechadoll4WalkLeft4::
	applymovement LOCALID_MECHADOLL_4, Route110_TrickHousePuzzle5_Movement_WalkLeft4
	waitmovement 0
	return

Route110_TrickHousePuzzle5_EventScript_Mechadoll5WalkLeft4::
	applymovement LOCALID_MECHADOLL_5, Route110_TrickHousePuzzle5_Movement_WalkLeft4
	waitmovement 0
	return

Route110_TrickHousePuzzle5_EventScript_Mechadoll1WalkLeft5::
	applymovement LOCALID_MECHADOLL_1, Route110_TrickHousePuzzle5_Movement_WalkLeft5
	waitmovement 0
	return

Route110_TrickHousePuzzle5_EventScript_Mechadoll2WalkLeft5::
	applymovement LOCALID_MECHADOLL_2, Route110_TrickHousePuzzle5_Movement_WalkLeft5
	waitmovement 0
	return

Route110_TrickHousePuzzle5_EventScript_Mechadoll3WalkLeft5::
	applymovement LOCALID_MECHADOLL_3, Route110_TrickHousePuzzle5_Movement_WalkLeft5
	waitmovement 0
	return

Route110_TrickHousePuzzle5_EventScript_Mechadoll4WalkLeft5::
	applymovement LOCALID_MECHADOLL_4, Route110_TrickHousePuzzle5_Movement_WalkLeft5
	waitmovement 0
	return

Route110_TrickHousePuzzle5_EventScript_Mechadoll5WalkLeft5::
	applymovement LOCALID_MECHADOLL_5, Route110_TrickHousePuzzle5_Movement_WalkLeft5
	waitmovement 0
	return

Route110_TrickHousePuzzle5_EventScript_Mechadoll1WalkRight1::
	applymovement LOCALID_MECHADOLL_1, Route110_TrickHousePuzzle5_Movement_WalkRight1
	waitmovement 0
	return

Route110_TrickHousePuzzle5_EventScript_Mechadoll2WalkRight1::
	applymovement LOCALID_MECHADOLL_2, Route110_TrickHousePuzzle5_Movement_WalkRight1
	waitmovement 0
	return

Route110_TrickHousePuzzle5_EventScript_Mechadoll3WalkRight1::
	applymovement LOCALID_MECHADOLL_3, Route110_TrickHousePuzzle5_Movement_WalkRight1
	waitmovement 0
	return

Route110_TrickHousePuzzle5_EventScript_Mechadoll4WalkRight1::
	applymovement LOCALID_MECHADOLL_4, Route110_TrickHousePuzzle5_Movement_WalkRight1
	waitmovement 0
	return

Route110_TrickHousePuzzle5_EventScript_Mechadoll5WalkRight1::
	applymovement LOCALID_MECHADOLL_5, Route110_TrickHousePuzzle5_Movement_WalkRight1
	waitmovement 0
	return

Route110_TrickHousePuzzle5_EventScript_Mechadoll1WalkRight2::
	applymovement LOCALID_MECHADOLL_1, Route110_TrickHousePuzzle5_Movement_WalkRight2
	waitmovement 0
	return

Route110_TrickHousePuzzle5_EventScript_Mechadoll2WalkRight2::
	applymovement LOCALID_MECHADOLL_2, Route110_TrickHousePuzzle5_Movement_WalkRight2
	waitmovement 0
	return

Route110_TrickHousePuzzle5_EventScript_Mechadoll3WalkRight2::
	applymovement LOCALID_MECHADOLL_3, Route110_TrickHousePuzzle5_Movement_WalkRight2
	waitmovement 0
	return

Route110_TrickHousePuzzle5_EventScript_Mechadoll4WalkRight2::
	applymovement LOCALID_MECHADOLL_4, Route110_TrickHousePuzzle5_Movement_WalkRight2
	waitmovement 0
	return

Route110_TrickHousePuzzle5_EventScript_Mechadoll5WalkRight2::
	applymovement LOCALID_MECHADOLL_5, Route110_TrickHousePuzzle5_Movement_WalkRight2
	waitmovement 0
	return

Route110_TrickHousePuzzle5_EventScript_Mechadoll1WalkRight3::
	applymovement LOCALID_MECHADOLL_1, Route110_TrickHousePuzzle5_Movement_WalkRight3
	waitmovement 0
	return

Route110_TrickHousePuzzle5_EventScript_Mechadoll2WalkRight3::
	applymovement LOCALID_MECHADOLL_2, Route110_TrickHousePuzzle5_Movement_WalkRight3
	waitmovement 0
	return

Route110_TrickHousePuzzle5_EventScript_Mechadoll3WalkRight3::
	applymovement LOCALID_MECHADOLL_3, Route110_TrickHousePuzzle5_Movement_WalkRight3
	waitmovement 0
	return

Route110_TrickHousePuzzle5_EventScript_Mechadoll4WalkRight3::
	applymovement LOCALID_MECHADOLL_4, Route110_TrickHousePuzzle5_Movement_WalkRight3
	waitmovement 0
	return

Route110_TrickHousePuzzle5_EventScript_Mechadoll5WalkRight3::
	applymovement LOCALID_MECHADOLL_5, Route110_TrickHousePuzzle5_Movement_WalkRight3
	waitmovement 0
	return

Route110_TrickHousePuzzle5_EventScript_Mechadoll1WalkRight4::
	applymovement LOCALID_MECHADOLL_1, Route110_TrickHousePuzzle5_Movement_WalkRight4
	waitmovement 0
	return

Route110_TrickHousePuzzle5_EventScript_Mechadoll2WalkRight4::
	applymovement LOCALID_MECHADOLL_2, Route110_TrickHousePuzzle5_Movement_WalkRight4
	waitmovement 0
	return

Route110_TrickHousePuzzle5_EventScript_Mechadoll3WalkRight4::
	applymovement LOCALID_MECHADOLL_3, Route110_TrickHousePuzzle5_Movement_WalkRight4
	waitmovement 0
	return

Route110_TrickHousePuzzle5_EventScript_Mechadoll4WalkRight4::
	applymovement LOCALID_MECHADOLL_4, Route110_TrickHousePuzzle5_Movement_WalkRight4
	waitmovement 0
	return

Route110_TrickHousePuzzle5_EventScript_Mechadoll5WalkRight4::
	applymovement LOCALID_MECHADOLL_5, Route110_TrickHousePuzzle5_Movement_WalkRight4
	waitmovement 0
	return

Route110_TrickHousePuzzle5_EventScript_Mechadoll1WalkRight5::
	applymovement LOCALID_MECHADOLL_1, Route110_TrickHousePuzzle5_Movement_WalkRight5
	waitmovement 0
	return

Route110_TrickHousePuzzle5_EventScript_Mechadoll2WalkRight5::
	applymovement LOCALID_MECHADOLL_2, Route110_TrickHousePuzzle5_Movement_WalkRight5
	waitmovement 0
	return

Route110_TrickHousePuzzle5_EventScript_Mechadoll3WalkRight5::
	applymovement LOCALID_MECHADOLL_3, Route110_TrickHousePuzzle5_Movement_WalkRight5
	waitmovement 0
	return

Route110_TrickHousePuzzle5_EventScript_Mechadoll4WalkRight5::
	applymovement LOCALID_MECHADOLL_4, Route110_TrickHousePuzzle5_Movement_WalkRight5
	waitmovement 0
	return

Route110_TrickHousePuzzle5_EventScript_Mechadoll5WalkRight5::
	applymovement LOCALID_MECHADOLL_5, Route110_TrickHousePuzzle5_Movement_WalkRight5
	waitmovement 0
	return

Route110_TrickHousePuzzle5_Movement_WalkLeft1:
	walk_left
	step_end

Route110_TrickHousePuzzle5_Movement_WalkLeft2:
	walk_left
	walk_left
	step_end

Route110_TrickHousePuzzle5_Movement_WalkLeft3:
	walk_left
	walk_left
	walk_left
	step_end

Route110_TrickHousePuzzle5_Movement_WalkLeft4:
	walk_left
	walk_left
	walk_left
	walk_left
	step_end

Route110_TrickHousePuzzle5_Movement_WalkLeft5:
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	step_end

Route110_TrickHousePuzzle5_Movement_WalkRight1:
	walk_right
	step_end

Route110_TrickHousePuzzle5_Movement_WalkRight2:
	walk_right
	walk_right
	step_end

Route110_TrickHousePuzzle5_Movement_WalkRight3:
	walk_right
	walk_right
	walk_right
	step_end

Route110_TrickHousePuzzle5_Movement_WalkRight4:
	walk_right
	walk_right
	walk_right
	walk_right
	step_end

Route110_TrickHousePuzzle5_Movement_WalkRight5:
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	step_end

Route110_TrickHousePuzzle5_Movement_MechadollShake:
	face_left
	delay_2
	face_right
	delay_2
	face_left
	delay_2
	face_right
	delay_2
	face_left
	delay_2
	face_right
	delay_2
	face_left
	delay_2
	face_right
	delay_2
	face_left
	delay_2
	face_right
	delay_2
	face_left
	delay_2
	face_right
	delay_2
	face_left
	delay_2
	face_right
	delay_2
	face_left
	delay_2
	face_right
	delay_2
	face_left
	delay_2
	face_right
	delay_2
	face_left
	delay_2
	face_right
	delay_2
	face_left
	delay_2
	face_right
	delay_2
	face_down
	step_end

Route110_TrickHousePuzzle5_Text_WroteSecretCodeLockOpened:
.string "{PLAYER} {252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{116}{0}{0}{244}{6}{1}{252}{25}{39}{0}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{51}{2}{0}{244}{7}{1}{252}{25}{45}{0}{0}{244}{6}{1}{252}{25}{47}{2}{0}{244}{6}{1}{252}{25}{31}{0}{0}{244}{7}{1}\n{252}{25}{41}{0}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{31}{0}{0}{244}{7}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{32}{0}{0}{244}{7}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{7}{0}{0}{244}{5}{1}{252}{25}{210}{1}{0}{244}{7}{1}\p“{252}{25}{13}{0}{0}{244}{6}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{41}{0}{0}{244}{6}{1}{252}{25}{4}{1}{0}{244}{7}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{52}{2}{0}{244}{6}{1}{252}{25}{13}{0}{0}{244}{6}{1}{252}{25}{14}{0}{0}{244}{8}{1}{252}{25}{78}{0}{0}{244}{6}{1}{252}{25}{39}{0}{0}{244}{6}{1}{252}{25}{7}{0}{0}{244}{5}{1}”\n… … … … … … … …\p{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{41}{0}{0}{244}{6}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{32}{0}{0}{244}{7}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{7}{0}{0}{244}{5}{1}{252}{25}{210}{1}{0}{244}{7}{1}{252}{25}{32}{2}{0}{244}{7}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{10}{0}{0}{244}{7}{1}{252}{25}{79}{0}{0}{244}{6}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{106}{1}{0}{244}{6}{1}{252}{25}{42}{0}{0}{244}{6}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{71}{0}{0}{244}{7}{1}{252}{25}{25}{0}{0}{244}{7}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{8}{0}{0}{244}{6}{1}!$"

Route110_TrickHousePuzzle5_Text_Mechadoll1Intro:
.string "{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{8}{0}{0}{244}{6}{1} {252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{8}{0}{0}{244}{6}{1}…\n{252}{25}{29}{2}{0}{244}{8}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{4}{1}{0}{244}{7}{1}{252}{25}{48}{0}{0}{244}{6}{1} MECHADOLL 1!\p{252}{25}{94}{1}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{26}{0}{0}{244}{7}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{31}{0}{0}{244}{7}{1}{252}{25}{113}{1}{0}{244}{11}{1}{252}{25}{27}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{211}{1}{0}{244}{6}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{143}{2}{0}{244}{8}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{46}{0}{0}{244}{7}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{25}{0}{0}{244}{7}{1}\n{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{29}{0}{0}{244}{6}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{13}{0}{0}{244}{6}{1}{252}{25}{7}{0}{0}{244}{5}{1}{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{32}{0}{0}{244}{7}{1}{252}{25}{202}{0}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1} MECHADOLL 5\l{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{106}{1}{0}{244}{6}{1}{252}{25}{42}{0}{0}{244}{6}{1}{252}{25}{13}{0}{0}{244}{6}{1}{252}{25}{7}{0}{0}{244}{5}{1}{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{92}{1}{0}{244}{7}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{51}{2}{0}{244}{7}{1}{252}{25}{45}{0}{0}{244}{6}{1}{252}{25}{47}{2}{0}{244}{6}{1}{252}{25}{31}{0}{0}{244}{7}{1}$"

Route110_TrickHousePuzzle5_Text_Mechadoll1Quiz1:
.string "{252}{25}{113}{1}{0}{244}{11}{1}{252}{25}{27}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{13}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{8}{0}{0}{244}{6}{1} MECHADOLL 1\p{252}{25}{0}{0}{0}{244}{5}{1}{252}{25}{32}{0}{0}{244}{7}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{33}{2}{0}{244}{7}{1}{252}{25}{42}{0}{0}{244}{6}{1}{252}{25}{46}{0}{0}{244}{7}{1}{252}{25}{224}{0}{0}{244}{8}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{4}{0}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{178}{0}{0}{244}{8}{1}\n{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{76}{1}{0}{244}{7}{1}{252}{25}{35}{0}{0}{244}{8}{1}{252}{25}{31}{0}{0}{244}{7}{1}{252}{25}{31}{0}{0}{244}{7}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{108}{1}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{28}{0}{0}{244}{7}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{12}{0}{0}{244}{4}{1} 110 {252}{25}{4}{1}{0}{244}{7}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{33}{2}{0}{244}{7}{1}{252}{25}{42}{0}{0}{244}{6}{1}{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{46}{0}{0}{244}{7}{1}{252}{25}{30}{0}{0}{244}{8}{1}?$"

Route110_TrickHousePuzzle5_Text_Mechadoll1Quiz2:
.string "{252}{25}{113}{1}{0}{244}{11}{1}{252}{25}{27}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{13}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{8}{0}{0}{244}{6}{1} MECHADOLL 1\p{252}{25}{0}{0}{0}{244}{5}{1}{252}{25}{32}{0}{0}{244}{7}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{33}{2}{0}{244}{7}{1}{252}{25}{42}{0}{0}{244}{6}{1}{252}{25}{46}{0}{0}{244}{7}{1}{252}{25}{224}{0}{0}{244}{8}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{4}{0}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{178}{0}{0}{244}{8}{1}\n{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{76}{1}{0}{244}{7}{1}{252}{25}{4}{0}{0}{244}{6}{1}{252}{25}{62}{1}{0}{244}{6}{1}{252}{25}{29}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{149}{1}{0}{244}{7}{1}{252}{25}{97}{2}{0}{244}{11}{1} {252}{25}{4}{1}{0}{244}{7}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{33}{2}{0}{244}{7}{1}{252}{25}{42}{0}{0}{244}{6}{1}{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{46}{0}{0}{244}{7}{1}{252}{25}{30}{0}{0}{244}{8}{1}?$"

Route110_TrickHousePuzzle5_Text_Mechadoll1Quiz3:
.string "{252}{25}{113}{1}{0}{244}{11}{1}{252}{25}{27}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{13}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{8}{0}{0}{244}{6}{1} MECHADOLL 1\p{252}{25}{0}{0}{0}{244}{5}{1}{252}{25}{32}{0}{0}{244}{7}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{33}{2}{0}{244}{7}{1}{252}{25}{42}{0}{0}{244}{6}{1}{252}{25}{46}{0}{0}{244}{7}{1}{252}{25}{224}{0}{0}{244}{8}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{4}{0}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{178}{0}{0}{244}{8}{1}\n{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{76}{1}{0}{244}{7}{1}{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{92}{1}{0}{244}{7}{1}{252}{25}{4}{0}{0}{244}{6}{1}{252}{25}{90}{1}{0}{244}{6}{1} LEECH LIFE {252}{25}{4}{1}{0}{244}{7}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{33}{2}{0}{244}{7}{1}{252}{25}{42}{0}{0}{244}{6}{1}{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{46}{0}{0}{244}{7}{1}{252}{25}{30}{0}{0}{244}{8}{1}?$"

Route110_TrickHousePuzzle5_Text_CorrectGoThrough:
.string "{252}{25}{77}{0}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{123}{0}{0}{244}{7}{1}{252}{25}{92}{1}{0}{244}{7}{1}{252}{25}{42}{0}{0}{244}{6}{1}{252}{25}{39}{0}{0}{244}{6}{1} {252}{25}{113}{1}{0}{244}{11}{1}{252}{25}{26}{0}{0}{244}{7}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{31}{0}{0}{244}{7}{1}{252}{25}{211}{1}{0}{244}{6}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{93}{1}{0}{244}{7}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}\n{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{55}{0}{0}{244}{6}{1}{252}{25}{18}{0}{0}{244}{8}{1}{252}{25}{72}{1}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{32}{0}{0}{244}{7}{1}{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{92}{1}{0}{244}{7}{1}$"

Route110_TrickHousePuzzle5_Text_DisappointmentError:
.string "{252}{25}{31}{0}{0}{244}{7}{1}{252}{25}{16}{0}{0}{244}{7}{1}{252}{25}{16}{0}{0}{244}{7}{1}{252}{25}{16}{0}{0}{244}{7}{1}{252}{25}{138}{2}{0}{244}{7}{1} {252}{25}{72}{0}{0}{244}{6}{1}{252}{25}{25}{0}{0}{244}{7}{1}{252}{25}{46}{0}{0}{244}{7}{1}{252}{25}{48}{2}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}\n{252}{25}{72}{0}{0}{244}{6}{1}{252}{25}{25}{0}{0}{244}{7}{1}{252}{25}{35}{0}{0}{244}{8}{1}{252}{25}{41}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{25}{0}{0}{244}{7}{1}$"

Route110_TrickHousePuzzle5_Text_Wahahahaha:
.string "{252}{25}{42}{0}{0}{244}{6}{1}{252}{25}{7}{0}{0}{244}{5}{1}{252}{25}{182}{2}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{182}{2}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{182}{2}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}! {252}{25}{42}{0}{0}{244}{6}{1}{252}{25}{7}{0}{0}{244}{5}{1}{252}{25}{182}{2}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{182}{2}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{182}{2}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}!\n{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{8}{0}{0}{244}{6}{1} {252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{8}{0}{0}{244}{6}{1}!$"

Route110_TrickHousePuzzle5_Text_WaitForNextChallenge:
.string "{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{13}{0}{0}{244}{6}{1}{252}{25}{7}{0}{0}{244}{5}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{95}{1}{0}{244}{7}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{28}{0}{0}{244}{7}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{39}{0}{0}{244}{6}{1}{252}{25}{10}{0}{0}{244}{7}{1}{252}{25}{93}{2}{0}{244}{7}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{66}{1}{0}{244}{7}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{32}{0}{0}{244}{7}{1}$"

Route110_TrickHousePuzzle5_Text_Mechadoll2Intro:
.string "{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{8}{0}{0}{244}{6}{1} {252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{8}{0}{0}{244}{6}{1}…\n{252}{25}{29}{2}{0}{244}{8}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{4}{1}{0}{244}{7}{1}{252}{25}{48}{0}{0}{244}{6}{1} MECHADOLL 2!\p{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{7}{0}{0}{244}{5}{1}{252}{25}{32}{2}{0}{244}{7}{1}{252}{25}{31}{0}{0}{244}{7}{1}{252}{25}{10}{0}{0}{244}{7}{1}{252}{25}{42}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{39}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{9}{0}{0}{244}{6}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{113}{1}{0}{244}{11}{1}{252}{25}{27}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{38}{0}{0}{244}{7}{1}\nMECHADOLL 1 {252}{25}{132}{1}{0}{244}{11}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{50}{0}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{32}{0}{0}{244}{7}{1}$"

Route110_TrickHousePuzzle5_Text_Mechadoll2Quiz1:
.string "{252}{25}{113}{1}{0}{244}{11}{1}{252}{25}{27}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{13}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{8}{0}{0}{244}{6}{1} MECHADOLL 2\p{252}{25}{0}{0}{0}{244}{5}{1}{252}{25}{32}{0}{0}{244}{7}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{33}{2}{0}{244}{7}{1}{252}{25}{42}{0}{0}{244}{6}{1}{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{46}{0}{0}{244}{7}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{154}{0}{0}{244}{7}{1}{252}{25}{76}{0}{0}{244}{7}{1}{252}{25}{26}{0}{0}{244}{7}{1}{252}{25}{216}{0}{0}{244}{6}{1}{252}{25}{161}{1}{0}{244}{5}{1}\n{252}{25}{20}{1}{0}{244}{6}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{13}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{74}{1}{0}{244}{8}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{9}{0}{0}{244}{6}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{29}{0}{0}{244}{6}{1}{252}{25}{48}{0}{0}{244}{6}{1}?$"

Route110_TrickHousePuzzle5_Text_Mechadoll2Quiz2:
.string "{252}{25}{113}{1}{0}{244}{11}{1}{252}{25}{27}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{13}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{8}{0}{0}{244}{6}{1} MECHADOLL 2\p{252}{25}{0}{0}{0}{244}{5}{1}{252}{25}{32}{0}{0}{244}{7}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{33}{2}{0}{244}{7}{1}{252}{25}{42}{0}{0}{244}{6}{1}{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{46}{0}{0}{244}{7}{1}{252}{25}{30}{0}{0}{244}{8}{1}\n{252}{25}{111}{1}{0}{244}{10}{1}{252}{25}{47}{2}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{79}{1}{0}{244}{6}{1}{252}{25}{26}{0}{0}{244}{7}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{43}{0}{0}{244}{7}{1}.{252}{25}{0}{0}{0}{244}{5}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{25}{0}{0}{244}{7}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{50}{0}{0}{244}{6}{1}?$"

Route110_TrickHousePuzzle5_Text_Mechadoll2Quiz3:
.string "{252}{25}{113}{1}{0}{244}{11}{1}{252}{25}{27}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{13}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{8}{0}{0}{244}{6}{1} MECHADOLL 2\p{252}{25}{126}{0}{0}{244}{7}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{10}{0}{0}{244}{7}{1}{252}{25}{42}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{4}{0}{0}{244}{6}{1}{252}{25}{90}{1}{0}{244}{6}{1}{252}{25}{0}{0}{0}{244}{5}{1}{252}{25}{32}{0}{0}{244}{7}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{33}{2}{0}{244}{7}{1}{252}{25}{42}{0}{0}{244}{6}{1}{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{46}{0}{0}{244}{7}{1}{252}{25}{30}{0}{0}{244}{8}{1}\n{252}{25}{4}{0}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{71}{1}{0}{244}{7}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{0}{0}{0}{244}{5}{1}{252}{25}{28}{0}{0}{244}{7}{1}{252}{25}{42}{0}{0}{244}{6}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{7}{0}{0}{244}{5}{1}?$"

Route110_TrickHousePuzzle5_Text_Mechadoll3Intro:
.string "{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{8}{0}{0}{244}{6}{1} {252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{8}{0}{0}{244}{6}{1}…\n{252}{25}{29}{2}{0}{244}{8}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{4}{1}{0}{244}{7}{1}{252}{25}{48}{0}{0}{244}{6}{1} MECHADOLL 3!\p{252}{25}{29}{2}{0}{244}{8}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{45}{0}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{4}{0}{0}{244}{6}{1}{252}{25}{13}{0}{0}{244}{6}{1}{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{66}{1}{0}{244}{7}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{46}{1}{0}{244}{6}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{129}{2}{0}{244}{5}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{68}{1}{0}{244}{7}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{88}{2}{0}{244}{8}{1}{252}{25}{30}{0}{0}{244}{8}{1}$"

Route110_TrickHousePuzzle5_Text_Mechadoll3Quiz1:
.string "{252}{25}{113}{1}{0}{244}{11}{1}{252}{25}{27}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{13}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{8}{0}{0}{244}{6}{1} MECHADOLL 3\p{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{7}{0}{0}{244}{5}{1}{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{35}{0}{0}{244}{8}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{80}{1}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{24}{2}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}?\nHARBOR MAIL {252}{25}{45}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{153}{2}{0}{244}{7}{1}{252}{25}{30}{0}{0}{244}{8}{1} {252}{25}{46}{0}{0}{244}{7}{1}{252}{25}{21}{1}{0}{244}{6}{1}{252}{25}{48}{0}{0}{244}{6}{1} BURN HEAL {252}{25}{46}{0}{0}{244}{7}{1}{252}{25}{224}{0}{0}{244}{8}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{153}{2}{0}{244}{7}{1}{252}{25}{30}{0}{0}{244}{8}{1}?$"

Route110_TrickHousePuzzle5_Text_Mechadoll3Quiz2:
.string "{252}{25}{113}{1}{0}{244}{11}{1}{252}{25}{27}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{13}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{8}{0}{0}{244}{6}{1} MECHADOLL 3\p{252}{25}{9}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{39}{0}{0}{244}{6}{1} GREAT BALL {252}{25}{46}{0}{0}{244}{7}{1}{252}{25}{224}{0}{0}{244}{8}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{224}{1}{0}{244}{6}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{106}{1}{0}{244}{6}{1}{252}{25}{42}{0}{0}{244}{6}{1}{252}{25}{53}{1}{0}{244}{9}{1}{252}{25}{48}{0}{0}{244}{6}{1}\nPOTION {252}{25}{46}{0}{0}{244}{7}{1}{252}{25}{224}{0}{0}{244}{8}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{9}{0}{0}{244}{6}{1}{252}{25}{42}{0}{0}{244}{6}{1}{252}{25}{25}{0}{0}{244}{7}{1} {252}{25}{13}{0}{0}{244}{6}{1}{252}{25}{7}{0}{0}{244}{5}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{46}{0}{0}{244}{7}{1}{252}{25}{22}{1}{0}{244}{6}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{129}{2}{0}{244}{5}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{68}{1}{0}{244}{7}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{40}{0}{0}{244}{5}{1}?$"

Route110_TrickHousePuzzle5_Text_Mechadoll3Quiz3:
.string "{252}{25}{113}{1}{0}{244}{11}{1}{252}{25}{27}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{13}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{8}{0}{0}{244}{6}{1} MECHADOLL 3\pREPEL {252}{25}{46}{0}{0}{244}{7}{1}{252}{25}{224}{0}{0}{244}{8}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{153}{2}{0}{244}{7}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{24}{2}{0}{244}{6}{1}{252}{25}{31}{0}{0}{244}{7}{1} SODA POP {252}{25}{46}{0}{0}{244}{7}{1}{252}{25}{224}{0}{0}{244}{8}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{9}{0}{0}{244}{6}{1}{252}{25}{42}{0}{0}{244}{6}{1}{252}{25}{25}{0}{0}{244}{7}{1}\n{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{42}{0}{0}{244}{6}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{24}{2}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{35}{0}{0}{244}{8}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{80}{1}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1} SUPER POTION {252}{25}{46}{0}{0}{244}{7}{1}{252}{25}{224}{0}{0}{244}{8}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{9}{0}{0}{244}{6}{1}{252}{25}{42}{0}{0}{244}{6}{1}{252}{25}{25}{0}{0}{244}{7}{1}{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{46}{0}{0}{244}{7}{1}{252}{25}{38}{0}{0}{244}{7}{1}?$"

Route110_TrickHousePuzzle5_Text_Mechadoll4Intro:
.string "{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{8}{0}{0}{244}{6}{1} {252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{8}{0}{0}{244}{6}{1}…\n{252}{25}{29}{2}{0}{244}{8}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{4}{1}{0}{244}{7}{1}{252}{25}{48}{0}{0}{244}{6}{1} MECHADOLL 4!\p{252}{25}{113}{1}{0}{244}{11}{1}{252}{25}{27}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{9}{0}{0}{244}{6}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{29}{2}{0}{244}{8}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{25}{0}{0}{244}{7}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{42}{0}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{180}{2}{0}{244}{7}{1}{252}{25}{41}{0}{0}{244}{6}{1}{252}{25}{16}{2}{0}{244}{7}{1}$"

Route110_TrickHousePuzzle5_Text_Mechadoll4Quiz1:
.string "{252}{25}{113}{1}{0}{244}{11}{1}{252}{25}{27}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{13}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{8}{0}{0}{244}{6}{1} MECHADOLL 4\p{252}{25}{4}{0}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{97}{1}{0}{244}{7}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{78}{0}{0}{244}{6}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{28}{0}{0}{244}{7}{1}{252}{25}{7}{0}{0}{244}{5}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{41}{0}{0}{244}{6}{1}\n{252}{25}{141}{2}{0}{244}{6}{1}{252}{25}{15}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{39}{0}{0}{244}{6}{1}{252}{25}{46}{0}{0}{244}{7}{1}{252}{25}{21}{1}{0}{244}{6}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{141}{2}{0}{244}{6}{1}{252}{25}{46}{0}{0}{244}{7}{1}{252}{25}{58}{0}{0}{244}{8}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{134}{0}{0}{244}{7}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{80}{1}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{24}{2}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}?$"

Route110_TrickHousePuzzle5_Text_Mechadoll4Quiz2:
.string "{252}{25}{113}{1}{0}{244}{11}{1}{252}{25}{27}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{13}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{8}{0}{0}{244}{6}{1} MECHADOLL 4\p{252}{25}{4}{0}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{19}{1}{0}{244}{7}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{158}{1}{0}{244}{8}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{15}{2}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}\n{252}{25}{142}{1}{0}{244}{7}{1}{252}{25}{24}{0}{0}{244}{10}{1}{252}{25}{26}{0}{0}{244}{7}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{46}{0}{0}{244}{7}{1}{252}{25}{21}{1}{0}{244}{6}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{142}{1}{0}{244}{7}{1}{252}{25}{24}{0}{0}{244}{10}{1}{252}{25}{39}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{39}{0}{0}{244}{6}{1}{252}{25}{134}{0}{0}{244}{7}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{80}{1}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{24}{2}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}?$"

Route110_TrickHousePuzzle5_Text_Mechadoll4Quiz3:
.string "{252}{25}{113}{1}{0}{244}{11}{1}{252}{25}{27}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{13}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{8}{0}{0}{244}{6}{1} MECHADOLL 4\p{252}{25}{4}{0}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{0}{0}{0}{244}{5}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{136}{0}{0}{244}{6}{1}{252}{25}{39}{0}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{28}{0}{0}{244}{7}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{18}{2}{0}{244}{5}{1}\n{252}{25}{134}{0}{0}{244}{7}{1}{252}{25}{36}{2}{0}{244}{9}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{136}{0}{0}{244}{6}{1}{252}{25}{39}{0}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{46}{0}{0}{244}{7}{1}{252}{25}{58}{0}{0}{244}{8}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{143}{0}{0}{244}{6}{1}{252}{25}{10}{0}{0}{244}{7}{1}{252}{25}{30}{0}{0}{244}{8}{1}?$"

Route110_TrickHousePuzzle5_Text_Mechadoll5Intro:
.string "{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{8}{0}{0}{244}{6}{1} {252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{8}{0}{0}{244}{6}{1}…\n{252}{25}{29}{2}{0}{244}{8}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{4}{1}{0}{244}{7}{1}{252}{25}{48}{0}{0}{244}{6}{1} MECHADOLL 5!\p{252}{25}{29}{2}{0}{244}{8}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{4}{1}{0}{244}{7}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{33}{0}{0}{244}{6}{1}{252}{25}{41}{0}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{153}{2}{0}{244}{7}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{8}{0}{0}{244}{6}{1}\n{252}{25}{154}{0}{0}{244}{7}{1}{252}{25}{13}{0}{0}{244}{6}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{41}{0}{0}{244}{6}{1}{252}{25}{37}{0}{0}{244}{7}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{10}{0}{0}{244}{7}{1}{252}{25}{220}{1}{0}{244}{7}{1}{252}{25}{76}{0}{0}{244}{7}{1}{252}{25}{4}{0}{0}{244}{6}{1}{252}{25}{13}{0}{0}{244}{6}{1}{252}{25}{154}{0}{0}{244}{7}{1}{252}{25}{164}{1}{0}{244}{6}{1}{252}{25}{25}{0}{0}{244}{7}{1}$"

Route110_TrickHousePuzzle5_Text_Mechadoll5Quiz1:
.string "{252}{25}{113}{1}{0}{244}{11}{1}{252}{25}{27}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{13}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{8}{0}{0}{244}{6}{1} MECHADOLL 5\p{252}{25}{4}{0}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{0}{0}{0}{244}{5}{1}{252}{25}{32}{0}{0}{244}{7}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{36}{0}{0}{244}{8}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{10}{0}{0}{244}{7}{1}{252}{25}{47}{2}{0}{244}{6}{1}{252}{25}{31}{0}{0}{244}{7}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{19}{1}{0}{244}{7}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{10}{0}{0}{244}{7}{1}{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}\n{252}{25}{134}{0}{0}{244}{7}{1}{252}{25}{0}{0}{0}{244}{5}{1}{252}{25}{32}{0}{0}{244}{7}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{248}{1}{0}{244}{6}{1}{252}{25}{143}{0}{0}{244}{6}{1}{252}{25}{33}{2}{0}{244}{7}{1}{252}{25}{42}{0}{0}{244}{6}{1}?$"

Route110_TrickHousePuzzle5_Text_Mechadoll5Quiz2:
.string "{252}{25}{113}{1}{0}{244}{11}{1}{252}{25}{27}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{13}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{8}{0}{0}{244}{6}{1} MECHADOLL 5\p{252}{25}{4}{0}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{19}{1}{0}{244}{7}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{84}{0}{0}{244}{6}{1}{252}{25}{42}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{25}{0}{0}{244}{7}{1}{252}{25}{7}{0}{0}{244}{5}{1}\n{252}{25}{134}{0}{0}{244}{7}{1}{252}{25}{97}{1}{0}{244}{7}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{93}{1}{0}{244}{7}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{103}{1}{0}{244}{7}{1}{252}{25}{143}{0}{0}{244}{6}{1}{252}{25}{46}{0}{0}{244}{7}{1}{252}{25}{47}{2}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}?$"

Route110_TrickHousePuzzle5_Text_Mechadoll5Quiz3:
.string "{252}{25}{113}{1}{0}{244}{11}{1}{252}{25}{27}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{13}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{8}{0}{0}{244}{6}{1} MECHADOLL 5\p{252}{25}{31}{0}{0}{244}{7}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{27}{0}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{28}{2}{0}{244}{6}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{39}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{30}{0}{0}{244}{8}{1}\n{252}{25}{134}{0}{0}{244}{7}{1}{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{26}{0}{0}{244}{7}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{29}{0}{0}{244}{6}{1}{252}{25}{137}{0}{0}{244}{6}{1}{252}{25}{26}{0}{0}{244}{7}{1}{252}{25}{143}{0}{0}{244}{6}{1}{252}{25}{10}{0}{0}{244}{7}{1}{252}{25}{30}{0}{0}{244}{8}{1}?$"
