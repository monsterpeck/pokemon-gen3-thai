SlateportCity_BattleTentCorridor_MapScripts::
	map_script MAP_SCRIPT_ON_FRAME_TABLE, SlateportCity_BattleTentCorridor_OnFrame
	map_script MAP_SCRIPT_ON_WARP_INTO_MAP_TABLE, SlateportCity_BattleTentCorridor_OnWarp
	.byte 0

	@ This is Slateport Tent's version of the Battle Factory Pre-Battle Room

SlateportCity_BattleTentCorridor_OnWarp:
	map_script_2 VAR_TEMP_1, 0, SlateportCity_BattleTentCorridor_EventScript_SetUpObjects
	.2byte 0

SlateportCity_BattleTentCorridor_EventScript_SetUpObjects::
	setvar VAR_TEMP_1, 1
	goto_if_ne VAR_0x8006, 1, SlateportCity_BattleTentCorridor_EventScript_TurnPlayerNorth
	setobjectxy LOCALID_SLATEPORT_TENT_CORRIDOR_ATTENDANT, 2, 2
	turnobject LOCALID_SLATEPORT_TENT_CORRIDOR_ATTENDANT, DIR_SOUTH
SlateportCity_BattleTentCorridor_EventScript_TurnPlayerNorth::
	turnobject LOCALID_PLAYER, DIR_NORTH
	end

SlateportCity_BattleTentCorridor_OnFrame:
	map_script_2 VAR_TEMP_0, 0, SlateportCity_BattleTentCorridor_EventScript_EnterCorridor
	.2byte 0

SlateportCity_BattleTentCorridor_EventScript_EnterCorridor::
	goto_if_eq VAR_0x8006, 1, SlateportCity_BattleTentCorridor_EventScript_ReturnToRoomFromBattle
	setvar VAR_TEMP_0, 1
	applymovement LOCALID_SLATEPORT_TENT_CORRIDOR_ATTENDANT, SlateportCity_BattleTentCorridor_Movement_AttendantEnter
	applymovement LOCALID_PLAYER, SlateportCity_BattleTentCorridor_Movement_PlayerEnter
	waitmovement 0
	goto_if_eq VAR_0x8006, 2, SlateportCity_BattleTentCorridor_EventScript_ResumeChallenge
	slateporttent_generaterentalmons
	slateporttent_generateopponentmons
	msgbox BattleFrontier_BattleFactoryPreBattleRoom_Text_HoldMonsChooseFromSelection, MSGBOX_DEFAULT
	fadescreen FADE_TO_BLACK
	slateporttent_rentmons
	waitstate
SlateportCity_BattleTentCorridor_EventScript_EnterBattleRoom::
	msgbox BattleFrontier_BattleFactoryPreBattleRoom_Text_RightThisWay, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_SLATEPORT_TENT_CORRIDOR_ATTENDANT, Common_Movement_WalkInPlaceFasterUp
	waitmovement 0
	opendoor 2, 1
	waitdooranim
	applymovement LOCALID_SLATEPORT_TENT_CORRIDOR_ATTENDANT, SlateportCity_BattleTentCorridor_Movement_AttendantExit
	applymovement LOCALID_PLAYER, SlateportCity_BattleTentCorridor_Movement_PlayerExit
	waitmovement 0
	closedoor 2, 1
	waitdooranim
	warp MAP_SLATEPORT_CITY_BATTLE_TENT_BATTLE_ROOM, 4, 4
	waitstate
	end

SlateportCity_BattleTentCorridor_EventScript_ReturnToRoomFromBattle::
	factory_setopponentmons
	factory_resethelditems
	msgbox BattleFrontier_BattleFactoryPreBattleRoom_Text_LetUsRestoreMons, MSGBOX_DEFAULT
	playfanfare MUS_HEAL
	waitfanfare
	special HealPlayerParty
SlateportCity_BattleTentCorridor_EventScript_AskReadyForOpponent::
	frontier_get FRONTIER_DATA_BATTLE_NUM
	call_if_eq VAR_RESULT, 1, SlateportCity_BattleTentCorridor_EventScript_ReadyFor2ndOpponent
	call_if_eq VAR_RESULT, 2, SlateportCity_BattleTentCorridor_EventScript_ReadyFor3rdOpponent
	multichoice 20, 6, MULTI_GO_ON_REST_RETIRE, TRUE
	switch VAR_RESULT
	case 0, SlateportCity_BattleTentCorridor_EventScript_AskSwapMon
	case 1, SlateportCity_BattleTentCorridor_EventScript_AskPauseChallenge
	case 2, SlateportCity_BattleTentCorridor_EventScript_AskRetireChallenge

SlateportCity_BattleTentCorridor_EventScript_AskPauseChallenge::
	msgbox BattleFrontier_BattleFactoryPreBattleRoom_Text_SaveAndQuitGame, MSGBOX_YESNO
	switch VAR_RESULT
	case NO, SlateportCity_BattleTentCorridor_EventScript_AskReadyForOpponent
	case YES, SlateportCity_BattleTentCorridor_EventScript_PauseChallenge
	case MULTI_B_PRESSED, SlateportCity_BattleTentCorridor_EventScript_AskReadyForOpponent

SlateportCity_BattleTentCorridor_EventScript_AskRetireChallenge::
	message BattleFrontier_BattleFactoryPreBattleRoom_Text_RetireFromChallenge
	waitmessage
	multichoicedefault 20, 8, MULTI_YESNO, 1, FALSE
	switch VAR_RESULT
	case 1, SlateportCity_BattleTentCorridor_EventScript_AskReadyForOpponent
	case 0, SlateportCity_BattleTent_EventScript_WarpToLobbyLost
	case MULTI_B_PRESSED, SlateportCity_BattleTentCorridor_EventScript_AskReadyForOpponent

SlateportCity_BattleTentCorridor_EventScript_AskSwapMon::
	slateporttent_generateopponentmons
	msgbox BattleFrontier_BattleFactoryPreBattleRoom_Text_LikeToSwapMon, MSGBOX_YESNO
	switch VAR_RESULT
	case NO, SlateportCity_BattleTentCorridor_EventScript_EnterBattleRoom
	case YES, SlateportCity_BattleTentCorridor_EventScript_SwapMons
	case MULTI_B_PRESSED, SlateportCity_BattleTentCorridor_EventScript_EnterBattleRoom

SlateportCity_BattleTentCorridor_EventScript_SwapMons::
	fadescreen FADE_TO_BLACK
	slateporttent_swapmons
	waitstate
	goto_if_eq VAR_RESULT, 1, SlateportCity_BattleTentCorridor_EventScript_EnterBattleRoom
	msgbox BattleFrontier_BattleFactoryPreBattleRoom_Text_YourSwapIsComplete, MSGBOX_DEFAULT
	goto SlateportCity_BattleTentCorridor_EventScript_EnterBattleRoom

SlateportCity_BattleTentCorridor_EventScript_ReadyFor2ndOpponent::
	message BattleFrontier_BattleFactoryPreBattleRoom_Text_ReadyFor2ndOpponent
	waitmessage
	return

SlateportCity_BattleTentCorridor_EventScript_ReadyFor3rdOpponent::
	message BattleFrontier_BattleFactoryPreBattleRoom_Text_ReadyFor3rdOpponent
	waitmessage
	return

SlateportCity_BattleTentCorridor_EventScript_PauseChallenge::
	message BattleFrontier_BattleFactoryPreBattleRoom_Text_SavingDataPleaseWait
	waitmessage
	slateporttent_save CHALLENGE_STATUS_PAUSED
	playse SE_SAVE
	waitse
	fadescreen FADE_TO_BLACK
	frontier_reset
	end

SlateportCity_BattleTentCorridor_EventScript_ResumeChallenge::
	special SavePlayerParty
	factory_setparties 0
	goto SlateportCity_BattleTentCorridor_EventScript_AskReadyForOpponent

SlateportCity_BattleTentCorridor_Movement_PlayerEnter:
	walk_up
	walk_up
	walk_up
	walk_up
	step_end

SlateportCity_BattleTentCorridor_Movement_PlayerExit:
	walk_up
	walk_up
	set_invisible
	step_end

SlateportCity_BattleTentCorridor_Movement_AttendantEnter:
	walk_up
	walk_up
	walk_up
	walk_up
	walk_in_place_faster_down
	step_end

SlateportCity_BattleTentCorridor_Movement_AttendantExit:
	walk_up
	set_invisible
	step_end

@ Leftover text from when this was a Contest Hall in R/S
@ Unused
SlateportCity_ContestHall_Text_AdviceForContests:
.string "อยากได้คำแนะนำดี ๆ\nเรื่องคอนเทสต์ไหม?\pถ้าใช้ท่าบางท่าต่อจาก\nท่าบางประเภท บางครั้งก็จะ\lเรียกความสนใจเพิ่มได้\pถ้ารู้จังหวะดี\nก็ทำคะแนนเสน่ห์ได้สูงเลย\pแน่นอนว่าคู่แข่งอาจพยายาม\nขัดขวางการแสดงของโปเกมอนคุณ$"

@ Unused
SlateportCity_ContestHall_Text_MyPapaIsContestJudge:
.string "พ่อฉันเป็นกรรมการคอนเทสต์\pโตขึ้นฉันจะเป็นอะไรดีนะ\nกรรมการหรือยิมลีดเดอร์?$"

@ Unused
SlateportCity_ContestHall_Text_ImLikeMajorlyCheesed:
.string "เฮ้ ฉันนี่แบบว่าเซ็งสุด ๆ\nรู้ไหม แบบว่า ฉันก็แค่\lอยากรู้ว่าทำไมโปเกมอนของฉัน\lไม่เคยชนะเลย แบบว่า เข้าใจปะ?\pฉันก็เลยไปบอกกรรมการ\nว่าฉันคิดยังไง แบบว่าฟรี ๆ เลยนะ\pแต่เขาไม่ยอมฟังฉันเลย เฮ้!\nแบบว่า เซ็งสุด ๆ เลย!\pเฮ้ เธอน่ะ! เงียบไปเลย รู้ไหม?\nเอ้านี่ รับไปซะ!$"

@ Unused
SlateportCity_ContestHall_Text_ExplainTorment:
.string "นั่นมัน TM41 ไง รู้ไหม?\nเฮ้ มันคือ TORMENT ได้ยินไหม?\pแบบว่า มันจะทำให้อีกฝ่าย\nใช้ท่าเดิมติดกันสองครั้งไม่ได้ เข้าใจไหม?\pเฮ้ ฟังให้ดีนะ แบบว่า\nฉันไม่ได้ใช้ TORMENT ใส่เธอหรอก!$"

@ Unused
SlateportCity_ContestHall_Text_MCStepUpTakePartInContest:
.string "พิธีกร: โอ้โห!\nโปเกมอนตัวนั้นดูดีไม่เบาเลยนะ?\pเชิญ! ก้าวเข้ามาแล้ว\nร่วมคอนเทสต์สุดวิเศษของเราเลย!\pคุณต้องทำได้ดีแน่! ฉันมั่นใจ!\nสายตาฉันไม่เคยพลาด!$"

@ Unused
SlateportCity_ContestHall_Text_JudgeWouldntDoToMissContest:
.string "กรรมการ: สวัสดี!\nดูแล้วคุณเป็นเทรนเนอร์สินะ!\pถ้าอย่างนั้น จะพลาด\nโปเกมอนคอนเทสต์ไปได้ยังไง!\pไปรับ CONTEST PASS ที่เมืองชิดาเกะ\nแล้วจะเข้าร่วมเมื่อไรก็ได้!$"

@ Unused
SlateportCity_ContestHall_Text_ItsAppealTime:
.string "ถึงเวลาอวดเสน่ห์แล้ว!\nจะเริ่มด้วยท่าไหนดีนะ?$"

@ Unused
SlateportCity_ContestHall_Text_DidntPayAttentionToAppeal:
.string "พวกเขาแทบไม่สนใจ\nการอวดเสน่ห์ของโปเกมอนฉันเลย…\pฮึ่ม กรรมการคนนั้น\nของดีอยู่ตรงหน้าก็ยังดูไม่ออก$"

@ Unused
SlateportCity_ContestHall_Text_RewardWithSageAdvice:
.string "โอ้ สวัสดี! มาดูใกล้ขนาดนี้\nต้องเป็นแฟนตัวยงแน่ ๆ\pเพื่อเป็นรางวัลให้ความกระตือรือร้น\nฉันจะให้คำแนะนำดี ๆ\pถ้าท่าไหนได้รับเสียงตอบรับดีมาก\nผู้ชมจะยิ่งตื่นเต้น\pโปเกมอนที่อวดเสน่ห์\nตอนที่ทุกคนกำลังตื่นเต้นสุด ๆ…\pอืม ยังไงก็ต้องมีเรื่องดี ๆ\nเกิดขึ้นแน่นอน!$"

@ Unused
SlateportCity_ContestHall_Text_MoreFreakedOutThanMon:
.string "ฉันทำไม่ได้! ฉันตื่นเต้น\nยิ่งกว่าโปเกมอนของตัวเองอีก\pทั้งตัวสั่น หัวใจก็เต้นไม่หยุด!$"

@ Unused
SlateportCity_ContestHall_Text_BattleAndContestAlike:
.string "การต่อสู้กับคอนเทสต์\nไม่เหมือนกัน แต่ก็คล้ายกันด้วย\pต้องพยายามให้เต็มที่และเชื่อมั่น\nในโปเกมอนที่คุณเลี้ยงมา$"

@ Unused
SlateportCity_ContestHall_Text_MonLooksOnTopOfGame:
.string "โปเกมอนตัวนั้นดูพร้อมเต็มที่\nเลยนะ?\pโปเกมอนที่ทำได้ดีใน\nการตัดสินรอบสอง ดูเหมือนจะ\lผ่อนคลายขึ้นตอนอวดเสน่ห์$"

@ Unused
SlateportCity_ContestHall_Text_MyMonBetterThanThatLot:
.string "ดูสภาพน่าเวทนานั่นสิ?\pฮึ โปเกมอนของฉันเก่งกว่า\nพวกนั้นแน่นอน!$"

@ Unused
SlateportCity_ContestHall_Text_GetUrgeToMoveWithMon:
.string "เวลาโปเกมอนกำลังอวดเสน่ห์\nอย่างมีพลัง คุณไม่รู้สึกอยาก\lขยับตามพวกมันบ้างเหรอ?$"

@ Unused
SlateportCity_ContestHall_Text_HyperRankStage:
.string "โปเกมอนคอนเทสต์\nเวทีระดับไฮเปอร์!$"

