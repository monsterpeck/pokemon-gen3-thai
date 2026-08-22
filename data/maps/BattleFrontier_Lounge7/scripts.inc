BattleFrontier_Lounge7_MapScripts::
	.byte 0

BattleFrontier_Lounge7_EventScript_LeftMoveTutor::
	lock
	faceplayer
	setvar VAR_TEMP_C, SCROLL_MULTI_BF_MOVE_TUTOR_1
	goto_if_set FLAG_MET_FRONTIER_BEAUTY_MOVE_TUTOR, BattleFrontier_Lounge7_EventScript_AlreadyMetLeftTutor
	msgbox BattleFrontier_Lounge7_Text_LeftTutorIntro, MSGBOX_DEFAULT
	setflag FLAG_MET_FRONTIER_BEAUTY_MOVE_TUTOR
	goto BattleFrontier_Lounge7_EventScript_ChooseLeftTutorMove
	end

BattleFrontier_Lounge7_EventScript_AlreadyMetLeftTutor::
	msgbox BattleFrontier_Lounge7_Text_LeftTutorWelcomeBack, MSGBOX_DEFAULT
	goto BattleFrontier_Lounge7_EventScript_ChooseLeftTutorMove
	end

BattleFrontier_Lounge7_EventScript_ChooseLeftTutorMove::
	message BattleFrontier_Lounge7_Text_TeachWhichMove
	waitmessage
	special ShowBattlePointsWindow
	setvar VAR_TEMP_FRONTIER_TUTOR_ID, 0
	setvar VAR_0x8004, SCROLL_MULTI_BF_MOVE_TUTOR_1
	setvar VAR_0x8006, 0
	special ShowScrollableMultichoice
	copyvar VAR_TEMP_FRONTIER_TUTOR_SELECTION, VAR_RESULT
	switch VAR_RESULT
	case 0, BattleFrontier_Lounge7_EventScript_Softboiled
	case 1, BattleFrontier_Lounge7_EventScript_SeismicToss
	case 2, BattleFrontier_Lounge7_EventScript_DreamEater
	case 3, BattleFrontier_Lounge7_EventScript_MegaPunch
	case 4, BattleFrontier_Lounge7_EventScript_MegaKick
	case 5, BattleFrontier_Lounge7_EventScript_BodySlam
	case 6, BattleFrontier_Lounge7_EventScript_RockSlide
	case 7, BattleFrontier_Lounge7_EventScript_Counter
	case 8, BattleFrontier_Lounge7_EventScript_ThunderWave
	case 9, BattleFrontier_Lounge7_EventScript_SwordsDance
	case 10, BattleFrontier_Lounge7_EventScript_ExitTutorMoveSelect
	case MULTI_B_PRESSED, BattleFrontier_Lounge7_EventScript_ExitTutorMoveSelect
	end

BattleFrontier_Lounge7_EventScript_ChooseNewLeftTutorMove::
	message BattleFrontier_Lounge7_Text_TeachWhichMove
	waitmessage
	setvar VAR_TEMP_FRONTIER_TUTOR_ID, 0
	setvar VAR_0x8004, SCROLL_MULTI_BF_MOVE_TUTOR_1
	setvar VAR_0x8006, 1
	special ShowScrollableMultichoice
	copyvar VAR_TEMP_FRONTIER_TUTOR_SELECTION, VAR_RESULT
	switch VAR_RESULT
	case 0, BattleFrontier_Lounge7_EventScript_Softboiled
	case 1, BattleFrontier_Lounge7_EventScript_SeismicToss
	case 2, BattleFrontier_Lounge7_EventScript_DreamEater
	case 3, BattleFrontier_Lounge7_EventScript_MegaPunch
	case 4, BattleFrontier_Lounge7_EventScript_MegaKick
	case 5, BattleFrontier_Lounge7_EventScript_BodySlam
	case 6, BattleFrontier_Lounge7_EventScript_RockSlide
	case 7, BattleFrontier_Lounge7_EventScript_Counter
	case 8, BattleFrontier_Lounge7_EventScript_ThunderWave
	case 9, BattleFrontier_Lounge7_EventScript_SwordsDance
	case 10, BattleFrontier_Lounge7_EventScript_ExitTutorMoveSelect
	case MULTI_B_PRESSED, BattleFrontier_Lounge7_EventScript_ExitTutorMoveSelect
	end

BattleFrontier_Lounge7_EventScript_Softboiled::
	setvar VAR_0x8008, 16
	goto BattleFrontier_Lounge7_EventScript_ConfirmMoveSelection
	end

BattleFrontier_Lounge7_EventScript_SeismicToss::
	setvar VAR_0x8008, 24
	goto BattleFrontier_Lounge7_EventScript_ConfirmMoveSelection
	end

BattleFrontier_Lounge7_EventScript_DreamEater::
	setvar VAR_0x8008, 24
	goto BattleFrontier_Lounge7_EventScript_ConfirmMoveSelection
	end

BattleFrontier_Lounge7_EventScript_MegaPunch::
	setvar VAR_0x8008, 24
	goto BattleFrontier_Lounge7_EventScript_ConfirmMoveSelection
	end

BattleFrontier_Lounge7_EventScript_MegaKick::
	setvar VAR_0x8008, 48
	goto BattleFrontier_Lounge7_EventScript_ConfirmMoveSelection
	end

BattleFrontier_Lounge7_EventScript_BodySlam::
	setvar VAR_0x8008, 48
	goto BattleFrontier_Lounge7_EventScript_ConfirmMoveSelection
	end

BattleFrontier_Lounge7_EventScript_RockSlide::
	setvar VAR_0x8008, 48
	goto BattleFrontier_Lounge7_EventScript_ConfirmMoveSelection
	end

BattleFrontier_Lounge7_EventScript_Counter::
	setvar VAR_0x8008, 48
	goto BattleFrontier_Lounge7_EventScript_ConfirmMoveSelection
	end

BattleFrontier_Lounge7_EventScript_ThunderWave::
	setvar VAR_0x8008, 48
	goto BattleFrontier_Lounge7_EventScript_ConfirmMoveSelection
	end

BattleFrontier_Lounge7_EventScript_SwordsDance::
	setvar VAR_0x8008, 48
	goto BattleFrontier_Lounge7_EventScript_ConfirmMoveSelection
	end

BattleFrontier_Lounge7_EventScript_RightMoveTutor::
	lock
	faceplayer
	setvar VAR_TEMP_C, SCROLL_MULTI_BF_MOVE_TUTOR_2
	goto_if_set FLAG_MET_FRONTIER_SWIMMER_MOVE_TUTOR, BattleFrontier_Lounge7_EventScript_AlreadyMetRightTutor
	msgbox BattleFrontier_Lounge7_Text_RightTutorIntro, MSGBOX_DEFAULT
	setflag FLAG_MET_FRONTIER_SWIMMER_MOVE_TUTOR
	goto BattleFrontier_Lounge7_EventScript_ChooseRightTutorMove
	end

BattleFrontier_Lounge7_EventScript_AlreadyMetRightTutor::
	msgbox BattleFrontier_Lounge7_Text_RightTutorWelcomeBack, MSGBOX_DEFAULT
	goto BattleFrontier_Lounge7_EventScript_ChooseRightTutorMove
	end

BattleFrontier_Lounge7_EventScript_ChooseRightTutorMove::
	message BattleFrontier_Lounge7_Text_TeachWhichMove
	waitmessage
	special ShowBattlePointsWindow
	setvar VAR_TEMP_FRONTIER_TUTOR_ID, 1
	setvar VAR_0x8004, SCROLL_MULTI_BF_MOVE_TUTOR_2
	setvar VAR_0x8006, 0
	special ShowScrollableMultichoice
	copyvar VAR_TEMP_FRONTIER_TUTOR_SELECTION, VAR_RESULT
	switch VAR_RESULT
	case 0, BattleFrontier_Lounge7_EventScript_DefenseCurl
	case 1, BattleFrontier_Lounge7_EventScript_Snore
	case 2, BattleFrontier_Lounge7_EventScript_MudSlap
	case 3, BattleFrontier_Lounge7_EventScript_Swift
	case 4, BattleFrontier_Lounge7_EventScript_IcyWind
	case 5, BattleFrontier_Lounge7_EventScript_Endure
	case 6, BattleFrontier_Lounge7_EventScript_PsychUp
	case 7, BattleFrontier_Lounge7_EventScript_IcePunch
	case 8, BattleFrontier_Lounge7_EventScript_ThunderPunch
	case 9, BattleFrontier_Lounge7_EventScript_FirePunch
	case 10, BattleFrontier_Lounge7_EventScript_ExitTutorMoveSelect
	case MULTI_B_PRESSED, BattleFrontier_Lounge7_EventScript_ExitTutorMoveSelect
	end

BattleFrontier_Lounge7_EventScript_ChooseNewRightTutorMove::
	message BattleFrontier_Lounge7_Text_TeachWhichMove
	waitmessage
	setvar VAR_TEMP_FRONTIER_TUTOR_ID, 1
	setvar VAR_0x8004, SCROLL_MULTI_BF_MOVE_TUTOR_2
	setvar VAR_0x8006, 1
	special ShowScrollableMultichoice
	copyvar VAR_TEMP_FRONTIER_TUTOR_SELECTION, VAR_RESULT
	switch VAR_RESULT
	case 0, BattleFrontier_Lounge7_EventScript_DefenseCurl
	case 1, BattleFrontier_Lounge7_EventScript_Snore
	case 2, BattleFrontier_Lounge7_EventScript_MudSlap
	case 3, BattleFrontier_Lounge7_EventScript_Swift
	case 4, BattleFrontier_Lounge7_EventScript_IcyWind
	case 5, BattleFrontier_Lounge7_EventScript_Endure
	case 6, BattleFrontier_Lounge7_EventScript_PsychUp
	case 7, BattleFrontier_Lounge7_EventScript_IcePunch
	case 8, BattleFrontier_Lounge7_EventScript_ThunderPunch
	case 9, BattleFrontier_Lounge7_EventScript_FirePunch
	case 10, BattleFrontier_Lounge7_EventScript_ExitTutorMoveSelect
	case MULTI_B_PRESSED, BattleFrontier_Lounge7_EventScript_ExitTutorMoveSelect
	end

BattleFrontier_Lounge7_EventScript_DefenseCurl::
	setvar VAR_0x8008, 16
	goto BattleFrontier_Lounge7_EventScript_ConfirmMoveSelection
	end

BattleFrontier_Lounge7_EventScript_Snore::
	setvar VAR_0x8008, 24
	goto BattleFrontier_Lounge7_EventScript_ConfirmMoveSelection
	end

BattleFrontier_Lounge7_EventScript_MudSlap::
	setvar VAR_0x8008, 24
	goto BattleFrontier_Lounge7_EventScript_ConfirmMoveSelection
	end

BattleFrontier_Lounge7_EventScript_Swift::
	setvar VAR_0x8008, 24
	goto BattleFrontier_Lounge7_EventScript_ConfirmMoveSelection
	end

BattleFrontier_Lounge7_EventScript_IcyWind::
	setvar VAR_0x8008, 24
	goto BattleFrontier_Lounge7_EventScript_ConfirmMoveSelection
	end

BattleFrontier_Lounge7_EventScript_Endure::
	setvar VAR_0x8008, 48
	goto BattleFrontier_Lounge7_EventScript_ConfirmMoveSelection
	end

BattleFrontier_Lounge7_EventScript_PsychUp::
	setvar VAR_0x8008, 48
	goto BattleFrontier_Lounge7_EventScript_ConfirmMoveSelection
	end

BattleFrontier_Lounge7_EventScript_IcePunch::
	setvar VAR_0x8008, 48
	goto BattleFrontier_Lounge7_EventScript_ConfirmMoveSelection
	end

BattleFrontier_Lounge7_EventScript_ThunderPunch::
	setvar VAR_0x8008, 48
	goto BattleFrontier_Lounge7_EventScript_ConfirmMoveSelection
	end

BattleFrontier_Lounge7_EventScript_FirePunch::
	setvar VAR_0x8008, 48
	goto BattleFrontier_Lounge7_EventScript_ConfirmMoveSelection
	end

BattleFrontier_Lounge7_EventScript_ExitTutorMoveSelect::
	special CloseBattleFrontierTutorWindow
	special CloseBattlePointsWindow
	msgbox BattleFrontier_Lounge7_Text_YouDontWantTo, MSGBOX_DEFAULT
	release
	end

BattleFrontier_Lounge7_EventScript_CancelChooseMon::
	msgbox BattleFrontier_Lounge7_Text_YouDontWantTo, MSGBOX_DEFAULT
	release
	end

@ VAR_0x8008 is the price
@ VAR_TEMP_C is the scroll multichoice ID
@ VAR_TEMP_FRONTIER_TUTOR_SELECTION is the move selection
@ VAR_TEMP_FRONTIER_TUTOR_ID is which move tutor was spoken to
BattleFrontier_Lounge7_EventScript_ConfirmMoveSelection::
	copyvar VAR_0x8004, VAR_TEMP_FRONTIER_TUTOR_SELECTION
	copyvar VAR_0x8005, VAR_TEMP_FRONTIER_TUTOR_ID
	special BufferBattleFrontierTutorMoveName
	buffernumberstring STR_VAR_2, VAR_0x8008
	copyvar VAR_0x8004, VAR_TEMP_C
	msgbox BattleFrontier_Lounge7_Text_MoveWillBeXBattlePoints, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, BattleFrontier_Lounge7_EventScript_ChooseNewMove
	specialvar VAR_TEMP_1, GetFrontierBattlePoints
	goto_if_ge VAR_TEMP_1, VAR_0x8008, BattleFrontier_Lounge7_EventScript_TeachTutorMove
	msgbox BattleFrontier_Lounge7_Text_HaventGotEnoughPoints, MSGBOX_DEFAULT
	goto BattleFrontier_Lounge7_EventScript_ChooseNewMove
	end

BattleFrontier_Lounge7_EventScript_TeachTutorMove::
	msgbox BattleFrontier_Lounge7_Text_TeachMoveToWhichMon, MSGBOX_DEFAULT
	special GetBattleFrontierTutorMoveIndex
	fadescreen FADE_TO_BLACK
	special CloseBattlePointsWindow
	special CloseBattleFrontierTutorWindow
	special ChooseMonForMoveTutor
	goto_if_eq VAR_RESULT, FALSE, BattleFrontier_Lounge7_EventScript_CancelChooseMon
	msgbox BattleFrontier_Lounge7_Text_IllTakeBattlePoints, MSGBOX_DEFAULT
	copyvar VAR_0x8004, VAR_0x8008
	special TakeFrontierBattlePoints
	release
	end

BattleFrontier_Lounge7_EventScript_ChooseNewMove::
	goto_if_eq VAR_TEMP_FRONTIER_TUTOR_ID, 0, BattleFrontier_Lounge7_EventScript_ChooseNewLeftTutorMove
	goto BattleFrontier_Lounge7_EventScript_ChooseNewRightTutorMove
	end

BattleFrontier_Lounge7_EventScript_Sailor::
	msgbox BattleFrontier_Lounge7_Text_ThinkLadiesDontGetAlong, MSGBOX_NPC
	end

BattleFrontier_Lounge7_EventScript_Gentleman::
	msgbox BattleFrontier_Lounge7_Text_LadiesWereStrongAndBeautiful, MSGBOX_NPC
	end

BattleFrontier_Lounge7_Text_LeftTutorIntro:
.string "ฮะฮะฮะ!\pดูจากตอนนี้คงไม่รู้หรอก\nแต่เมื่อก่อนฉันเป็นเทรนเนอร์ที่แกร่งมาก.\pใคร ๆ ก็รู้จักฉันในฐานะสาวงาม\nที่แกร่งที่สุดเลยนะ!\p… … … … … …\pอะไรอีกล่ะ?\nไม่เชื่อฉันสินะ.\pฉันไม่เหมือนยายขี้โม้ตรงนั้นหรอก\nฉันมีฝีมือจริง ๆ!\pจะพิสูจน์ให้ดู.\nฉันสอนท่าพิเศษแถมน่ารัก\lให้โปเกมอนของเธอได้.\pแต่บทเรียนของฉันไม่ฟรีนะ.\nจ่ายค่าท่าที่สอนด้วย\lแบทเทิลพอยต์นิดหน่อยเป็นไง?$"

BattleFrontier_Lounge7_Text_LeftTutorWelcomeBack:
.string "ฮะฮะฮะ!\pกลับมาเรียนท่าโปเกมอน\nแบบพิเศษแถมน่ารักอีกแล้วเหรอ?$"

BattleFrontier_Lounge7_Text_TeachWhichMove:
.string "เอาล่ะ ๆ ดูนี่!\nอยากให้ฉันสอนท่าไหน?$"

BattleFrontier_Lounge7_Text_MoveWillBeXBattlePoints:
.string "ท่า {STR_VAR_1} สินะ?\nต้องใช้ {STR_VAR_2} แบทเทิลพอยต์ ตกลงไหม?$"

BattleFrontier_Lounge7_Text_TeachMoveToWhichMon:
.string "เอาล่ะ ๆ ทีนี้เลือกโปเกมอน\nที่จะให้ฉันสอนท่านี้.$"

BattleFrontier_Lounge7_Text_HaventGotEnoughPoints:
.string "อะไรเนี่ย…\nแบทเทิลพอยต์ไม่พอนี่นา!$"

BattleFrontier_Lounge7_Text_IllTakeBattlePoints:
.string "เห็นฝีมือฉันแล้วใช่ไหม?\nงั้นขอรับแบทเทิลพอยต์ไปล่ะนะ!$"

BattleFrontier_Lounge7_Text_YouDontWantTo:
.string "ว่าไงนะ?\nไม่เอาเหรอ…\pถ้าอยากเห็นฝีมือฉันเมื่อไร\nก็แวะมาได้ตลอดเลย!$"

BattleFrontier_Lounge7_Text_RightTutorIntro:
.string "หึหึหึ!\pตอนนี้อาจดูไม่ออก แต่เมื่อก่อน\nฉันเป็นเทรนเนอร์ชั้นยอดเลยนะ.\pใคร ๆ ก็รู้จักฉันในฐานะนักว่ายน้ำ\nผู้ไร้เทียมทานที่สุดเลยล่ะ!\p… … … … … …\pเป็นอะไรไป?\nไม่เชื่อฉันสินะ.\pฉันไม่เหมือนยายตัวตลกตรงนั้นหรอก\nฉันมีประสบการณ์จริง ๆ!\pฉันพิสูจน์ให้ดูได้.\nฉันสอนท่าหนักแน่นแต่สวยงาม\lให้โปเกมอนของเธอได้.\pแต่บทเรียนของฉันไม่ฟรีนะ.\nจ่ายค่าท่าที่สอนด้วย\lแบทเทิลพอยต์นิดหน่อยเป็นไง?$"

BattleFrontier_Lounge7_Text_RightTutorWelcomeBack:
.string "หึหึหึ!\pมาเรียนท่าโปเกมอน\nแบบหนักแน่นแต่สวยงามเหรอ?$"

BattleFrontier_Lounge7_Text_ThinkLadiesDontGetAlong:
.string "สองคนนั้นชอบเหน็บแนมกัน\nจนคงคิดว่าพวกเธอ\lไม่ถูกกันใช่ไหม.\pแต่ถ้าเป็นแบบนั้นจริง ก็คงไม่\nมายืนอยู่ด้วยกันตรงนี้หรอก จริงไหม?$"

BattleFrontier_Lounge7_Text_LadiesWereStrongAndBeautiful:
.string "ตอนฉันยังเป็นเด็กตัวเล็ก ๆ\nสองคนนั้นทั้งแกร่งและงดงามมาก.\pพวกเธอเป็นไอดอลของเหล่าเทรนเนอร์.\pแม้ตอนนี้ อายุจะเพิ่มขึ้น แต่\nฝีมือของพวกเธอก็ไม่ได้ลดลง.\pจริง ๆ แล้ว ท่าของโปเกมอนพวกเธอ\nยิ่งขัดเกลาจนเฉียบคมกว่าเดิม.\pแต่… ไม่รู้ทำไม ฉันอดรู้สึกไม่ได้\nว่า…\pกาลเวลาช่างโหดร้ายจริง ๆ…$"

BattleFrontier_Lounge7_Text_SoftboiledDesc::
.string "ฟื้น HP ได้\nสูงสุดครึ่งหนึ่งของ\nHP สูงสุดของผู้ใช้.$"

BattleFrontier_Lounge7_Text_SeismicTossDesc::
.string "สร้างความเสียหาย\nเท่ากับเลเวล\nของผู้ใช้.$"

BattleFrontier_Lounge7_Text_DreamEaterDesc::
.string "ฟื้น HP ครึ่งหนึ่ง\nของความเสียหายที่ทำ\nกับคู่ต่อสู้ที่หลับอยู่.$"

BattleFrontier_Lounge7_Text_MegaPunchDesc::
.string "หมัดทรงพลัง\nที่ปล่อยออกมาด้วย\nพลังมหาศาล.$"

BattleFrontier_Lounge7_Text_MegaKickDesc::
.string "ลูกเตะที่\nทรงพลังอย่างยิ่ง\nด้วยแรงมหาศาล.$"

BattleFrontier_Lounge7_Text_BodySlamDesc::
.string "พุ่งชนด้วยทั้งตัว\nและอาจทำให้\nเป็นอัมพาต.$"

BattleFrontier_Lounge7_Text_RockSlideDesc::
.string "ขว้างก้อนหินใหญ่\nใส่คู่ต่อสู้ อาจ\nทำให้ชะงัก.$"

BattleFrontier_Lounge7_Text_CounterDesc::
.string "โต้กลับการโจมตี\nกายภาพด้วยพลัง\nเป็นสองเท่า.$"

BattleFrontier_Lounge7_Text_ThunderWaveDesc::
.string "ปล่อยกระแสไฟ\nอ่อน ๆ ที่ทำให้\nคู่ต่อสู้เป็นอัมพาต.$"

BattleFrontier_Lounge7_Text_SwordsDanceDesc::
.string "ระบำต่อสู้\nที่เพิ่ม ATTACK\nอย่างมาก.$"

BattleFrontier_Lounge7_Text_DefenseCurlDesc::
.string "ม้วนตัวเพื่อ\nซ่อนจุดอ่อนและ\nเพิ่ม DEFENSE.$"

BattleFrontier_Lounge7_Text_SnoreDesc::
.string "โจมตีด้วยเสียงดัง\nใช้ได้เฉพาะตอน\nกำลังหลับ.$"

BattleFrontier_Lounge7_Text_MudSlapDesc::
.string "สาดโคลนใส่\nหน้าคู่ต่อสู้เพื่อ\nลดความแม่นยำ.$"

BattleFrontier_Lounge7_Text_SwiftDesc::
.string "ปล่อยลำแสง\nรูปดาวที่\nไม่มีวันพลาด.$"

BattleFrontier_Lounge7_Text_IcyWindDesc::
.string "โจมตีด้วยความเย็น\nพร้อมลด SPEED\nของคู่ต่อสู้.$"

BattleFrontier_Lounge7_Text_EndureDesc::
.string "ทนการโจมตีใด ๆ\nได้ 1 เทิร์น\nโดยเหลือ HP 1.$"

BattleFrontier_Lounge7_Text_PsychUpDesc::
.string "คัดลอกผลที่เกิด\nกับคู่ต่อสู้มา\nใช้กับตัวเอง.$"

BattleFrontier_Lounge7_Text_IcePunchDesc::
.string "หมัดเยือกแข็ง\nที่อาจทำให้\nคู่ต่อสู้แข็งตัว.$"

BattleFrontier_Lounge7_Text_ThunderPunchDesc::
.string "หมัดชาร์จไฟ\nที่อาจทำให้\nคู่ต่อสู้เป็นอัมพาต.$"

BattleFrontier_Lounge7_Text_FirePunchDesc::
.string "หมัดเพลิง\nที่อาจทำให้\nคู่ต่อสู้ถูกเผาไหม้.$"
