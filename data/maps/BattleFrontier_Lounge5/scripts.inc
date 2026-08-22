BattleFrontier_Lounge5_MapScripts::
	.byte 0

BattleFrontier_Lounge5_EventScript_NatureGirl::
	lock
	faceplayer
	msgbox BattleFrontier_Lounge5_Text_NatureGirlGreeting, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, BattleFrontier_Lounge5_EventScript_NatureGirlNoneShown
	special ChoosePartyMon
	lock
	faceplayer
	goto_if_eq VAR_0x8004, PARTY_NOTHING_CHOSEN, BattleFrontier_Lounge5_EventScript_NatureGirlNoneShown
	specialvar VAR_RESULT, ScriptGetPartyMonSpecies
	goto_if_eq VAR_RESULT, SPECIES_EGG, BattleFrontier_Lounge5_EventScript_NatureGirlEgg
	special ShowNatureGirlMessage
	waitmessage
	waitbuttonpress
	release
	end

BattleFrontier_Lounge5_EventScript_NatureGirlEgg::
	msgbox BattleFrontier_Lounge5_Text_NatureGirlEgg, MSGBOX_DEFAULT
	release
	end

BattleFrontier_Lounge5_EventScript_NatureGirlNoneShown::
	msgbox BattleFrontier_Lounge5_Text_NatureGirlNoneShown, MSGBOX_DEFAULT
	release
	end

BattleFrontier_Lounge5_EventScript_Gentleman::
	msgbox BattleFrontier_Lounge5_Text_LadyClaimsSheUnderstandsPokemon, MSGBOX_NPC
	end

BattleFrontier_Lounge5_EventScript_BlackBelt::
	msgbox BattleFrontier_Lounge5_Text_GirlSayingSomethingProfound, MSGBOX_NPC
	end

BattleFrontier_Lounge5_EventScript_LittleBoy::
	msgbox BattleFrontier_Lounge5_Text_GirlPlaysAtRedHouseALot, MSGBOX_NPC
	end

BattleFrontier_Lounge5_Text_NatureGirlGreeting::
.string "ฮิฮิ!\nฉันรู้ว่าโปเกมอนกำลังคิดอะไรอยู่!\pขอร้องล่ะ!\nขอดูโปเกมอนของเธอหน่อยได้ไหม?$"

BattleFrontier_Lounge5_Text_NatureGirlNoneShown::
.string "โธ่!\nขี้เหนียวจัง!$"

BattleFrontier_Lounge5_Text_NatureGirlHardy::
.string "อืม…\pตัวนี้บอกว่าชอบสู้!\nถึงจะเจ็บมาก ๆ\lก็ยังสู้ต่อ!$"

BattleFrontier_Lounge5_Text_NatureGirlLonely::
.string "อืม…\pตัวนี้บอกว่าชอบใช้ลูกเล่น!\nแต่ถ้าเจ็บมากพอ\lก็จะหันมาเอาคืน!$"

BattleFrontier_Lounge5_Text_NatureGirlBrave::
.string "อืม…\pตัวนี้บอกว่าชอบสู้!\nแต่ถ้าเจ็บมากพอ\lก็จะเริ่มห่วงตัวเอง!$"

BattleFrontier_Lounge5_Text_NatureGirlAdamant::
.string "อืม…\pตัวนี้บอกว่าชอบสู้!\nถึงจะเจ็บมาก ๆ\lก็ยังสู้ต่อ!$"

BattleFrontier_Lounge5_Text_NatureGirlNaughty::
.string "อืม…\pตัวนี้บอกว่าชอบดูแลตัวเอง!\nแต่ถ้าเจ็บมากพอ\lก็จะหันมาเอาคืน!$"

BattleFrontier_Lounge5_Text_NatureGirlBold::
.string "อืม…\pตัวนี้บอกว่าชอบใช้ลูกเล่น!\nแต่ถ้าเจ็บมากพอ\lก็จะเริ่มห่วงตัวเอง!$"

BattleFrontier_Lounge5_Text_NatureGirlDocileNaiveQuietQuirky::
.string "อืม…\pตัวนี้บอกว่าชอบสู้!\nถึงจะเจ็บมาก ๆ\lก็ยังสู้ต่อ!$"

BattleFrontier_Lounge5_Text_NatureGirlRelaxed::
.string "อืม…\pตัวนี้บอกว่าชอบใช้ลูกเล่น!\nแต่ถ้าเจ็บมากพอ\lก็จะหันมาเอาคืน!$"

BattleFrontier_Lounge5_Text_NatureGirlImpish::
.string "อืม…\pตัวนี้บอกว่าชอบสู้!\nแต่ถ้าเจ็บมากพอ\lก็จะเริ่มห่วงตัวเอง!$"

BattleFrontier_Lounge5_Text_NatureGirlLax::
.string "อืม…\pตัวนี้บอกว่าชอบใช้ลูกเล่น!\nต่อให้เจ็บมาก ๆ\lก็ยังใช้ลูกเล่นเหมือนเดิม!$"

BattleFrontier_Lounge5_Text_NatureGirlTimid::
.string "อืม…\pตัวนี้บอกว่าชอบสู้!\nแต่ถ้าเจ็บมากพอ\lก็จะหันมาใช้ลูกเล่น!$"

BattleFrontier_Lounge5_Text_NatureGirlHasty::
.string "อืม…\pตัวนี้บอกว่าชอบสู้!\nถึงจะเจ็บมาก ๆ\lก็ยังสู้ต่อ!$"

BattleFrontier_Lounge5_Text_NatureGirlSerious::
.string "อืม…\pตัวนี้บอกว่าชอบใช้ลูกเล่น!\nต่อให้เจ็บมาก ๆ\lก็ยังใช้ลูกเล่นเหมือนเดิม!$"

BattleFrontier_Lounge5_Text_NatureGirlJolly::
.string "อืม…\pตัวนี้บอกว่าชอบใช้ลูกเล่น!\nแต่ถ้าเจ็บมากพอ\lก็จะเริ่มห่วงตัวเอง!$"

BattleFrontier_Lounge5_Text_NatureGirlModest::
.string "อืม…\pตัวนี้บอกว่าชอบดูแลตัวเอง!\nไม่ว่าจะเจ็บมากหรือไม่\lก็ยังคอยห่วงตัวเองอยู่!$"

BattleFrontier_Lounge5_Text_NatureGirlMild::
.string "อืม…\pตัวนี้บอกว่าชอบดูแลตัวเอง!\nแต่ถ้าเจ็บมากพอ\lก็จะหันมาใช้ลูกเล่น!$"

BattleFrontier_Lounge5_Text_NatureGirlBashful::
.string "อืม…\pตัวนี้บอกว่าชอบดูแลตัวเอง!\nถึงจะเจ็บมาก ๆ\lก็ยังคอยห่วงตัวเองอยู่!$"

BattleFrontier_Lounge5_Text_NatureGirlRash::
.string "อืม…\pตัวนี้บอกว่าชอบใช้ลูกเล่น!\nต่อให้เจ็บมาก ๆ\lก็ยังใช้ลูกเล่นเหมือนเดิม!$"

BattleFrontier_Lounge5_Text_NatureGirlCalm::
.string "อืม…\pตัวนี้บอกว่าชอบดูแลตัวเอง!\nถึงจะเจ็บมาก ๆ\lก็ยังคอยห่วงตัวเองอยู่!$"

BattleFrontier_Lounge5_Text_NatureGirlGentle::
.string "อืม…\pตัวนี้บอกว่าชอบดูแลตัวเอง!\nแต่ถ้าเจ็บมากพอ\lก็จะหันมาเอาคืน!$"

BattleFrontier_Lounge5_Text_NatureGirlSassy::
.string "อืม…\pตัวนี้บอกว่าชอบสู้!\nแต่ถ้าเจ็บมากพอ\lก็จะหันมาใช้ลูกเล่น!$"

BattleFrontier_Lounge5_Text_NatureGirlCareful::
.string "อืม…\pตัวนี้บอกว่าชอบดูแลตัวเอง!\nแต่ถ้าเจ็บมากพอ\lก็จะหันมาใช้ลูกเล่น!$"

BattleFrontier_Lounge5_Text_NatureGirlEgg::
.string "แบบนั้นไม่ได้สิ! ไข่กำลังหลับอยู่!\nฉันคุยกับมันไม่ได้หรอก!$"

BattleFrontier_Lounge5_Text_LadyClaimsSheUnderstandsPokemon::
.string "น่ารักจริง ๆ!\nเด็กผู้หญิงตัวน้อยคนนั้นบอกว่า\lเข้าใจภาษาโปเกมอนด้วยนะ!$"

BattleFrontier_Lounge5_Text_GirlSayingSomethingProfound::
.string "ฉันรู้สึกว่าเด็กคนนั้น\nกำลังพูดอะไรที่ลึกซึ้งมากเลย.$"

BattleFrontier_Lounge5_Text_GirlPlaysAtRedHouseALot::
.string "ฉันรู้อะไรอย่างหนึ่ง!\pเด็กคนนั้นไปเล่นที่บ้านสีแดง\nบ่อยมากเลย!$"

