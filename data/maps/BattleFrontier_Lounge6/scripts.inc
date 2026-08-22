BattleFrontier_Lounge6_MapScripts::
	.byte 0

BattleFrontier_Lounge6_EventScript_Trader::
	lock
	faceplayer
	goto_if_set FLAG_BATTLE_FRONTIER_TRADE_DONE, BattleFrontier_Lounge6_EventScript_TradeCompleted
	setvar VAR_0x8008, INGAME_TRADE_MEOWTH
	copyvar VAR_0x8004, VAR_0x8008
	specialvar VAR_RESULT, GetInGameTradeSpeciesInfo
	copyvar VAR_0x8009, VAR_RESULT
	msgbox BattleFrontier_Lounge6_Text_WouldYouLikeToTrade, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, BattleFrontier_Lounge6_EventScript_DeclineTrade
	special ChoosePartyMon
	copyvar VAR_0x800A, VAR_0x8004
	goto_if_eq VAR_0x8004, PARTY_NOTHING_CHOSEN, BattleFrontier_Lounge6_EventScript_DeclineTrade
	copyvar VAR_0x8005, VAR_0x800A
	specialvar VAR_RESULT, GetTradeSpecies
	copyvar VAR_0x800B, VAR_RESULT
	goto_if_ne VAR_RESULT, VAR_0x8009, BattleFrontier_Lounge6_EventScript_NotRequestedMon
	copyvar VAR_0x8004, VAR_0x8008
	copyvar VAR_0x8005, VAR_0x800A
	special CreateInGameTradePokemon
	special DoInGameTradeScene
	msgbox BattleFrontier_Lounge6_Text_PromiseIllBeGoodToIt, MSGBOX_DEFAULT
	setflag FLAG_BATTLE_FRONTIER_TRADE_DONE
	release
	end

BattleFrontier_Lounge6_EventScript_DeclineTrade::
	msgbox BattleFrontier_Lounge6_Text_WellThatsFineToo, MSGBOX_DEFAULT
	release
	end

BattleFrontier_Lounge6_EventScript_NotRequestedMon::
	bufferspeciesname STR_VAR_1, VAR_0x8009
	msgbox BattleFrontier_Lounge6_Text_DontTradeForAnythingButMon, MSGBOX_DEFAULT
	release
	end

BattleFrontier_Lounge6_EventScript_TradeCompleted::
	msgbox BattleFrontier_Lounge6_Text_SkittySoMuchCuterThanImagined, MSGBOX_DEFAULT
	release
	end

BattleFrontier_Lounge6_Text_WouldYouLikeToTrade:
.string "โปเกมอนของฉันคือ {STR_VAR_2}.\nรู้จักไหม?\lน่ารักแล้วก็นิสัยดีมากเลยนะ.\pเจ้าตัวนี้ ฉันภูมิใจพอที่จะ\nยอมแลกให้เลย!\pเอา {STR_VAR_1} ของเธอ\nมาแลกกับ {STR_VAR_2} ของฉันไหม?$"

BattleFrontier_Lounge6_Text_PromiseIllBeGoodToIt:
.string "โอ้ น่ารักจัง!\nขอบคุณนะ!\lฉันสัญญาว่าจะดูแลอย่างดี!\pโอ้! แล้วก็ช่วยดูแล\n{STR_VAR_2} ของฉันให้ดีด้วยนะ!$"

BattleFrontier_Lounge6_Text_DontTradeForAnythingButMon:
.string "โอ้ ขอโทษนะ!\nฉันตั้งใจจะแลกกับ\l{STR_VAR_1} เท่านั้น.$"

BattleFrontier_Lounge6_Text_WellThatsFineToo:
.string "อ้อ ไม่แลกเหรอ?\nไม่เป็นไรจ้ะ.\lไว้แวะมาหาเราอีกนะ.$"

BattleFrontier_Lounge6_Text_SkittySoMuchCuterThanImagined:
.string "ฮิฮิ!\nเอเนโคน่ารักกว่าที่ฉัน\lจินตนาการไว้อีก ดีใจจัง!$"
