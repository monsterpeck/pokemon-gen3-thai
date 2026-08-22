BattleFrontier_ReceptionGate_MapScripts::
	map_script MAP_SCRIPT_ON_FRAME_TABLE, BattleFrontier_ReceptionGate_OnFrame
	map_script MAP_SCRIPT_ON_TRANSITION, BattleFrontier_ReceptionGate_OnTransition
	.byte 0

BattleFrontier_ReceptionGate_OnTransition:
	setflag FLAG_LANDMARK_BATTLE_FRONTIER
	end

BattleFrontier_ReceptionGate_OnFrame:
	map_script_2 VAR_HAS_ENTERED_BATTLE_FRONTIER, 0, BattleFrontier_ReceptionGate_EventScript_FirstTimeEntering
	.2byte 0

BattleFrontier_ReceptionGate_EventScript_FirstTimeEntering::
	lockall
	setvar VAR_HAS_ENTERED_BATTLE_FRONTIER, 1
	playse SE_PIN
	applymovement LOCALID_FRONTIER_RECEPTION_GREETER, Common_Movement_ExclamationMark
	waitmovement 0
	applymovement LOCALID_FRONTIER_RECEPTION_GREETER, Common_Movement_Delay48
	waitmovement 0
	msgbox BattleFrontier_ReceptionGate_Text_FirstTimeHereThisWay, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_PLAYER, BattleFrontier_ReceptionGate_Movement_PlayerApproachCounter
	waitmovement 0
	goto BattleFrontier_ReceptionGate_EventScript_ScottScene
	end

BattleFrontier_ReceptionGate_EventScript_ScottScene::
	msgbox BattleFrontier_ReceptionGate_Text_WelcomeToBattleFrontier, MSGBOX_DEFAULT
	msgbox BattleFrontier_ReceptionGate_Text_IssueFrontierPass, MSGBOX_DEFAULT
	playfanfare MUS_OBTAIN_ITEM
	message BattleFrontier_ReceptionGate_Text_ObtainedFrontierPass
	waitfanfare
	waitmessage
	msgbox BattleFrontier_ReceptionGate_Text_PlacedTrainerCardInFrontierPass, MSGBOX_DEFAULT
	setflag FLAG_SYS_FRONTIER_PASS
	msgbox BattleFrontier_ReceptionGate_Text_EnjoyBattleFrontier, MSGBOX_DEFAULT
	msgbox BattleFrontier_ReceptionGate_Text_IfItIsntPlayerYouCame, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_FRONTIER_RECEPTION_GREETER, Common_Movement_WalkInPlaceFasterUp
	applymovement LOCALID_FRONTIER_RECEPTION_GUIDE, Common_Movement_WalkInPlaceFasterUp
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterUp
	waitmovement 0
	playse SE_PIN
	applymovement LOCALID_FRONTIER_RECEPTION_GREETER, Common_Movement_ExclamationMark
	applymovement LOCALID_FRONTIER_RECEPTION_GUIDE, Common_Movement_ExclamationMark
	applymovement LOCALID_PLAYER, Common_Movement_ExclamationMark
	waitmovement 0
	msgbox BattleFrontier_ReceptionGate_Text_OhMrScottGoodDay, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_FRONTIER_RECEPTION_GREETER, BattleFrontier_ReceptionGate_Movement_GreeterFaceScott
	applymovement LOCALID_FRONTIER_RECEPTION_GUIDE, BattleFrontier_ReceptionGate_Movement_FacilityGuideFaceScott
	applymovement LOCALID_PLAYER, BattleFrontier_ReceptionGate_Movement_PlayerFaceScott
	applymovement LOCALID_FRONTIER_RECEPTION_SCOTT, BattleFrontier_ReceptionGate_Movement_ScottEnter
	waitmovement 0
	msgbox BattleFrontier_ReceptionGate_Text_ScottGreatToSeeYouHere, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_FRONTIER_RECEPTION_SCOTT, BattleFrontier_ReceptionGate_Movement_ScottExit
	waitmovement 0
	removeobject LOCALID_FRONTIER_RECEPTION_SCOTT
	releaseall
	end

BattleFrontier_ReceptionGate_Movement_PlayerApproachCounter:
	walk_up
	walk_up
	walk_left
	walk_left
	step_end

BattleFrontier_ReceptionGate_Movement_PlayerFaceScott:
	delay_16
	delay_16
	delay_16
	delay_8
	walk_in_place_faster_right
	step_end

@ Unused
BattleFrontier_ReceptionGate_Movement_WalkDown:
	walk_down
	walk_down
	step_end

BattleFrontier_ReceptionGate_Movement_ScottEnter:
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_left
	step_end

BattleFrontier_ReceptionGate_Movement_ScottExit:
	walk_right
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	step_end

BattleFrontier_ReceptionGate_Movement_GreeterFaceScott:
	delay_16
	delay_16
	delay_16
	delay_8
	walk_in_place_faster_right
	step_end

BattleFrontier_ReceptionGate_Movement_FacilityGuideFaceScott:
	delay_16
	delay_16
	delay_16
	delay_8
	walk_in_place_faster_left
	step_end

BattleFrontier_ReceptionGate_EventScript_Greeter::
	lock
	faceplayer
	msgbox BattleFrontier_ReceptionGate_Text_WelcomeToBattleFrontier, MSGBOX_DEFAULT
	msgbox BattleFrontier_ReceptionGate_Text_EnjoyBattleFrontier, MSGBOX_DEFAULT
	release
	end

BattleFrontier_ReceptionGate_EventScript_FacilityGuide::
	lock
	faceplayer
	msgbox BattleFrontier_ReceptionGate_Text_YourGuideToFacilities, MSGBOX_DEFAULT
	goto BattleFrontier_ReceptionGate_EventScript_ChooseFacilityToLearnAbout
	end

BattleFrontier_ReceptionGate_EventScript_ChooseFacilityToLearnAbout::
	message BattleFrontier_ReceptionGate_Text_LearnAboutWhich2
	waitmessage
	setvar VAR_0x8004, SCROLL_MULTI_BF_RECEPTIONIST
	special ShowScrollableMultichoice
	switch VAR_RESULT
	case 0, BattleFrontier_ReceptionGate_EventScript_BattleTower
	case 1, BattleFrontier_ReceptionGate_EventScript_BattleDome
	case 2, BattleFrontier_ReceptionGate_EventScript_BattlePalace
	case 3, BattleFrontier_ReceptionGate_EventScript_BattleArena
	case 4, BattleFrontier_ReceptionGate_EventScript_BattleFactory
	case 5, BattleFrontier_ReceptionGate_EventScript_BattlePike
	case 6, BattleFrontier_ReceptionGate_EventScript_BattlePyramid
	case 7, BattleFrontier_ReceptionGate_EventScript_RankingHall
	case 8, BattleFrontier_ReceptionGate_EventScript_ExchangeCorner
	case 9, BattleFrontier_ReceptionGate_EventScript_ExitFacilityGuide
	case MULTI_B_PRESSED, BattleFrontier_ReceptionGate_EventScript_ExitFacilityGuide
	end

BattleFrontier_ReceptionGate_EventScript_BattleTower::
	msgbox BattleFrontier_ReceptionGate_Text_BattleTowerInfo, MSGBOX_DEFAULT
	goto BattleFrontier_ReceptionGate_EventScript_ChooseFacilityToLearnAbout
	end

BattleFrontier_ReceptionGate_EventScript_BattleDome::
	msgbox BattleFrontier_ReceptionGate_Text_BattleDomeInfo, MSGBOX_DEFAULT
	goto BattleFrontier_ReceptionGate_EventScript_ChooseFacilityToLearnAbout
	end

BattleFrontier_ReceptionGate_EventScript_BattlePalace::
	msgbox BattleFrontier_ReceptionGate_Text_BattlePalaceInfo, MSGBOX_DEFAULT
	goto BattleFrontier_ReceptionGate_EventScript_ChooseFacilityToLearnAbout
	end

BattleFrontier_ReceptionGate_EventScript_BattleArena::
	msgbox BattleFrontier_ReceptionGate_Text_BattleArenaInfo, MSGBOX_DEFAULT
	goto BattleFrontier_ReceptionGate_EventScript_ChooseFacilityToLearnAbout
	end

BattleFrontier_ReceptionGate_EventScript_BattleFactory::
	msgbox BattleFrontier_ReceptionGate_Text_BattleFactoryInfo, MSGBOX_DEFAULT
	goto BattleFrontier_ReceptionGate_EventScript_ChooseFacilityToLearnAbout
	end

BattleFrontier_ReceptionGate_EventScript_BattlePike::
	msgbox BattleFrontier_ReceptionGate_Text_BattlePikeInfo, MSGBOX_DEFAULT
	goto BattleFrontier_ReceptionGate_EventScript_ChooseFacilityToLearnAbout
	end

BattleFrontier_ReceptionGate_EventScript_BattlePyramid::
	msgbox BattleFrontier_ReceptionGate_Text_BattlePyramidInfo, MSGBOX_DEFAULT
	goto BattleFrontier_ReceptionGate_EventScript_ChooseFacilityToLearnAbout
	end

BattleFrontier_ReceptionGate_EventScript_RankingHall::
	msgbox BattleFrontier_ReceptionGate_Text_RankingHallInfo, MSGBOX_DEFAULT
	goto BattleFrontier_ReceptionGate_EventScript_ChooseFacilityToLearnAbout
	end

BattleFrontier_ReceptionGate_EventScript_ExchangeCorner::
	msgbox BattleFrontier_ReceptionGate_Text_ExchangeCornerInfo, MSGBOX_DEFAULT
	goto BattleFrontier_ReceptionGate_EventScript_ChooseFacilityToLearnAbout
	end

BattleFrontier_ReceptionGate_EventScript_ExitFacilityGuide::
	msgbox BattleFrontier_ReceptionGate_Text_EnjoyBattleFrontier, MSGBOX_DEFAULT
	release
	end

BattleFrontier_ReceptionGate_EventScript_RulesGuide::
	lock
	faceplayer
	msgbox BattleFrontier_ReceptionGate_Text_YourGuideToRules, MSGBOX_DEFAULT
	goto BattleFrontier_ReceptionGate_EventScript_ChooseRuleToLearnAbout
	end

BattleFrontier_ReceptionGate_EventScript_ChooseRuleToLearnAbout::
	message BattleFrontier_ReceptionGate_Text_LearnAboutWhat
	waitmessage
	multichoice 15, 0, MULTI_FRONTIER_RULES, FALSE
	switch VAR_RESULT
	case 0, BattleFrontier_ReceptionGate_EventScript_LevelMode
	case 1, BattleFrontier_ReceptionGate_EventScript_Level50
	case 2, BattleFrontier_ReceptionGate_EventScript_OpenLevel
	case 3, BattleFrontier_ReceptionGate_EventScript_MonEntry
	case 4, BattleFrontier_ReceptionGate_EventScript_HoldItems
	case 5, BattleFrontier_ReceptionGate_EventScript_ExitRulesGuide
	case MULTI_B_PRESSED, BattleFrontier_ReceptionGate_EventScript_ExitRulesGuide
	end

BattleFrontier_ReceptionGate_EventScript_LevelMode::
	msgbox BattleFrontier_ReceptionGate_Text_LevelModeInfo, MSGBOX_DEFAULT
	goto BattleFrontier_ReceptionGate_EventScript_ChooseRuleToLearnAbout
	end

BattleFrontier_ReceptionGate_EventScript_Level50::
	msgbox BattleFrontier_ReceptionGate_Text_Level50Info, MSGBOX_DEFAULT
	goto BattleFrontier_ReceptionGate_EventScript_ChooseRuleToLearnAbout
	end

BattleFrontier_ReceptionGate_EventScript_OpenLevel::
	msgbox BattleFrontier_ReceptionGate_Text_OpenLevelInfo, MSGBOX_DEFAULT
	goto BattleFrontier_ReceptionGate_EventScript_ChooseRuleToLearnAbout
	end

BattleFrontier_ReceptionGate_EventScript_MonEntry::
	msgbox BattleFrontier_ReceptionGate_Text_MonEntryInfo, MSGBOX_DEFAULT
	goto BattleFrontier_ReceptionGate_EventScript_ChooseRuleToLearnAbout
	end

BattleFrontier_ReceptionGate_EventScript_HoldItems::
	msgbox BattleFrontier_ReceptionGate_Text_HoldItemsInfo, MSGBOX_DEFAULT
	goto BattleFrontier_ReceptionGate_EventScript_ChooseRuleToLearnAbout
	end

BattleFrontier_ReceptionGate_EventScript_ExitRulesGuide::
	msgbox BattleFrontier_ReceptionGate_Text_EnjoyBattleFrontier, MSGBOX_DEFAULT
	release
	end

BattleFrontier_ReceptionGate_EventScript_FrontierPassGuide::
	lock
	faceplayer
	msgbox BattleFrontier_ReceptionGate_Text_YourGuideToFrontierPass, MSGBOX_DEFAULT
	goto BattleFrontier_ReceptionGate_EventScript_ChooseFrontierPassInfoToLearnAbout
	end

BattleFrontier_ReceptionGate_EventScript_ChooseFrontierPassInfoToLearnAbout::
	message BattleFrontier_ReceptionGate_Text_LearnAboutWhich1
	waitmessage
	multichoice 16, 4, MULTI_FRONTIER_PASS_INFO, FALSE
	switch VAR_RESULT
	case 0, BattleFrontier_ReceptionGate_EventScript_Symbols
	case 1, BattleFrontier_ReceptionGate_EventScript_RecordBattle
	case 2, BattleFrontier_ReceptionGate_EventScript_BattlePoints
	case 3, BattleFrontier_ReceptionGate_EventScript_ExitFrontierPassGuide
	case MULTI_B_PRESSED, BattleFrontier_ReceptionGate_EventScript_ExitFrontierPassGuide
	end

BattleFrontier_ReceptionGate_EventScript_Symbols::
	msgbox BattleFrontier_ReceptionGate_Text_SymbolsInfo, MSGBOX_DEFAULT
	goto BattleFrontier_ReceptionGate_EventScript_ChooseFrontierPassInfoToLearnAbout
	end

BattleFrontier_ReceptionGate_EventScript_RecordBattle::
	msgbox BattleFrontier_ReceptionGate_Text_RecordedBattleInfo, MSGBOX_DEFAULT
	goto BattleFrontier_ReceptionGate_EventScript_ChooseFrontierPassInfoToLearnAbout
	end

BattleFrontier_ReceptionGate_EventScript_BattlePoints::
	msgbox BattleFrontier_ReceptionGate_Text_BattlePointsInfo, MSGBOX_DEFAULT
	goto BattleFrontier_ReceptionGate_EventScript_ChooseFrontierPassInfoToLearnAbout
	end

BattleFrontier_ReceptionGate_EventScript_ExitFrontierPassGuide::
	msgbox BattleFrontier_ReceptionGate_Text_EnjoyBattleFrontier, MSGBOX_DEFAULT
	release
	end

BattleFrontier_ReceptionGate_Text_FirstTimeHereThisWay:
.string "มาที่นี่ครั้งแรกใช่ไหม?\nเชิญทางนี้เลย!$"

BattleFrontier_ReceptionGate_Text_WelcomeToBattleFrontier:
.string "แนวหน้าของการต่อสู้โปเกมอน!\nยินดีต้อนรับสู่แบทเทิลฟรอนเทียร์!$"

BattleFrontier_ReceptionGate_Text_IssueFrontierPass:
.string "สำหรับผู้มาเยือนครั้งแรก เราจะมอบ\nฟรอนเทียร์พาสให้.\pใช้ได้กับทุกสถานที่\nในแบทเทิลฟรอนเทียร์.\pรับไปเลย!$"

BattleFrontier_ReceptionGate_Text_ObtainedFrontierPass:
.string "{PLAYER} ได้รับ\nฟรอนเทียร์พาส.$"

BattleFrontier_ReceptionGate_Text_PlacedTrainerCardInFrontierPass:
.string "{PLAYER} {252}{25}{4}{0}{0}{244}{6}{1}{252}{25}{81}{1}{0}{244}{6}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{28}{0}{0}{244}{7}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{18}{2}{0}{244}{5}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{18}{2}{0}{244}{5}{1}{252}{25}{25}{0}{0}{244}{7}{1}\n{252}{25}{41}{0}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{4}{0}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{36}{0}{0}{244}{8}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{126}{0}{0}{244}{7}{1}{252}{25}{39}{0}{0}{244}{6}{1}{252}{25}{18}{2}{0}{244}{5}{1}{252}{25}{35}{0}{0}{244}{8}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{45}{0}{0}{244}{6}{1}$"

BattleFrontier_ReceptionGate_Text_EnjoyBattleFrontier:
.string "ขอให้สนุกกับทุกสิ่งที่\nแบทเทิลฟรอนเทียร์มีให้!$"

BattleFrontier_ReceptionGate_Text_IfItIsntPlayerYouCame:
.string "???: อ้าว นี่ {PLAYER}{KUN} ไม่ใช่เหรอ!\nมาถึงที่นี่แล้วสินะ!$"

BattleFrontier_ReceptionGate_Text_OhMrScottGoodDay:
.string "ไกด์: โอ้! คุณสก็อตต์ครับ!\nสวัสดีครับ!$"

BattleFrontier_ReceptionGate_Text_ScottGreatToSeeYouHere:
.string "สก็อตต์: ดีใจจริง ๆ ที่ได้เจอเธอที่นี่\nจริง ๆ นะ!\pหวังว่าเธอจะค่อย ๆ ใช้เวลา\nสำรวจให้ทั่วเลย.\pแน่นอน ฉันก็หวังให้เธอได้สัมผัส\nแก่นแท้ของการต่อสู้ด้วย.\pฉันมีห้องพักอยู่ที่นี่เหมือนกัน ถ้ามี\nเวลาก็แวะมาได้เลย.$"

BattleFrontier_ReceptionGate_Text_YourGuideToFacilities:
.string "ฉันคือไกด์แนะนำสถานที่ต่าง ๆ\nภายในแบทเทิลฟรอนเทียร์.$"

BattleFrontier_ReceptionGate_Text_LearnAboutWhich2:
.string "อยากรู้เรื่องไหน?$"

BattleFrontier_ReceptionGate_Text_BattleTowerInfo:
.string "หอคอยขนาดยักษ์ที่ถือเป็น\nสัญลักษณ์ของแบทเทิลฟรอนเทียร์.\pภายในมีแบทเทิลรูม 4 แบบ\nสำหรับซิงเกิล ดับเบิล มัลติ\lและลิงก์มัลติแบทเทิล.$"

BattleFrontier_ReceptionGate_Text_BattleDomeInfo:
.string "แบทเทิลโดมคืออาคารขนาดใหญ่\nรูปทรงเหมือนไข่ยักษ์.\pที่นี่จัดการแข่งขัน\nที่เรียกว่าแบทเทิลทัวร์นีย์.\pแบทเทิลทัวร์นีย์มี\n2 คอร์ส คือซิงเกิลและดับเบิล\lแบทเทิล.$"

BattleFrontier_ReceptionGate_Text_BattlePalaceInfo:
.string "แบทเทิลพาเลซคืออาคารสีแดง\nทางขวาของแบทเทิลฟรอนเทียร์.\pมีแบทเทิลฮอลล์ 2 แบบ\nสำหรับซิงเกิลและดับเบิลแบทเทิล.$"

BattleFrontier_ReceptionGate_Text_BattleArenaInfo:
.string "แบทเทิลอารีนาคืออาคารคล้ายโดโจ\nอยู่บริเวณกลางค่อนไปทางขวา\lของแบทเทิลฟรอนเทียร์.\pที่นี่จัดการแข่งขันที่เรียกว่า\nเซ็ต KO ทัวร์นีย์.$"

BattleFrontier_ReceptionGate_Text_BattleFactoryInfo:
.string "แบทเทิลแฟกทอรีคืออาคารขนาดใหญ่\nที่อยู่ใกล้เราที่สุด.\pที่นี่จัดการแข่งขันที่เรียกว่า\nแบทเทิลสวอป.\pแบทเทิลสวอปมี\n2 คอร์ส คือซิงเกิลและดับเบิล\lแบทเทิล.$"

BattleFrontier_ReceptionGate_Text_BattlePikeInfo:
.string "แบทเทิลไพค์คืออาคารที่มีรูปทรง\nเหมือนโปเกมอน อยู่บริเวณกลางค่อนไปซ้าย\lของแบทเทิลฟรอนเทียร์.\pที่นี่จัดการแข่งขันที่เรียกว่า\nแบทเทิลชอยซ์.$"

BattleFrontier_ReceptionGate_Text_BattlePyramidInfo:
.string "แบทเทิลพีระมิดคือ\nพีระมิดขนาดมหึมา.\pที่นี่จัดการแข่งขันที่เรียกว่า\nแบทเทิลเควสต์.$"

BattleFrontier_ReceptionGate_Text_RankingHallInfo:
.string "แรงกิงฮอลล์อยู่ใกล้\nแบทเทิลทาวเวอร์.\pที่นั่นคุณจะได้เห็นสถิติสุดยอด\nของเหล่าเทรนเนอร์ที่เคย\lท้าประลองมากมายใน\lแบทเทิลฟรอนเทียร์.$"

BattleFrontier_ReceptionGate_Text_ExchangeCornerInfo:
.string "เอ็กซ์เชนจ์เซอร์วิสคอร์เนอร์อยู่ใกล้\nแบทเทิลทาวเวอร์.\pแบทเทิลพอยต์ที่คุณได้รับจาก\nแบทเทิลฟรอนเทียร์สามารถนำไปแลก\lของรางวัลชั้นเยี่ยมที่นั่นได้.$"

BattleFrontier_ReceptionGate_Text_YourGuideToRules:
.string "ฉันคือไกด์อธิบายกฎพื้นฐานที่\nใช้ร่วมกันในการท้าประลองต่าง ๆ\lของสถานที่ในแบทเทิล\lฟรอนเทียร์.$"

BattleFrontier_ReceptionGate_Text_LearnAboutWhat:
.string "อยากรู้เรื่องอะไร?$"

BattleFrontier_ReceptionGate_Text_LevelModeInfo:
.string "การท้าประลองทั้งหมดในสถานที่\nของแบทเทิลฟรอนเทียร์มี\l2 คอร์ส คือเลเวล 50 และโอเพนเลเวล.$"

BattleFrontier_ReceptionGate_Text_Level50Info:
.string "คอร์สเลเวล 50 เปิดให้โปเกมอน\nที่มีเลเวลไม่เกิน 50 เข้าร่วม.\pแต่โปรดจำไว้ว่าเทรนเนอร์\nคู่ต่อสู้จะไม่มีโปเกมอน\lที่ต่ำกว่าเลเวล 50.\pคอร์สนี้เป็นระดับเริ่มต้นสำหรับ\nการต่อสู้ในแบทเทิลฟรอนเทียร์.\pเราแนะนำให้เริ่มท้าประลอง\nจากคอร์สนี้.$"

BattleFrontier_ReceptionGate_Text_OpenLevelInfo:
.string "คอร์สโอเพนเลเวลไม่จำกัด\nเลเวลของโปเกมอนที่เข้า\lท้าประลอง.\pเลเวลของคู่ต่อสู้จะถูกปรับ\nให้ตรงกับเลเวลของ\lโปเกมอนของคุณ.\pอย่างไรก็ตาม เทรนเนอร์คู่ต่อสู้\nจะไม่มีโปเกมอนต่ำกว่าเลเวล 60.$"

BattleFrontier_ReceptionGate_Text_MonEntryInfo:
.string "โปเกมอนเกือบทุกชนิดสามารถ\nเข้าท้าประลองได้ทุกสถานที่.\pแต่ไข่และโปเกมอนบางชนิด\nไม่ได้รับอนุญาต.\pจำนวนโปเกมอนที่ต้องใช้ในการ\nท้าประลองขึ้นอยู่กับแต่ละสถานที่.\pแต่ทุกสถานที่จะไม่อนุญาตให้\nใช้โปเกมอนชนิดเดียวกันตั้งแต่\l2 ตัวขึ้นไป.$"

BattleFrontier_ReceptionGate_Text_HoldItemsInfo:
.string "เมื่อเข้าท้าประลองในสถานที่\nของแบทเทิลฟรอนเทียร์ โปเกมอน\lห้ามถือไอเทมชนิดเดียวกัน.\pโปรดตรวจให้แน่ใจว่าโปเกมอน\nทุกตัวที่เข้าท้าประลองถือ\lไอเทมต่างชนิดกัน.$"

BattleFrontier_ReceptionGate_Text_YourGuideToFrontierPass:
.string "ฉันคือไกด์แนะนำฟรอนเทียร์พาส.$"

BattleFrontier_ReceptionGate_Text_LearnAboutWhich1:
.string "อยากรู้เรื่องไหน?$"

BattleFrontier_ReceptionGate_Text_SymbolsInfo:
.string "แบทเทิลฟรอนเทียร์มี\nสถานที่ทั้งหมด 7 แห่ง.\pเทรนเนอร์ที่ได้รับการยอมรับ\nในฝีมือ อาจได้รับ\lสัญลักษณ์จากแต่ละสถานที่.\pเพื่อรับสัญลักษณ์ เทรนเนอร์อาจต้อง\nชนะเทรนเนอร์คนอื่นต่อเนื่อง\lและอาจต้องชนะการแข่งขันหลายครั้ง.\pการได้สัญลักษณ์ไม่ใช่เรื่องง่ายเลย.\nขอให้โชคดี!$"

BattleFrontier_ReceptionGate_Text_RecordedBattleInfo:
.string "สามารถบันทึกการต่อสู้ 1 ครั้ง\nไว้ในฟรอนเทียร์พาสได้.\pคุณอาจบันทึกการต่อสู้ที่เล่นกับ\nเพื่อนหนึ่งคนหรือหลายคน.\pหรือบันทึกการต่อสู้ที่เกิดขึ้น\nในแบทเทิลฟรอนเทียร์ ยกเว้น\lการแข่งขันในแบทเทิลไพค์หรือ\lแบทเทิลพีระมิด.\pเมื่อการต่อสู้จบ คุณสามารถเลือก\nบันทึกแมตช์นั้นได้.$"

BattleFrontier_ReceptionGate_Text_BattlePointsInfo:
.string "แบทเทิลพอยต์คือรางวัลที่มอบให้\nเทรนเนอร์ที่ต่อสู้ได้ยอดเยี่ยม\lในแบทเทิลฟรอนเทียร์.\pคุณสามารถนำแบทเทิลพอยต์\nไปแลกของรางวัลที่เอ็กซ์เชนจ์เซอร์วิส\lคอร์เนอร์ได้.$"

