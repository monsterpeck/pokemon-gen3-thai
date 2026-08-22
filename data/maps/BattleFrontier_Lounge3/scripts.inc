BattleFrontier_Lounge3_MapScripts::
	.byte 0

	.set BET_AMOUNT_5,  5
	.set BET_AMOUNT_10, 10
	.set BET_AMOUNT_15, 15

BattleFrontier_Lounge3_EventScript_Gambler::
	lock
	faceplayer
	goto_if_set FLAG_MET_BATTLE_FRONTIER_GAMBLER, BattleFrontier_Lounge3_EventScript_AlreadyMetGambler
	call BattleFrontier_Lounge3_EventScript_CountSilverSymbols
	goto_if_le VAR_0x8004, 2, BattleFrontier_Lounge3_EventScript_NotEnoughSilverSymbols
	setflag FLAG_MET_BATTLE_FRONTIER_GAMBLER
	msgbox BattleFrontier_Lounge3_Text_YouLookToughExplainGambling, MSGBOX_DEFAULT
	goto BattleFrontier_Lounge3_EventScript_AskToEnterChallenge
	end

BattleFrontier_Lounge3_EventScript_AskToEnterChallenge::
	special ShowFrontierGamblerLookingMessage
	waitmessage
	waitbuttonpress
	msgbox BattleFrontier_Lounge3_Text_HowAboutEnteringEventForMe, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, BattleFrontier_Lounge3_EventScript_DeclineChallenge
	msgbox BattleFrontier_Lounge3_Text_SpotMeSomeBattlePoints, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, BattleFrontier_Lounge3_EventScript_DeclineChallenge
	message BattleFrontier_Lounge3_Text_HowMuchCanYouSpot
	waitmessage
	special ShowBattlePointsWindow
	goto BattleFrontier_Lounge3_EventScript_ChooseBetAmount
	end

BattleFrontier_Lounge3_EventScript_ChooseBetAmount::
	multichoice 20, 4, MULTI_FRONTIER_GAMBLER_BET, FALSE
	copyvar VAR_FRONTIER_GAMBLER_AMOUNT_BET, VAR_RESULT
	switch VAR_RESULT
	case FRONTIER_GAMBLER_BET_5, BattleFrontier_Lounge3_EventScript_Bet5
	case FRONTIER_GAMBLER_BET_10, BattleFrontier_Lounge3_EventScript_Bet10
	case FRONTIER_GAMBLER_BET_15, BattleFrontier_Lounge3_EventScript_Bet15
	case FRONTIER_GAMBLER_BET_CANCEL, BattleFrontier_Lounge3_EventScript_CancelBet
	case MULTI_B_PRESSED, BattleFrontier_Lounge3_EventScript_CancelBet
	end

BattleFrontier_Lounge3_EventScript_Bet5::
	setvar VAR_0x8008, BET_AMOUNT_5
	goto BattleFrontier_Lounge3_EventScript_TryPlaceBet
	end

BattleFrontier_Lounge3_EventScript_Bet10::
	setvar VAR_0x8008, BET_AMOUNT_10
	goto BattleFrontier_Lounge3_EventScript_TryPlaceBet
	end

BattleFrontier_Lounge3_EventScript_Bet15::
	setvar VAR_0x8008, BET_AMOUNT_15
	goto BattleFrontier_Lounge3_EventScript_TryPlaceBet
	end

BattleFrontier_Lounge3_EventScript_TryPlaceBet::
	specialvar VAR_TEMP_1, GetFrontierBattlePoints
	goto_if_ge VAR_TEMP_1, VAR_0x8008, BattleFrontier_Lounge3_EventScript_PlaceBet
	msgbox BattleFrontier_Lounge3_Text_YouDontHaveEnoughPoints, MSGBOX_DEFAULT
	message BattleFrontier_Lounge3_Text_HowMuchCanYouSpot
	waitmessage
	goto BattleFrontier_Lounge3_EventScript_ChooseBetAmount
	end

BattleFrontier_Lounge3_EventScript_PlaceBet::
	copyvar VAR_0x8004, VAR_0x8008
	special TakeFrontierBattlePoints
	setvar VAR_FRONTIER_GAMBLER_STATE, FRONTIER_GAMBLER_PLACED_BET
	special UpdateBattlePointsWindow
	playse SE_SHOP
	msgbox BattleFrontier_Lounge3_Text_ThanksOffYouGo, MSGBOX_DEFAULT
	goto BattleFrontier_Lounge3_EventScript_FinishBet
	end

BattleFrontier_Lounge3_EventScript_FinishBet::
	special ShowFrontierGamblerGoMessage
	waitmessage
	waitbuttonpress
	special CloseBattlePointsWindow
	release
	end

BattleFrontier_Lounge3_EventScript_CountSilverSymbols::
	setvar VAR_0x8004, 0
	call_if_set FLAG_SYS_TOWER_SILVER, BattleFrontier_Lounge3_EventScript_AddSilverSymbolCount
	call_if_set FLAG_SYS_DOME_SILVER, BattleFrontier_Lounge3_EventScript_AddSilverSymbolCount
	call_if_set FLAG_SYS_PALACE_SILVER, BattleFrontier_Lounge3_EventScript_AddSilverSymbolCount
	call_if_set FLAG_SYS_ARENA_SILVER, BattleFrontier_Lounge3_EventScript_AddSilverSymbolCount
	call_if_set FLAG_SYS_FACTORY_SILVER, BattleFrontier_Lounge3_EventScript_AddSilverSymbolCount
	call_if_set FLAG_SYS_PIKE_SILVER, BattleFrontier_Lounge3_EventScript_AddSilverSymbolCount
	call_if_set FLAG_SYS_PYRAMID_SILVER, BattleFrontier_Lounge3_EventScript_AddSilverSymbolCount
	return

BattleFrontier_Lounge3_EventScript_AddSilverSymbolCount::
	addvar VAR_0x8004, 1
	return

BattleFrontier_Lounge3_EventScript_NotEnoughSilverSymbols::
	msgbox BattleFrontier_Lounge3_Text_CantYouSeeWereBusyHere, MSGBOX_DEFAULT
	goto BattleFrontier_Lounge3_EventScript_FaceOriginalDirection
	end

BattleFrontier_Lounge3_EventScript_AlreadyMetGambler::
	msgbox BattleFrontier_Lounge3_Text_Oh, MSGBOX_DEFAULT
	goto_if_ge VAR_FRONTIER_GAMBLER_STATE, FRONTIER_GAMBLER_PLACED_BET, BattleFrontier_Lounge3_EventScript_CheckBetResults
	goto BattleFrontier_Lounge3_EventScript_AskToEnterChallenge
	end

BattleFrontier_Lounge3_EventScript_CheckBetResults::
	goto_if_eq VAR_FRONTIER_GAMBLER_STATE, FRONTIER_GAMBLER_PLACED_BET, BattleFrontier_Lounge3_EventScript_ChallengeNotAttempted
	goto_if_eq VAR_FRONTIER_GAMBLER_STATE, FRONTIER_GAMBLER_WON, BattleFrontier_Lounge3_EventScript_WonChallenge
	goto BattleFrontier_Lounge3_EventScript_LostChallenge
	end

BattleFrontier_Lounge3_EventScript_WonChallenge::
	msgbox BattleFrontier_Lounge3_Text_HelloChampHeresYourPoints, MSGBOX_DEFAULT
	call_if_eq VAR_FRONTIER_GAMBLER_AMOUNT_BET, FRONTIER_GAMBLER_BET_5, BattleFrontier_Lounge3_EventScript_RewardBet5
	call_if_eq VAR_FRONTIER_GAMBLER_AMOUNT_BET, FRONTIER_GAMBLER_BET_10, BattleFrontier_Lounge3_EventScript_RewardBet10
	call_if_eq VAR_FRONTIER_GAMBLER_AMOUNT_BET, FRONTIER_GAMBLER_BET_15, BattleFrontier_Lounge3_EventScript_RewardBet15
	msgbox BattleFrontier_Lounge3_Text_ObtainedBattlePoints, MSGBOX_GETPOINTS
	special GiveFrontierBattlePoints
	msgbox BattleFrontier_Lounge3_Text_ThinkOfMeForAnotherChallenge, MSGBOX_DEFAULT
	setvar VAR_FRONTIER_GAMBLER_STATE, FRONTIER_GAMBLER_WAITING
	release
	end

BattleFrontier_Lounge3_EventScript_LostChallenge::
	msgbox BattleFrontier_Lounge3_Text_NiceTryCantReturnPoints, MSGBOX_DEFAULT
	setvar VAR_FRONTIER_GAMBLER_STATE, FRONTIER_GAMBLER_WAITING
	release
	end

BattleFrontier_Lounge3_EventScript_RewardBet5::
	buffernumberstring STR_VAR_1, (BET_AMOUNT_5 * 2)
	setvar VAR_0x8004, (BET_AMOUNT_5 * 2)
	return

BattleFrontier_Lounge3_EventScript_RewardBet10::
	buffernumberstring STR_VAR_1, (BET_AMOUNT_10 * 2)
	setvar VAR_0x8004, (BET_AMOUNT_10 * 2)
	return

BattleFrontier_Lounge3_EventScript_RewardBet15::
	buffernumberstring STR_VAR_1, (BET_AMOUNT_15 * 2)
	setvar VAR_0x8004, (BET_AMOUNT_15 * 2)
	return

BattleFrontier_Lounge3_EventScript_ChallengeNotAttempted::
	special ShowFrontierGamblerGoMessage
	waitmessage
	waitbuttonpress
	release
	end

BattleFrontier_Lounge3_EventScript_DeclineChallenge::
	msgbox BattleFrontier_Lounge3_Text_NotInterested, MSGBOX_DEFAULT
	release
	end

BattleFrontier_Lounge3_EventScript_CancelBet::
	special CloseBattlePointsWindow
	goto BattleFrontier_Lounge3_EventScript_DeclineChallenge
	end

BattleFrontier_Lounge3_EventScript_Man::
	msgbox BattleFrontier_Lounge3_Text_ShouldBeTakingChallenges, MSGBOX_NPC
	end

BattleFrontier_Lounge3_EventScript_Woman::
	lock
	faceplayer
	msgbox BattleFrontier_Lounge3_Text_BackedWrongTrainer, MSGBOX_DEFAULT
	goto BattleFrontier_Lounge3_EventScript_FaceOriginalDirection
	end

BattleFrontier_Lounge3_EventScript_PokefanF::
	lock
	faceplayer
	msgbox BattleFrontier_Lounge3_Text_KnowWinnerWhenISeeOne, MSGBOX_DEFAULT
	goto BattleFrontier_Lounge3_EventScript_FaceOriginalDirection
	end

BattleFrontier_Lounge3_EventScript_FatMan::
	lock
	faceplayer
	msgbox BattleFrontier_Lounge3_Text_TrainerGoodButRattled, MSGBOX_DEFAULT
	goto BattleFrontier_Lounge3_EventScript_FaceOriginalDirection
	end

BattleFrontier_Lounge3_EventScript_FaceOriginalDirection::
	closemessage
	applymovement VAR_LAST_TALKED, Common_Movement_FaceOriginalDirection
	waitmovement 0
	release
	end

BattleFrontier_Lounge3_Text_CantYouSeeWereBusyHere::
.string "…มีอะไรล่ะ?\pไม่เห็นหรือว่าเรากำลังยุ่งกันอยู่?\nธุระของเธอไว้ทีหลังไม่ได้รึ?$"

BattleFrontier_Lounge3_Text_YouLookToughExplainGambling::
.string "…หืม?\nดูแล้วเธอน่าจะเป็นเทรนเนอร์ฝีมือดี.\pหึหึ…\nฟังข้อเสนอของฉันหน่อยสิ.\pพวกเรารวมกลุ่มกันเล่นเกมเล็ก ๆ\nเกี่ยวกับสิ่งที่เกิดขึ้นใน\lแบทเทิลฟรอนเทียร์.\pกติกาง่ายมาก.\pก่อนอื่น เราจะเลือกสถานที่หนึ่ง\nในแบทเทิลฟรอนเทียร์.\pจากนั้นแต่ละคนเลือกเทรนเนอร์คนละคน\nที่กำลังท้าสถานที่นั้นอยู่\lแล้วเดิมพันด้วยแบทเทิลพอยต์.\pคนที่เลือกเทรนเนอร์ซึ่งทำสถิติได้ดีที่สุด\nจะได้แบทเทิลพอยต์ทั้งหมด\lในกองเดิมพันไป.\pง่ายดีใช่ไหม?\nเอาล่ะ…$"

BattleFrontier_Lounge3_Text_ChallengeBattleTowerSingle::
.string "ฉันกำลังหาเทรนเนอร์ที่จะไปท้า\nห้องซิงเกิลแบทเทิลของ\lแบทเทิลทาวเวอร์.\pแต่จนถึงตอนนี้ยังไม่เห็นเทรนเนอร์\nที่ดูมีแววชนะเลย.$"

BattleFrontier_Lounge3_Text_ChallengeBattleTowerDouble::
.string "ฉันกำลังหาเทรนเนอร์ที่จะไปท้า\nห้องดับเบิลแบทเทิลของ\lแบทเทิลทาวเวอร์.\pแต่จนถึงตอนนี้ยังไม่เห็นเทรนเนอร์\nที่ดูมีแววชนะเลย.$"

BattleFrontier_Lounge3_Text_ChallengeBattleTowerMulti::
.string "ฉันกำลังหาเทรนเนอร์ที่จะไปท้า\nห้องมัลติแบทเทิลของ\lแบทเทิลทาวเวอร์.\pแต่จนถึงตอนนี้ยังไม่เห็นเทรนเนอร์\nที่ดูมีแววชนะเลย.$"

BattleFrontier_Lounge3_Text_ChallengeBattleDomeSingle::
.string "ฉันกำลังหาเทรนเนอร์ที่จะเข้า\nทัวร์นาเมนต์ซิงเกิลแบทเทิลของ\lแบทเทิลโดม.\pแต่จนถึงตอนนี้ยังไม่เห็นเทรนเนอร์\nที่ดูมีแววชนะเลย.$"

BattleFrontier_Lounge3_Text_ChallengeBattleDomeDouble::
.string "ฉันกำลังหาเทรนเนอร์ที่จะเข้า\nทัวร์นาเมนต์ดับเบิลแบทเทิลของ\lแบทเทิลโดม.\pแต่จนถึงตอนนี้ยังไม่เห็นเทรนเนอร์\nที่ดูมีแววชนะเลย.$"

BattleFrontier_Lounge3_Text_ChallengeBattleFactorySingle::
.string "ฉันกำลังหาเทรนเนอร์ที่จะเข้า\nแบทเทิลสวอปซิงเกิลทัวร์นาเมนต์ของ\lแบทเทิลแฟกทอรี.\pแต่จนถึงตอนนี้ยังไม่เห็นเทรนเนอร์\nที่ดูมีแววชนะเลย.$"

BattleFrontier_Lounge3_Text_ChallengeBattleFactoryDouble::
.string "ฉันกำลังหาเทรนเนอร์ที่จะเข้า\nแบทเทิลสวอปดับเบิลทัวร์นาเมนต์ของ\lแบทเทิลแฟกทอรี.\pแต่จนถึงตอนนี้ยังไม่เห็นเทรนเนอร์\nที่ดูมีแววชนะเลย.$"

BattleFrontier_Lounge3_Text_ChallengeBattlePalaceSingle::
.string "ฉันกำลังหาเทรนเนอร์ที่จะไปท้า\nฮอลล์ซิงเกิลแบทเทิลของ\lแบทเทิลพาเลซ.\pแต่จนถึงตอนนี้ยังไม่เห็นเทรนเนอร์\nที่ดูมีแววชนะเลย.$"

BattleFrontier_Lounge3_Text_ChallengeBattlePalaceDouble::
.string "ฉันกำลังหาเทรนเนอร์ที่จะไปท้า\nฮอลล์ดับเบิลแบทเทิลของ\lแบทเทิลพาเลซ.\pแต่จนถึงตอนนี้ยังไม่เห็นเทรนเนอร์\nที่ดูมีแววชนะเลย.$"

BattleFrontier_Lounge3_Text_ChallengeBattleArena::
.string "ฉันกำลังหาเทรนเนอร์ที่จะเข้า\nเซ็ต KO ทัวร์นาเมนต์ของ\lแบทเทิลอารีนา.\pแต่จนถึงตอนนี้ยังไม่เห็นเทรนเนอร์\nที่ดูมีแววชนะเลย.$"

BattleFrontier_Lounge3_Text_ChallengeBattlePike::
.string "ฉันกำลังหาเทรนเนอร์ที่จะเข้า\nแบทเทิลไพค์\lในแบทเทิลชอยซ์.\pแต่จนถึงตอนนี้ยังไม่เห็นเทรนเนอร์\nที่ดูมีแววชนะเลย.$"

BattleFrontier_Lounge3_Text_ChallengeBattlePyramid::
.string "ฉันกำลังหาเทรนเนอร์ที่จะเข้า\nแบทเทิลเควสต์ของ\lแบทเทิลพีระมิด.\pแต่จนถึงตอนนี้ยังไม่เห็นเทรนเนอร์\nที่ดูมีแววชนะเลย.$"

BattleFrontier_Lounge3_Text_HowAboutEnteringEventForMe::
.string "ฉันจะให้เธอได้ประโยชน์ด้วยแน่นอน.\nว่าไงล่ะ?\lช่วยลงแข่งรายการนั้นให้ฉันหน่อยไหม?$"

BattleFrontier_Lounge3_Text_SpotMeSomeBattlePoints::
.string "ดีเลย เยี่ยมมาก.\nงั้น เอ่อ… ช่วยออกแบทเทิลพอยต์\lของเธอให้ฉันหน่อยได้ไหม?\pเชื่อฉันเถอะ หลังจากนั้น\nฉันจะตอบแทนเธอแน่นอน.$"

BattleFrontier_Lounge3_Text_HowMuchCanYouSpot::
.string "เยี่ยม เยี่ยม!\nแล้วจะออกให้ฉันเท่าไร?$"

BattleFrontier_Lounge3_Text_YouDontHaveEnoughPoints::
.string "โอ้ ไม่ ไม่ ไม่!\nแบทเทิลพอยต์ของเธอไม่พอ!\pอย่ามาเล่นอะไรไร้สาระ\nให้ทุกคนเสียเวลาสิ!$"

BattleFrontier_Lounge3_Text_ThanksOffYouGo::
.string "หึหึ! ขอบใจมาก!\nเอาล่ะ ไปได้แล้ว!$"

BattleFrontier_Lounge3_Text_GetToBattleTowerSingle::
.string "รีบไปห้องซิงเกิลแบทเทิล\nของแบทเทิลทาวเวอร์ทันที!\pงานนี้ต้องชนะเท่านั้น!\nอย่าทำโอกาสหลุดมือล่ะ!\lอนาคตของเราสองคนขึ้นอยู่กับเธอ!$"

BattleFrontier_Lounge3_Text_GetToBattleTowerDouble::
.string "รีบไปห้องดับเบิลแบทเทิล\nของแบทเทิลทาวเวอร์ทันที!\pงานนี้ต้องชนะเท่านั้น!\nอย่าทำโอกาสหลุดมือล่ะ!\lอนาคตของเราสองคนขึ้นอยู่กับเธอ!$"

BattleFrontier_Lounge3_Text_GetToBattleTowerMulti::
.string "รีบไปห้องมัลติแบทเทิล\nของแบทเทิลทาวเวอร์ทันที!\pงานนี้ต้องชนะเท่านั้น!\nอย่าทำโอกาสหลุดมือล่ะ!\lอนาคตของเราสองคนขึ้นอยู่กับเธอ!$"

BattleFrontier_Lounge3_Text_GetToBattleDomeSingle::
.string "รีบไปทัวร์นาเมนต์ซิงเกิลแบทเทิล\nของแบทเทิลโดมทันที!\pงานนี้ต้องชนะเท่านั้น!\nอย่าทำโอกาสหลุดมือล่ะ!\lอนาคตของเราสองคนขึ้นอยู่กับเธอ!$"

BattleFrontier_Lounge3_Text_GetToBattleDomeDouble::
.string "รีบไปทัวร์นาเมนต์ดับเบิลแบทเทิล\nของแบทเทิลโดมทันที!\pงานนี้ต้องชนะเท่านั้น!\nอย่าทำโอกาสหลุดมือล่ะ!\lอนาคตของเราสองคนขึ้นอยู่กับเธอ!$"

BattleFrontier_Lounge3_Text_GetToBattleFactorySingle::
.string "รีบไปแบทเทิลสวอปซิงเกิลทัวร์นาเมนต์\nของแบทเทิลแฟกทอรีทันที!\pงานนี้ต้องชนะเท่านั้น!\nอย่าทำโอกาสหลุดมือล่ะ!\lอนาคตของเราสองคนขึ้นอยู่กับเธอ!$"

BattleFrontier_Lounge3_Text_GetToBattleFactoryDouble::
.string "รีบไปแบทเทิลสวอปดับเบิลทัวร์นาเมนต์\nของแบทเทิลแฟกทอรีทันที!\pงานนี้ต้องชนะเท่านั้น!\nอย่าทำโอกาสหลุดมือล่ะ!\lอนาคตของเราสองคนขึ้นอยู่กับเธอ!$"

BattleFrontier_Lounge3_Text_GetToBattlePalaceSingle::
.string "รีบไปฮอลล์ซิงเกิลแบทเทิล\nของแบทเทิลพาเลซทันที!\pงานนี้ต้องชนะเท่านั้น!\nอย่าทำโอกาสหลุดมือล่ะ!\lอนาคตของเราสองคนขึ้นอยู่กับเธอ!$"

BattleFrontier_Lounge3_Text_GetToBattlePalaceDouble::
.string "รีบไปฮอลล์ดับเบิลแบทเทิล\nของแบทเทิลพาเลซทันที!\pงานนี้ต้องชนะเท่านั้น!\nอย่าทำโอกาสหลุดมือล่ะ!\lอนาคตของเราสองคนขึ้นอยู่กับเธอ!$"

BattleFrontier_Lounge3_Text_GetToBattleArena::
.string "รีบไปเซ็ต KO ทัวร์นาเมนต์\nของแบทเทิลอารีนาทันที!\pงานนี้ต้องชนะเท่านั้น!\nอย่าทำโอกาสหลุดมือล่ะ!\lอนาคตของเราสองคนขึ้นอยู่กับเธอ!$"

BattleFrontier_Lounge3_Text_GetToBattlePike::
.string "รีบไปแบทเทิลชอยซ์\nของแบทเทิลไพค์ทันที!\pงานนี้ต้องชนะเท่านั้น!\nอย่าทำโอกาสหลุดมือล่ะ!\lอนาคตของเราสองคนขึ้นอยู่กับเธอ!$"

BattleFrontier_Lounge3_Text_GetToBattlePyramid::
.string "รีบไปแบทเทิลเควสต์\nของแบทเทิลพีระมิดทันที!\pงานนี้ต้องชนะเท่านั้น!\nอย่าทำโอกาสหลุดมือล่ะ!\lอนาคตของเราสองคนขึ้นอยู่กับเธอ!$"

BattleFrontier_Lounge3_Text_NiceTryCantReturnPoints::
.string "อ้อ เธอนี่เอง…\nพยายามได้ดีแล้ว…\pเสียใจด้วย แต่ฉันคืน\nแบทเทิลพอยต์ให้ไม่ได้…\pเอาเรื่องนี้เป็นแรงผลักดัน\nให้คราวหน้าพยายามมากขึ้นก็แล้วกัน!$"

BattleFrontier_Lounge3_Text_HelloChampHeresYourPoints::
.string "โอ้ เยี่ยม!\nหวัดดี แชมป์!\pฉันรู้อยู่แล้วว่าเธอทำได้!\nรู้อยู่แล้วว่าเธอต้องชนะ!\lเราสองคนเป็นผู้ชนะ!\pฉันจะคืนแบทเทิลพอยต์ให้\nพร้อมของแถมจากฉันอีกนิดหน่อย!$"

BattleFrontier_Lounge3_Text_ObtainedBattlePoints::
.string "{PLAYER} ได้รับ\nแบทเทิลพอยต์ {STR_VAR_1} แต้ม.$"

BattleFrontier_Lounge3_Text_ThinkOfMeForAnotherChallenge::
.string "ถ้าอยากท้าประลองอีกครั้ง\nอย่าลืมนึกถึงฉันนะ!$"

BattleFrontier_Lounge3_Text_NotInterested::
.string "ไม่สนใจงั้นเหรอ?! อย่ากลัว\nที่จะเสี่ยงหน่อยเลย!$"

BattleFrontier_Lounge3_Text_Oh::
.string "โอ้…$"

BattleFrontier_Lounge3_Text_BackedWrongTrainer::
.string "{252}{25}{29}{2}{0}{244}{8}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{121}{0}{0}{244}{6}{1}{252}{25}{39}{0}{0}{244}{6}{1}{252}{25}{18}{2}{0}{244}{5}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{28}{0}{0}{244}{7}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{18}{2}{0}{244}{5}{1}{252}{25}{72}{0}{0}{244}{6}{1}{252}{25}{25}{0}{0}{244}{7}{1}{252}{25}{10}{0}{0}{244}{7}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{142}{0}{0}{244}{6}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{106}{1}{0}{244}{6}{1}{252}{25}{42}{0}{0}{244}{6}{1}!\p{252}{25}{46}{0}{0}{244}{7}{1}{252}{25}{21}{1}{0}{244}{6}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{29}{2}{0}{244}{8}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{10}{0}{0}{244}{7}{1}{252}{25}{42}{0}{0}{244}{6}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{32}{0}{0}{244}{7}{1}{252}{25}{66}{1}{0}{244}{7}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{142}{2}{0}{244}{6}{1}{252}{25}{26}{0}{0}{244}{7}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{32}{0}{0}{244}{7}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{65}{0}{0}{244}{7}{1}\n{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{46}{0}{0}{244}{7}{1}{252}{25}{19}{1}{0}{244}{7}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{10}{0}{0}{244}{7}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{51}{1}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{123}{0}{0}{244}{7}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{7}{0}{0}{244}{5}{1}…$"

BattleFrontier_Lounge3_Text_TrainerGoodButRattled::
.string "{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{28}{0}{0}{244}{7}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{18}{2}{0}{244}{5}{1}{252}{25}{10}{0}{0}{244}{7}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{88}{2}{0}{244}{8}{1}{252}{25}{30}{0}{0}{244}{8}{1}…\p{252}{25}{131}{0}{0}{244}{6}{1}{252}{25}{19}{1}{0}{244}{7}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{123}{0}{0}{244}{7}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{7}{0}{0}{244}{5}{1} {252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{66}{1}{0}{244}{7}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{140}{0}{0}{244}{6}{1}{252}{25}{39}{0}{0}{244}{6}{1}{252}{25}{9}{0}{0}{244}{6}{1}{252}{25}{48}{2}{0}{244}{6}{1}{252}{25}{18}{0}{0}{244}{8}{1}{252}{25}{59}{1}{0}{244}{4}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{39}{0}{0}{244}{6}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{50}{0}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{32}{0}{0}{244}{7}{1}\n{252}{25}{10}{0}{0}{244}{7}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{33}{2}{0}{244}{7}{1}{252}{25}{42}{0}{0}{244}{6}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{25}{0}{0}{244}{7}{1}{252}{25}{4}{0}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{31}{0}{0}{244}{7}{1}{252}{25}{28}{0}{0}{244}{7}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{67}{0}{0}{244}{7}{1}{252}{25}{41}{0}{0}{244}{6}{1}{252}{25}{0}{0}{0}{244}{5}{1}{252}{25}{25}{0}{0}{244}{7}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{39}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{8}{0}{0}{244}{6}{1}…$"

BattleFrontier_Lounge3_Text_KnowWinnerWhenISeeOne::
.string "คิกคิก!\nฉันดูออกว่าใครเป็นผู้ชนะ!$"

BattleFrontier_Lounge3_Text_ShouldBeTakingChallenges::
.string "เทรนเนอร์พวกนั้น…\nทำอะไรกันอยู่นะ?\lน่าจะไปท้าประลองกันได้แล้ว.$"
