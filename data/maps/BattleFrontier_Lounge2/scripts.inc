BattleFrontier_Lounge2_MapScripts::
	.byte 0

@ This NPC gives hints about a random facility or battle mode.
@ For battle modes he gives generic advice
@ For facilities, depending on how far the player has progressed he will say either
@    The name of the Frontier Brain there
@    The type and description of the 3 pokemon they use in their silver battle
@    The type and description of the 3 pokemon they use in their gold battle
BattleFrontier_Lounge2_EventScript_FrontierManiac::
	lock
	faceplayer
	goto_if_set FLAG_MET_BATTLE_FRONTIER_MANIAC, BattleFrontier_Lounge2_EventScript_AlreadyMetManiac
	setflag FLAG_MET_BATTLE_FRONTIER_MANIAC
	msgbox BattleFrontier_Lounge2_Text_FrontierManiacIntro, MSGBOX_DEFAULT
	goto BattleFrontier_Lounge2_EventScript_GiveAdvice
	end

BattleFrontier_Lounge2_EventScript_AlreadyMetManiac::
	msgbox BattleFrontier_Lounge2_Text_SwingByForTheLatestWord, MSGBOX_DEFAULT
	goto BattleFrontier_Lounge2_EventScript_GiveAdvice
	end

BattleFrontier_Lounge2_EventScript_GiveAdvice::
	call_if_eq VAR_FRONTIER_MANIAC_FACILITY, FRONTIER_MANIAC_TOWER_SINGLES, BattleFrontier_Lounge2_EventScript_BufferSingle
	call_if_eq VAR_FRONTIER_MANIAC_FACILITY, FRONTIER_MANIAC_TOWER_DOUBLES, BattleFrontier_Lounge2_EventScript_BufferDouble
	call_if_eq VAR_FRONTIER_MANIAC_FACILITY, FRONTIER_MANIAC_TOWER_MULTIS, BattleFrontier_Lounge2_EventScript_BufferMulti
	call_if_eq VAR_FRONTIER_MANIAC_FACILITY, FRONTIER_MANIAC_TOWER_LINK, BattleFrontier_Lounge2_EventScript_BufferMultiLink
	call_if_eq VAR_FRONTIER_MANIAC_FACILITY, FRONTIER_MANIAC_DOME, BattleFrontier_Lounge2_EventScript_BufferBattleDome
	call_if_eq VAR_FRONTIER_MANIAC_FACILITY, FRONTIER_MANIAC_FACTORY, BattleFrontier_Lounge2_EventScript_BufferBattleFactory
	call_if_eq VAR_FRONTIER_MANIAC_FACILITY, FRONTIER_MANIAC_PALACE, BattleFrontier_Lounge2_EventScript_BufferBattlePalace
	call_if_eq VAR_FRONTIER_MANIAC_FACILITY, FRONTIER_MANIAC_ARENA, BattleFrontier_Lounge2_EventScript_BufferBattleArena
	call_if_eq VAR_FRONTIER_MANIAC_FACILITY, FRONTIER_MANIAC_PIKE, BattleFrontier_Lounge2_EventScript_BufferBattlePike
	call_if_eq VAR_FRONTIER_MANIAC_FACILITY, FRONTIER_MANIAC_PYRAMID, BattleFrontier_Lounge2_EventScript_BufferBattlePyramid
@ <= FRONTIER_MANIAC_TOWER_LINK is any Battle Tower mode
	call_if_le VAR_FRONTIER_MANIAC_FACILITY, FRONTIER_MANIAC_TOWER_LINK, BattleFrontier_Lounge2_EventScript_BattleTowerNews
@ >= FRONTIER_MANIAC_DOME is any facility other than Battle Tower
	call_if_ge VAR_FRONTIER_MANIAC_FACILITY, FRONTIER_MANIAC_DOME, BattleFrontier_Lounge2_EventScript_FacilityNews
	special ShowFrontierManiacMessage
	waitmessage
	waitbuttonpress
	release
	end

BattleFrontier_Lounge2_EventScript_BattleTowerNews::
	msgbox BattleFrontier_Lounge2_Text_BattleTowerIsHottest, MSGBOX_DEFAULT
	return

BattleFrontier_Lounge2_EventScript_FacilityNews::
	msgbox BattleFrontier_Lounge2_Text_FacilityIsHottest, MSGBOX_DEFAULT
	return

BattleFrontier_Lounge2_EventScript_BufferSingle::
	bufferstdstring STR_VAR_1, STDSTRING_SINGLE
	return

BattleFrontier_Lounge2_EventScript_BufferDouble::
	bufferstdstring STR_VAR_1, STDSTRING_DOUBLE
	return

BattleFrontier_Lounge2_EventScript_BufferMulti::
	bufferstdstring STR_VAR_1, STDSTRING_MULTI
	return

BattleFrontier_Lounge2_EventScript_BufferMultiLink::
	bufferstdstring STR_VAR_1, STDSTRING_MULTI_LINK
	return

BattleFrontier_Lounge2_EventScript_BufferBattleDome::
	bufferstdstring STR_VAR_1, STDSTRING_BATTLE_DOME
	return

BattleFrontier_Lounge2_EventScript_BufferBattleFactory::
	bufferstdstring STR_VAR_1, STDSTRING_BATTLE_FACTORY
	return

BattleFrontier_Lounge2_EventScript_BufferBattlePalace::
	bufferstdstring STR_VAR_1, STDSTRING_BATTLE_PALACE
	return

BattleFrontier_Lounge2_EventScript_BufferBattleArena::
	bufferstdstring STR_VAR_1, STDSTRING_BATTLE_ARENA
	return

BattleFrontier_Lounge2_EventScript_BufferBattlePike::
	bufferstdstring STR_VAR_1, STDSTRING_BATTLE_PIKE
	return

BattleFrontier_Lounge2_EventScript_BufferBattlePyramid::
	bufferstdstring STR_VAR_1, STDSTRING_BATTLE_PYRAMID
	return

BattleFrontier_Lounge2_EventScript_Maniac1::
	lock
	msgbox BattleFrontier_Lounge2_Text_NewsGatheringPower, MSGBOX_DEFAULT
	release
	end

BattleFrontier_Lounge2_EventScript_Maniac2::
	lock
	msgbox BattleFrontier_Lounge2_Text_AmazingPowersOfObservation, MSGBOX_DEFAULT
	release
	end

BattleFrontier_Lounge2_EventScript_Maniac3::
	lock
	msgbox BattleFrontier_Lounge2_Text_AmazingPowerOfPersuasion, MSGBOX_DEFAULT
	release
	end

BattleFrontier_Lounge2_EventScript_TriathleteF::
	msgbox BattleFrontier_Lounge2_Text_ThisPlaceIsScaringMe, MSGBOX_NPC
	end

BattleFrontier_Lounge2_Text_FrontierManiacIntro::
.string "ว่าไง! ถ้าเป็นข่าวเรื่อง\nแบทเทิลฟรอนเทียร์ ฉันคือเบอร์หนึ่ง.\pจะเรียกฉันว่า\nฟรอนเทียร์มาเนียกก็ได้.\pขอถามให้แน่ใจ เธอเป็นเทรนเนอร์\nใช่ไหม?\pฉันยินดีเล่าข่าวเด็ดล่าสุด\nที่รวบรวมมาจากแบทเทิลฟรอนเทียร์.$"

BattleFrontier_Lounge2_Text_SwingByForTheLatestWord::
.string "ว่าไง! แวะมาซักฉันเรื่อง\nข่าวล่าสุดสินะ? ได้เลย!$"

@ Unused
BattleFrontier_Lounge2_Text_MyInformationsBeenUsefulRight::
.string "เป็นไง? เป็นไง? เป็นไง?\pข้อมูลของฉันมีประโยชน์\nกับเธอมากเลยใช่ไหม?$"

BattleFrontier_Lounge2_Text_FacilityIsHottest::
.string "ขอดูก่อนนะ…\pได้ยินว่าตอนนี้ {STR_VAR_1}\nกำลังฮิตที่สุดเลย.$"

BattleFrontier_Lounge2_Text_BattleTowerIsHottest::
.string "ขอดูก่อนนะ…\pได้ยินว่าตอนนี้แบทเทิลทาวเวอร์\n{STR_VAR_1} กำลังฮิตที่สุด.$"

BattleFrontier_Lounge2_Text_SalonMaidenIsThere::
.string "พนันได้เลยว่าเธอยังไม่รู้!\pหนึ่งในยอดเทรนเนอร์ที่สก็อตต์\nเรียกว่าฟรอนเทียร์เบรนอยู่ที่นั่น.\pผู้ดูแลคือเทรนเนอร์ลึกลับ\nที่เรียกกันว่า ซาลอนเมเดน.$"

BattleFrontier_Lounge2_Text_SalonMaidenSilverMons::
.string "เคยสู้กับซาลอนเมเดนหรือยัง?\pตอนที่เธอกำลังหยั่งเชิงคู่ต่อสู้\nได้ยินว่าเธอใช้โปเกมอนเหล่านี้:\pโปเกมอนพลังจิต ประเภท PSYCHIC,\nโปเกมอนภูเขาไฟ ประเภท FIRE,\lและโปเกมอนจอมหลับ ประเภท NORMAL.$"

BattleFrontier_Lounge2_Text_SalonMaidenGoldMons::
.string "เคยสู้กับซาลอนเมเดน\nตอนที่เธอเอาจริงหรือยัง?\pตอนที่สู้เต็มกำลัง\nได้ยินว่าเธอใช้โปเกมอนเหล่านี้:\pโปเกมอนอีออน ประเภท DRAGON & PSYCHIC,\nโปเกมอนสายฟ้า ประเภท ELECTRIC,\lและโปเกมอนจอมหลับ ประเภท NORMAL.$"

BattleFrontier_Lounge2_Text_DomeAceIsThere::
.string "พนันได้เลยว่าเธอยังไม่รู้!\pหนึ่งในยอดเทรนเนอร์ที่สก็อตต์\nเรียกว่าฟรอนเทียร์เบรนอยู่ที่นั่น.\pผู้ดูแลคือเทรนเนอร์สุดฉูดฉาด\nที่เรียกกันว่า โดมเอซ.$"

BattleFrontier_Lounge2_Text_DomeAceSilverMons::
.string "เคยสู้กับโดมเอซหรือยัง?\pตอนที่เขายังไม่เอาจริงกับคู่ต่อสู้\nเขาใช้โปเกมอนสามตัวนี้:\pโปเกมอนมังกร ประเภท DRAGON & FLYING,\nโปเกมอนปลาโคลน ประเภท WATER & GROUND,\lและโปเกมอนเปลวไฟ ประเภท FIRE & FLYING.$"

BattleFrontier_Lounge2_Text_DomeAceGoldMons::
.string "เคยสู้กับโดมเอซ\nตอนที่เขาเอาจริงหรือยัง?\pตอนที่เขาแสดงกลยุทธ์เต็มที่\nเขาใช้โปเกมอนสามตัวนี้:\pโปเกมอนอีออน ประเภท DRAGON & FLYING,\nโปเกมอนปลาโคลน ประเภท WATER & GROUND,\lและโปเกมอนขาเหล็ก ประเภท\lSTEEL & PSYCHIC.$"

BattleFrontier_Lounge2_Text_FactoryHeadIsThere::
.string "พนันได้เลยว่าเธอยังไม่รู้!\pหนึ่งในยอดเทรนเนอร์ที่สก็อตต์\nเรียกว่าฟรอนเทียร์เบรนอยู่ที่นั่น.\pผู้ดูแลคือเทรนเนอร์สุดประหลาด\nที่เรียกกันว่า แฟกทอรีเฮด.$"

BattleFrontier_Lounge2_Text_FactoryHeadSilverMons::
.string "เคยสู้กับแฟกทอรีเฮด\nมาแล้วหรือยัง?\pขอคิดก่อน… เวลาเขาลงสู้\nเขาจะใช้โปเกมอนเช่าสามตัว.\pเงื่อนไขการต่อสู้ของเขา\nแทบจะเหมือนกับของเธอเลย.$"

BattleFrontier_Lounge2_Text_FactoryHeadGoldMons::
.string "เคยสู้กับแฟกทอรีเฮด\nตอนที่เขาเอาจริงหรือยัง?\pถึงจะเอาจริง เขาก็ยังใช้\nโปเกมอนเช่าสามตัวเหมือนเดิม.\pเงื่อนไขการต่อสู้ของเขา\nแทบจะเหมือนกับของเธอเลย.$"

BattleFrontier_Lounge2_Text_PikeQueenIsThere::
.string "พนันได้เลยว่าเธอยังไม่รู้!\pหนึ่งในยอดเทรนเนอร์ที่สก็อตต์\nเรียกว่าฟรอนเทียร์เบรนอยู่ที่นั่น.\pผู้ดูแลคือเทรนเนอร์สุดน่ากลัว\nที่เรียกกันว่า ไพค์ควีน.$"

BattleFrontier_Lounge2_Text_PikeQueenSilverMons::
.string "เคยสู้กับไพค์ควีน\nมาก่อนหรือยัง?\pเขาว่าตอนที่เธออารมณ์ดี\nเธอใช้โปเกมอนสามตัวนี้:\pโปเกมอนงูเขี้ยว ประเภท POISON,\nโปเกมอนรา ประเภท BUG & ROCK,\lและโปเกมอนอ่อนโยน ประเภท WATER.$"

BattleFrontier_Lounge2_Text_PikeQueenGoldMons::
.string "เคยสู้กับไพค์ควีน\nตอนที่เธอเอาจริงหรือยัง?\pเขาว่าตอนที่เธอโมโหจริงจัง\nเธอใช้โปเกมอนสามตัวนี้:\pโปเกมอนงูเขี้ยว ประเภท POISON,\nโปเกมอนงูเหล็ก ประเภท STEEL & GROUND,\lและโปเกมอนโหดเหี้ยม ประเภท\lWATER & FLYING.$"

BattleFrontier_Lounge2_Text_ArenaTycoonIsThere::
.string "พนันได้เลยว่าเธอยังไม่รู้!\pหนึ่งในยอดเทรนเนอร์ที่สก็อตต์\nเรียกว่าฟรอนเทียร์เบรนอยู่ที่นั่น.\pผู้ดูแลคือเทรนเนอร์สุดน่ารัก\nที่เรียกกันว่า อารีนาไทคูน.$"

BattleFrontier_Lounge2_Text_ArenaTycoonSilverMons::
.string "เคยสู้กับอารีนาไทคูน\nมาก่อนหรือยัง?\pตอนที่เธอกำลังประเมินฝีมือคู่ต่อสู้\nได้ยินว่าเธอใช้โปเกมอนเหล่านี้:\pโปเกมอนเขาเดี่ยว ประเภท BUG & FIGHTING,\nโปเกมอนแสงจันทร์ ประเภท DARK,\lและโปเกมอนเปลือกคราบ ประเภท BUG & GHOST.$"

BattleFrontier_Lounge2_Text_ArenaTycoonGoldMons::
.string "เคยสู้กับอารีนาไทคูน\nตอนที่เธอเอาจริงหรือยัง?\pตอนที่เธอสู้แบบเอาเป็นเอาตาย\nได้ยินว่าเธอใช้โปเกมอนเหล่านี้:\pโปเกมอนแสงจันทร์ ประเภท DARK,\nโปเกมอนเงา ประเภท GHOST & POISON,\lและโปเกมอนเห็ด ประเภท\lGRASS & FIGHTING.$"

BattleFrontier_Lounge2_Text_PalaceMavenIsThere::
.string "พนันได้เลยว่าเธอยังไม่รู้!\pหนึ่งในยอดเทรนเนอร์ที่สก็อตต์\nเรียกว่าฟรอนเทียร์เบรนอยู่ที่นั่น.\pผู้ดูแลคือเทรนเนอร์บรรยากาศน่ากลัว\nที่เรียกกันว่า พาเลซมาเวน.$"

BattleFrontier_Lounge2_Text_PalaceMavenSilverMons::
.string "เคยสู้กับพาเลซมาเวน\nมาก่อนหรือยัง?\pตอนที่เขาทดสอบจิตใจคู่ต่อสู้\nได้ยินว่าเขาใช้โปเกมอนเหล่านี้:\pโปเกมอนค้างคาว ประเภท POISON & FLYING,\nโปเกมอนจอมขี้เกียจ ประเภท NORMAL และ\lโปเกมอนขนส่ง ประเภท WATER & ICE.$"

BattleFrontier_Lounge2_Text_PalaceMavenGoldMons::
.string "เคยสู้กับพาเลซมาเวน\nตอนที่เขาเอาจริงหรือยัง?\pตอนที่เขาทุ่มพลังทั้งหมดเข้าสู้\nได้ยินว่าเขาใช้โปเกมอนเหล่านี้:\pโปเกมอนในตำนาน ประเภท FIRE,\nโปเกมอนจอมขี้เกียจ ประเภท NORMAL,\lและโปเกมอนออโรรา ประเภท WATER.$"

BattleFrontier_Lounge2_Text_PyramidKingIsThere::
.string "พนันได้เลยว่าเธอยังไม่รู้!\pหนึ่งในยอดเทรนเนอร์ที่สก็อตต์\nเรียกว่าฟรอนเทียร์เบรนอยู่ที่นั่น.\pผู้ดูแลคือเทรนเนอร์เลือดร้อน\nที่เรียกกันว่า พีระมิดคิง.$"

BattleFrontier_Lounge2_Text_PyramidKingSilverMons::
.string "เคยสู้กับพีระมิดคิง\nมาก่อนหรือยัง?\pตอนที่เขากำลังวัดพลังคู่ต่อสู้\nได้ยินว่าเขาใช้โปเกมอนเหล่านี้:\pโปเกมอนยอดหิน ประเภท ROCK,\nโปเกมอนภูเขาน้ำแข็ง ประเภท ICE,\lและโปเกมอนเหล็ก ประเภท STEEL.$"

BattleFrontier_Lounge2_Text_PyramidKingGoldMons::
.string "เคยสู้กับพีระมิดคิง\nตอนที่เขาเอาจริงหรือยัง?\pตอนที่พลังร้อนแรงพลุ่งพล่าน\nได้ยินว่าเขาใช้โปเกมอนเหล่านี้:\pโปเกมอนเยือกแข็ง ประเภท ICE & FLYING,\nโปเกมอนไฟฟ้า ประเภท ELECTRIC & FLYING,\lและโปเกมอนเปลวไฟ ประเภท\lFIRE & FLYING.$"

BattleFrontier_Lounge2_Text_DoubleBattleAdvice1::
.string "แน่นอน มีหลายแห่งที่เข้า\nดับเบิลแบทเทิลได้.\pแต่ห้องดับเบิลแบทเทิลของ\nแบทเทิลทาวเวอร์น่ะ เป็นพื้นฐานเลย!\pเหมาะสำหรับเรียนรู้ว่า\nดับเบิลแบทเทิลที่แบทเทิลฟรอนเทียร์\lเล่นกันยังไง.$"

BattleFrontier_Lounge2_Text_DoubleBattleAdvice2::
.string "เวลาแบทเทิลที่นี่ต้องระวังให้ดี.\pได้ยินว่ามีเทรนเนอร์ที่คิด\nกลยุทธ์ขึ้นมาโดยเฉพาะสำหรับ\lดับเบิลแบทเทิลเลยนะ.$"

BattleFrontier_Lounge2_Text_DoubleBattleAdvice3::
.string "ถ้ามั่นใจและคุ้นเคยกับ\nดับเบิลแบทเทิลที่นี่แล้ว ก็น่าจะ\lลองท้าสถานที่อื่นที่มี\lดับเบิลแบทเทิลดูนะ.$"

BattleFrontier_Lounge2_Text_MultiBattleAdvice::
.string "มีเทรนเนอร์สารพัดแบบมารวมตัวกัน\nที่แบทเทิลซาลอน.\pลองคิดดูสิ อาจได้เจอ\nเพื่อนหรือคนรู้จักของเธอก็ได้!\lลองมองหาให้ดีนะ!$"

BattleFrontier_Lounge2_Text_LinkMultiBattleAdvice::
.string "ถ้ามากับเพื่อน ให้ไปที่\nห้องลิงก์มัลติแบทเทิล.\pถ้าเล่นกับเพื่อนที่เก่ง\nก็เตรียมเจอคู่ต่อสู้สุดแกร่งได้เลย!$"

BattleFrontier_Lounge2_Text_NewsGatheringPower::
.string "พลังรวบรวมข่าวสุดยอดจริง ๆ!\nสมกับเป็นอาจารย์ของฉัน!$"

BattleFrontier_Lounge2_Text_AmazingPowersOfObservation::
.string "ช่างสังเกตสุดยอดจริง ๆ!\nสมกับเป็นอาจารย์ของฉัน!$"

BattleFrontier_Lounge2_Text_AmazingPowerOfPersuasion::
.string "พลังโน้มน้าวสุดยอดจริง ๆ!\nสมกับเป็นอาจารย์ของฉัน!$"

BattleFrontier_Lounge2_Text_ThisPlaceIsScaringMe::
.string "…ที่นี่มันอะไรกัน?\nชักน่ากลัวแล้วสิ…$"

