BattleFrontier_ExchangeServiceCorner_MapScripts::
	.byte 0

BattleFrontier_ExchangeServiceCorner_EventScript_ClerkWelcome::
	msgbox BattleFrontier_ExchangeServiceCorner_Text_WelcomePleaseChoosePrize, MSGBOX_DEFAULT
	special ShowBattlePointsWindow
	return

BattleFrontier_ExchangeServiceCorner_EventScript_ClerkGoodbye::
	msgbox BattleFrontier_ExchangeServiceCorner_Text_ThankYouVisitWithPoints, MSGBOX_DEFAULT
	special CloseBattlePointsWindow
	release
	end

BattleFrontier_ExchangeServiceCorner_EventScript_TryPurchasePrize::
	specialvar VAR_TEMP_1, GetFrontierBattlePoints
	goto_if_ge VAR_TEMP_1, VAR_0x8008, BattleFrontier_ExchangeServiceCorner_EventScript_TryGivePrize
	msgbox BattleFrontier_ExchangeServiceCorner_Text_DontHaveEnoughPoints, MSGBOX_DEFAULT
	goto_if_eq VAR_TEMP_2, EXCHANGE_CORNER_DECOR1_CLERK, BattleFrontier_ExchangeServiceCorner_EventScript_ChooseDecor1
	goto_if_eq VAR_TEMP_2, EXCHANGE_CORNER_DECOR2_CLERK, BattleFrontier_ExchangeServiceCorner_EventScript_ChooseDecor2
	goto_if_eq VAR_TEMP_2, EXCHANGE_CORNER_VITAMIN_CLERK, BattleFrontier_ExchangeServiceCorner_EventScript_ChooseVitamin
	goto BattleFrontier_ExchangeServiceCorner_EventScript_ChooseHoldItem
	end

BattleFrontier_ExchangeServiceCorner_EventScript_TryGivePrize::
	goto_if_eq VAR_TEMP_2, EXCHANGE_CORNER_DECOR1_CLERK, BattleFrontier_ExchangeServiceCorner_EventScript_TryGiveDecor
	goto_if_eq VAR_TEMP_2, EXCHANGE_CORNER_DECOR2_CLERK, BattleFrontier_ExchangeServiceCorner_EventScript_TryGiveDecor
	goto BattleFrontier_ExchangeServiceCorner_EventScript_TryGiveItem
	end

BattleFrontier_ExchangeServiceCorner_EventScript_TryGiveDecor::
	checkdecorspace VAR_0x8009
	goto_if_eq VAR_RESULT, FALSE, BattleFrontier_ExchangeServiceCorner_EventScript_NoRoomForDecor
	copyvar VAR_0x8004, VAR_0x8008
	special TakeFrontierBattlePoints
	adddecoration VAR_0x8009
	special UpdateBattlePointsWindow
	playse SE_SHOP
	msgbox BattleFrontier_ExchangeServiceCorner_Text_WellSendItToPC, MSGBOX_DEFAULT
	goto_if_eq VAR_TEMP_2, EXCHANGE_CORNER_DECOR1_CLERK, BattleFrontier_ExchangeServiceCorner_EventScript_ChooseDecor1
	goto BattleFrontier_ExchangeServiceCorner_EventScript_ChooseDecor2
	end

BattleFrontier_ExchangeServiceCorner_EventScript_NoRoomForDecor::
	msgbox BattleFrontier_ExchangeServiceCorner_Text_PCIsFull, MSGBOX_DEFAULT
	special CloseBattlePointsWindow
	release
	end

BattleFrontier_ExchangeServiceCorner_EventScript_TryGiveItem::
	checkitemspace VAR_0x8009
	goto_if_eq VAR_RESULT, FALSE, BattleFrontier_ExchangeServiceCorner_EventScript_BagFull
	copyvar VAR_0x8004, VAR_0x8008
	special TakeFrontierBattlePoints
	additem VAR_0x8009
	special UpdateBattlePointsWindow
	playse SE_SHOP
	msgbox BattleFrontier_ExchangeServiceCorner_Text_HereIsYourPrize, MSGBOX_DEFAULT
	goto_if_eq VAR_TEMP_2, EXCHANGE_CORNER_VITAMIN_CLERK, BattleFrontier_ExchangeServiceCorner_EventScript_ChooseVitamin
	goto BattleFrontier_ExchangeServiceCorner_EventScript_ChooseHoldItem
	end

BattleFrontier_ExchangeServiceCorner_EventScript_BagFull::
	msgbox BattleFrontier_ExchangeServiceCorner_Text_DontHaveSpaceToHoldIt, MSGBOX_DEFAULT
	special CloseBattlePointsWindow
	release
	end

BattleFrontier_ExchangeServiceCorner_EventScript_DecorClerk1::
	lock
	faceplayer
	setvar VAR_TEMP_2, EXCHANGE_CORNER_DECOR1_CLERK
	call BattleFrontier_ExchangeServiceCorner_EventScript_ClerkWelcome
	goto BattleFrontier_ExchangeServiceCorner_EventScript_ChooseDecor1
	end

BattleFrontier_ExchangeServiceCorner_EventScript_ChooseDecor1::
	setvar VAR_0x8004, SCROLL_MULTI_BF_EXCHANGE_CORNER_DECOR_VENDOR_1
	special ShowFrontierExchangeCornerItemIconWindow
	special ShowScrollableMultichoice
	special CloseFrontierExchangeCornerItemIconWindow
	switch VAR_RESULT
	case 0, BattleFrontier_ExchangeServiceCorner_EventScript_KissPoster
	case 1, BattleFrontier_ExchangeServiceCorner_EventScript_KissCushion
	case 2, BattleFrontier_ExchangeServiceCorner_EventScript_SmoochumDoll
	case 3, BattleFrontier_ExchangeServiceCorner_EventScript_TogepiDoll
	case 4, BattleFrontier_ExchangeServiceCorner_EventScript_MeowthDoll
	case 5, BattleFrontier_ExchangeServiceCorner_EventScript_ClefairyDoll
	case 6, BattleFrontier_ExchangeServiceCorner_EventScript_DittoDoll
	case 7, BattleFrontier_ExchangeServiceCorner_EventScript_CyndaquilDoll
	case 8, BattleFrontier_ExchangeServiceCorner_EventScript_ChikoritaDoll
	case 9, BattleFrontier_ExchangeServiceCorner_EventScript_TotodileDoll
	case 10, BattleFrontier_ExchangeServiceCorner_EventScript_ClerkGoodbye
	case MULTI_B_PRESSED, BattleFrontier_ExchangeServiceCorner_EventScript_ClerkGoodbye
	end

BattleFrontier_ExchangeServiceCorner_EventScript_KissPoster::
	msgbox BattleFrontier_ExchangeServiceCorner_Text_ConfirmKissPoster, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, BattleFrontier_ExchangeServiceCorner_EventScript_ChooseDecor1
	setvar VAR_0x8008, 16
	setvar VAR_0x8009, DECOR_KISS_POSTER
	goto BattleFrontier_ExchangeServiceCorner_EventScript_TryPurchasePrize
	end

BattleFrontier_ExchangeServiceCorner_EventScript_KissCushion::
	msgbox BattleFrontier_ExchangeServiceCorner_Text_ConfirmKissCushion, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, BattleFrontier_ExchangeServiceCorner_EventScript_ChooseDecor1
	setvar VAR_0x8008, 32
	setvar VAR_0x8009, DECOR_KISS_CUSHION
	goto BattleFrontier_ExchangeServiceCorner_EventScript_TryPurchasePrize
	end

BattleFrontier_ExchangeServiceCorner_EventScript_SmoochumDoll::
	msgbox BattleFrontier_ExchangeServiceCorner_Text_ConfirmSmoochumDoll, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, BattleFrontier_ExchangeServiceCorner_EventScript_ChooseDecor1
	setvar VAR_0x8008, 32
	setvar VAR_0x8009, DECOR_SMOOCHUM_DOLL
	goto BattleFrontier_ExchangeServiceCorner_EventScript_TryPurchasePrize
	end

BattleFrontier_ExchangeServiceCorner_EventScript_TogepiDoll::
	msgbox BattleFrontier_ExchangeServiceCorner_Text_ConfirmTogepiDoll, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, BattleFrontier_ExchangeServiceCorner_EventScript_ChooseDecor1
	setvar VAR_0x8008, 48
	setvar VAR_0x8009, DECOR_TOGEPI_DOLL
	goto BattleFrontier_ExchangeServiceCorner_EventScript_TryPurchasePrize
	end

BattleFrontier_ExchangeServiceCorner_EventScript_MeowthDoll::
	msgbox BattleFrontier_ExchangeServiceCorner_Text_ConfirmMeowthDoll, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, BattleFrontier_ExchangeServiceCorner_EventScript_ChooseDecor1
	setvar VAR_0x8008, 48
	setvar VAR_0x8009, DECOR_MEOWTH_DOLL
	goto BattleFrontier_ExchangeServiceCorner_EventScript_TryPurchasePrize
	end

BattleFrontier_ExchangeServiceCorner_EventScript_ClefairyDoll::
	msgbox BattleFrontier_ExchangeServiceCorner_Text_ConfirmClefairyDoll, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, BattleFrontier_ExchangeServiceCorner_EventScript_ChooseDecor1
	setvar VAR_0x8008, 48
	setvar VAR_0x8009, DECOR_CLEFAIRY_DOLL
	goto BattleFrontier_ExchangeServiceCorner_EventScript_TryPurchasePrize
	end

BattleFrontier_ExchangeServiceCorner_EventScript_DittoDoll::
	msgbox BattleFrontier_ExchangeServiceCorner_Text_ConfirmDittoDoll, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, BattleFrontier_ExchangeServiceCorner_EventScript_ChooseDecor1
	setvar VAR_0x8008, 48
	setvar VAR_0x8009, DECOR_DITTO_DOLL
	goto BattleFrontier_ExchangeServiceCorner_EventScript_TryPurchasePrize
	end

BattleFrontier_ExchangeServiceCorner_EventScript_CyndaquilDoll::
	msgbox BattleFrontier_ExchangeServiceCorner_Text_ConfirmCyndaquilDoll, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, BattleFrontier_ExchangeServiceCorner_EventScript_ChooseDecor1
	setvar VAR_0x8008, 80
	setvar VAR_0x8009, DECOR_CYNDAQUIL_DOLL
	goto BattleFrontier_ExchangeServiceCorner_EventScript_TryPurchasePrize
	end

BattleFrontier_ExchangeServiceCorner_EventScript_ChikoritaDoll::
	msgbox BattleFrontier_ExchangeServiceCorner_Text_ConfirmChikoritaDoll, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, BattleFrontier_ExchangeServiceCorner_EventScript_ChooseDecor1
	setvar VAR_0x8008, 80
	setvar VAR_0x8009, DECOR_CHIKORITA_DOLL
	goto BattleFrontier_ExchangeServiceCorner_EventScript_TryPurchasePrize
	end

BattleFrontier_ExchangeServiceCorner_EventScript_TotodileDoll::
	msgbox BattleFrontier_ExchangeServiceCorner_Text_ConfirmTotodileDoll, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, BattleFrontier_ExchangeServiceCorner_EventScript_ChooseDecor1
	setvar VAR_0x8008, 80
	setvar VAR_0x8009, DECOR_TOTODILE_DOLL
	goto BattleFrontier_ExchangeServiceCorner_EventScript_TryPurchasePrize
	end

BattleFrontier_ExchangeServiceCorner_EventScript_DecorClerk2::
	lock
	faceplayer
	setvar VAR_TEMP_2, EXCHANGE_CORNER_DECOR2_CLERK
	call BattleFrontier_ExchangeServiceCorner_EventScript_ClerkWelcome
	goto BattleFrontier_ExchangeServiceCorner_EventScript_ChooseDecor2
	end

BattleFrontier_ExchangeServiceCorner_EventScript_ChooseDecor2::
	setvar VAR_0x8004, SCROLL_MULTI_BF_EXCHANGE_CORNER_DECOR_VENDOR_2
	special ShowFrontierExchangeCornerItemIconWindow
	special ShowScrollableMultichoice
	special CloseFrontierExchangeCornerItemIconWindow
	switch VAR_RESULT
	case 0, BattleFrontier_ExchangeServiceCorner_EventScript_LaprasDoll
	case 1, BattleFrontier_ExchangeServiceCorner_EventScript_SnorlaxDoll
	case 2, BattleFrontier_ExchangeServiceCorner_EventScript_VenusaurDoll
	case 3, BattleFrontier_ExchangeServiceCorner_EventScript_CharizardDoll
	case 4, BattleFrontier_ExchangeServiceCorner_EventScript_BlastoiseDoll
	case 5, BattleFrontier_ExchangeServiceCorner_EventScript_ClerkGoodbye
	case MULTI_B_PRESSED, BattleFrontier_ExchangeServiceCorner_EventScript_ClerkGoodbye
	end

BattleFrontier_ExchangeServiceCorner_EventScript_LaprasDoll::
	msgbox BattleFrontier_ExchangeServiceCorner_Text_ConfirmLaprasDoll, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, BattleFrontier_ExchangeServiceCorner_EventScript_ChooseDecor2
	setvar VAR_0x8008, 128
	setvar VAR_0x8009, DECOR_LAPRAS_DOLL
	goto BattleFrontier_ExchangeServiceCorner_EventScript_TryPurchasePrize
	end

BattleFrontier_ExchangeServiceCorner_EventScript_SnorlaxDoll::
	msgbox BattleFrontier_ExchangeServiceCorner_Text_ConfirmSnorlaxDoll, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, BattleFrontier_ExchangeServiceCorner_EventScript_ChooseDecor2
	setvar VAR_0x8008, 128
	setvar VAR_0x8009, DECOR_SNORLAX_DOLL
	goto BattleFrontier_ExchangeServiceCorner_EventScript_TryPurchasePrize
	end

BattleFrontier_ExchangeServiceCorner_EventScript_VenusaurDoll::
	msgbox BattleFrontier_ExchangeServiceCorner_Text_ConfirmVenusaurDoll, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, BattleFrontier_ExchangeServiceCorner_EventScript_ChooseDecor2
	setvar VAR_0x8008, 256
	setvar VAR_0x8009, DECOR_VENUSAUR_DOLL
	goto BattleFrontier_ExchangeServiceCorner_EventScript_TryPurchasePrize
	end

BattleFrontier_ExchangeServiceCorner_EventScript_CharizardDoll::
	msgbox BattleFrontier_ExchangeServiceCorner_Text_ConfirmCharizardDoll, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, BattleFrontier_ExchangeServiceCorner_EventScript_ChooseDecor2
	setvar VAR_0x8008, 256
	setvar VAR_0x8009, DECOR_CHARIZARD_DOLL
	goto BattleFrontier_ExchangeServiceCorner_EventScript_TryPurchasePrize
	end

BattleFrontier_ExchangeServiceCorner_EventScript_BlastoiseDoll::
	msgbox BattleFrontier_ExchangeServiceCorner_Text_ConfirmBlastoiseDoll, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, BattleFrontier_ExchangeServiceCorner_EventScript_ChooseDecor2
	setvar VAR_0x8008, 256
	setvar VAR_0x8009, DECOR_BLASTOISE_DOLL
	goto BattleFrontier_ExchangeServiceCorner_EventScript_TryPurchasePrize
	end

BattleFrontier_ExchangeServiceCorner_EventScript_VitaminClerk::
	lock
	faceplayer
	setvar VAR_TEMP_2, EXCHANGE_CORNER_VITAMIN_CLERK
	call BattleFrontier_ExchangeServiceCorner_EventScript_ClerkWelcome
	goto BattleFrontier_ExchangeServiceCorner_EventScript_ChooseVitamin
	end

BattleFrontier_ExchangeServiceCorner_EventScript_ChooseVitamin::
	setvar VAR_0x8004, SCROLL_MULTI_BF_EXCHANGE_CORNER_VITAMIN_VENDOR
	special ShowFrontierExchangeCornerItemIconWindow
	special ShowScrollableMultichoice
	special CloseFrontierExchangeCornerItemIconWindow
	switch VAR_RESULT
	case 0, BattleFrontier_ExchangeServiceCorner_EventScript_Protein
	case 1, BattleFrontier_ExchangeServiceCorner_EventScript_Calcium
	case 2, BattleFrontier_ExchangeServiceCorner_EventScript_Iron
	case 3, BattleFrontier_ExchangeServiceCorner_EventScript_Zinc
	case 4, BattleFrontier_ExchangeServiceCorner_EventScript_Carbos
	case 5, BattleFrontier_ExchangeServiceCorner_EventScript_HPUp
	case 6, BattleFrontier_ExchangeServiceCorner_EventScript_ClerkGoodbye
	case MULTI_B_PRESSED, BattleFrontier_ExchangeServiceCorner_EventScript_ClerkGoodbye
	end

BattleFrontier_ExchangeServiceCorner_EventScript_Protein::
	msgbox BattleFrontier_ExchangeServiceCorner_Text_ConfirmProtein, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, BattleFrontier_ExchangeServiceCorner_EventScript_ChooseVitamin
	setvar VAR_0x8008, 1
	setvar VAR_0x8009, ITEM_PROTEIN
	goto BattleFrontier_ExchangeServiceCorner_EventScript_TryPurchasePrize
	end

BattleFrontier_ExchangeServiceCorner_EventScript_Calcium::
	msgbox BattleFrontier_ExchangeServiceCorner_Text_ConfirmCalcium, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, BattleFrontier_ExchangeServiceCorner_EventScript_ChooseVitamin
	setvar VAR_0x8008, 1
	setvar VAR_0x8009, ITEM_CALCIUM
	goto BattleFrontier_ExchangeServiceCorner_EventScript_TryPurchasePrize
	end

BattleFrontier_ExchangeServiceCorner_EventScript_Iron::
	msgbox BattleFrontier_ExchangeServiceCorner_Text_ConfirmIron, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, BattleFrontier_ExchangeServiceCorner_EventScript_ChooseVitamin
	setvar VAR_0x8008, 1
	setvar VAR_0x8009, ITEM_IRON
	goto BattleFrontier_ExchangeServiceCorner_EventScript_TryPurchasePrize
	end

BattleFrontier_ExchangeServiceCorner_EventScript_Zinc::
	msgbox BattleFrontier_ExchangeServiceCorner_Text_ConfirmZinc, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, BattleFrontier_ExchangeServiceCorner_EventScript_ChooseVitamin
	setvar VAR_0x8008, 1
	setvar VAR_0x8009, ITEM_ZINC
	goto BattleFrontier_ExchangeServiceCorner_EventScript_TryPurchasePrize
	end

BattleFrontier_ExchangeServiceCorner_EventScript_Carbos::
	msgbox BattleFrontier_ExchangeServiceCorner_Text_ConfirmCarbos, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, BattleFrontier_ExchangeServiceCorner_EventScript_ChooseVitamin
	setvar VAR_0x8008, 1
	setvar VAR_0x8009, ITEM_CARBOS
	goto BattleFrontier_ExchangeServiceCorner_EventScript_TryPurchasePrize
	end

BattleFrontier_ExchangeServiceCorner_EventScript_HPUp::
	msgbox BattleFrontier_ExchangeServiceCorner_Text_ConfirmHPUp, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, BattleFrontier_ExchangeServiceCorner_EventScript_ChooseVitamin
	setvar VAR_0x8008, 1
	setvar VAR_0x8009, ITEM_HP_UP
	goto BattleFrontier_ExchangeServiceCorner_EventScript_TryPurchasePrize
	end

BattleFrontier_ExchangeServiceCorner_EventScript_HoldItemClerk::
	lock
	faceplayer
	setvar VAR_TEMP_2, EXCHANGE_CORNER_HOLD_ITEM_CLERK
	call BattleFrontier_ExchangeServiceCorner_EventScript_ClerkWelcome
	goto BattleFrontier_ExchangeServiceCorner_EventScript_ChooseHoldItem
	end

BattleFrontier_ExchangeServiceCorner_EventScript_ChooseHoldItem::
	setvar VAR_0x8004, SCROLL_MULTI_BF_EXCHANGE_CORNER_HOLD_ITEM_VENDOR
	special ShowFrontierExchangeCornerItemIconWindow
	special ShowScrollableMultichoice
	special CloseFrontierExchangeCornerItemIconWindow
	switch VAR_RESULT
	case 0, BattleFrontier_ExchangeServiceCorner_EventScript_Leftovers
	case 1, BattleFrontier_ExchangeServiceCorner_EventScript_WhiteHerb
	case 2, BattleFrontier_ExchangeServiceCorner_EventScript_QuickClaw
	case 3, BattleFrontier_ExchangeServiceCorner_EventScript_MentalHerb
	case 4, BattleFrontier_ExchangeServiceCorner_EventScript_Brightpowder
	case 5, BattleFrontier_ExchangeServiceCorner_EventScript_ChoiceBand
	case 6, BattleFrontier_ExchangeServiceCorner_EventScript_KingsRock
	case 7, BattleFrontier_ExchangeServiceCorner_EventScript_FocusBand
	case 8, BattleFrontier_ExchangeServiceCorner_EventScript_ScopeLens
	case 9, BattleFrontier_ExchangeServiceCorner_EventScript_ClerkGoodbye
	case MULTI_B_PRESSED, BattleFrontier_ExchangeServiceCorner_EventScript_ClerkGoodbye
	end

BattleFrontier_ExchangeServiceCorner_EventScript_Leftovers::
	msgbox BattleFrontier_ExchangeServiceCorner_Text_ConfirmLeftovers, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, BattleFrontier_ExchangeServiceCorner_EventScript_ChooseHoldItem
	setvar VAR_0x8008, 48
	setvar VAR_0x8009, ITEM_LEFTOVERS
	goto BattleFrontier_ExchangeServiceCorner_EventScript_TryPurchasePrize
	end

BattleFrontier_ExchangeServiceCorner_EventScript_WhiteHerb::
	msgbox BattleFrontier_ExchangeServiceCorner_Text_ConfirmWhiteHerb, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, BattleFrontier_ExchangeServiceCorner_EventScript_ChooseHoldItem
	setvar VAR_0x8008, 48
	setvar VAR_0x8009, ITEM_WHITE_HERB
	goto BattleFrontier_ExchangeServiceCorner_EventScript_TryPurchasePrize
	end

BattleFrontier_ExchangeServiceCorner_EventScript_QuickClaw::
	msgbox BattleFrontier_ExchangeServiceCorner_Text_ConfirmQuickClaw, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, BattleFrontier_ExchangeServiceCorner_EventScript_ChooseHoldItem
	setvar VAR_0x8008, 48
	setvar VAR_0x8009, ITEM_QUICK_CLAW
	goto BattleFrontier_ExchangeServiceCorner_EventScript_TryPurchasePrize
	end

BattleFrontier_ExchangeServiceCorner_EventScript_MentalHerb::
	msgbox BattleFrontier_ExchangeServiceCorner_Text_ConfirmMentalHerb, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, BattleFrontier_ExchangeServiceCorner_EventScript_ChooseHoldItem
	setvar VAR_0x8008, 48
	setvar VAR_0x8009, ITEM_MENTAL_HERB
	goto BattleFrontier_ExchangeServiceCorner_EventScript_TryPurchasePrize
	end

BattleFrontier_ExchangeServiceCorner_EventScript_Brightpowder::
	msgbox BattleFrontier_ExchangeServiceCorner_Text_ConfirmBrightpowder, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, BattleFrontier_ExchangeServiceCorner_EventScript_ChooseHoldItem
	setvar VAR_0x8008, 64
	setvar VAR_0x8009, ITEM_BRIGHT_POWDER
	goto BattleFrontier_ExchangeServiceCorner_EventScript_TryPurchasePrize
	end

BattleFrontier_ExchangeServiceCorner_EventScript_ChoiceBand::
	msgbox BattleFrontier_ExchangeServiceCorner_Text_ConfirmChoiceBand, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, BattleFrontier_ExchangeServiceCorner_EventScript_ChooseHoldItem
	setvar VAR_0x8008, 64
	setvar VAR_0x8009, ITEM_CHOICE_BAND
	goto BattleFrontier_ExchangeServiceCorner_EventScript_TryPurchasePrize
	end

BattleFrontier_ExchangeServiceCorner_EventScript_KingsRock::
	msgbox BattleFrontier_ExchangeServiceCorner_Text_ConfirmKingsRock, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, BattleFrontier_ExchangeServiceCorner_EventScript_ChooseHoldItem
	setvar VAR_0x8008, 64
	setvar VAR_0x8009, ITEM_KINGS_ROCK
	goto BattleFrontier_ExchangeServiceCorner_EventScript_TryPurchasePrize
	end

BattleFrontier_ExchangeServiceCorner_EventScript_FocusBand::
	msgbox BattleFrontier_ExchangeServiceCorner_Text_ConfirmFocusBand, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, BattleFrontier_ExchangeServiceCorner_EventScript_ChooseHoldItem
	setvar VAR_0x8008, 64
	setvar VAR_0x8009, ITEM_FOCUS_BAND
	goto BattleFrontier_ExchangeServiceCorner_EventScript_TryPurchasePrize
	end

BattleFrontier_ExchangeServiceCorner_EventScript_ScopeLens::
	msgbox BattleFrontier_ExchangeServiceCorner_Text_ConfirmScopeLens, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, BattleFrontier_ExchangeServiceCorner_EventScript_ChooseHoldItem
	setvar VAR_0x8008, 64
	setvar VAR_0x8009, ITEM_SCOPE_LENS
	goto BattleFrontier_ExchangeServiceCorner_EventScript_TryPurchasePrize
	end

BattleFrontier_ExchangeServiceCorner_EventScript_Man::
	msgbox BattleFrontier_ExchangeServiceCorner_Text_GoGetYourOwnDoll, MSGBOX_NPC
	end

BattleFrontier_ExchangeServiceCorner_EventScript_Sailor::
	msgbox BattleFrontier_ExchangeServiceCorner_Text_ItemsWillGetMonTougher, MSGBOX_NPC
	end

BattleFrontier_ExchangeServiceCorner_EventScript_PokefanF::
	lock
	msgbox BattleFrontier_ExchangeServiceCorner_Text_GetYouAnythingYouWant, MSGBOX_DEFAULT
	release
	end

BattleFrontier_ExchangeServiceCorner_EventScript_RichBoy::
	msgbox BattleFrontier_ExchangeServiceCorner_Text_WishIHadAllDolls, MSGBOX_NPC
	end

BattleFrontier_ExchangeServiceCorner_EventScript_Girl::
	msgbox BattleFrontier_ExchangeServiceCorner_Text_MoreBattlePointsForRecord, MSGBOX_NPC
	end

BattleFrontier_ExchangeServiceCorner_Text_WelcomePleaseChoosePrize:
.string "สวัสดี ที่นี่คือจุดแลก\nแบทเทิลพอยต์.\pเราจะนำแบทเทิลพอยต์ที่คุณสะสม\nมาแลกเป็นของรางวัลดี ๆ.\pโปรดเลือกของรางวัลจากรายการนี้.$"

@ Unused
BattleFrontier_ExchangeServiceCorner_Text_PleaseChoosePrize:
.string "โปรดเลือกของรางวัลจากรายการนี้.$"

BattleFrontier_ExchangeServiceCorner_Text_ConfirmKissPoster:
.string "คุณเลือก KISS POSTER แล้ว.\nถูกต้องไหม?$"

BattleFrontier_ExchangeServiceCorner_Text_ConfirmKissCushion:
.string "คุณเลือก KISS CUSHION แล้ว.\nถูกต้องไหม?$"

BattleFrontier_ExchangeServiceCorner_Text_ConfirmSmoochumDoll:
.string "คุณเลือก SMOOCHUM DOLL แล้ว.\nถูกต้องไหม?$"

BattleFrontier_ExchangeServiceCorner_Text_ConfirmTogepiDoll:
.string "คุณเลือก TOGEPI DOLL แล้ว.\nถูกต้องไหม?$"

BattleFrontier_ExchangeServiceCorner_Text_ConfirmMeowthDoll:
.string "คุณเลือก MEOWTH DOLL แล้ว.\nถูกต้องไหม?$"

BattleFrontier_ExchangeServiceCorner_Text_ConfirmClefairyDoll:
.string "คุณเลือก CLEFAIRY DOLL แล้ว.\nถูกต้องไหม?$"

BattleFrontier_ExchangeServiceCorner_Text_ConfirmDittoDoll:
.string "คุณเลือก DITTO DOLL แล้ว.\nถูกต้องไหม?$"

BattleFrontier_ExchangeServiceCorner_Text_ConfirmCyndaquilDoll:
.string "คุณเลือก CYNDAQUIL DOLL แล้ว.\nถูกต้องไหม?$"

BattleFrontier_ExchangeServiceCorner_Text_ConfirmChikoritaDoll:
.string "คุณเลือก CHIKORITA DOLL แล้ว.\nถูกต้องไหม?$"

BattleFrontier_ExchangeServiceCorner_Text_ConfirmTotodileDoll:
.string "คุณเลือก TOTODILE DOLL แล้ว.\nถูกต้องไหม?$"

BattleFrontier_ExchangeServiceCorner_Text_ConfirmLaprasDoll:
.string "คุณเลือก LAPRAS DOLL แล้ว.\nถูกต้องไหม?$"

BattleFrontier_ExchangeServiceCorner_Text_ConfirmSnorlaxDoll:
.string "คุณเลือก SNORLAX DOLL แล้ว.\nถูกต้องไหม?$"

BattleFrontier_ExchangeServiceCorner_Text_ConfirmVenusaurDoll:
.string "คุณเลือก VENUSAUR DOLL แล้ว.\nถูกต้องไหม?$"

BattleFrontier_ExchangeServiceCorner_Text_ConfirmCharizardDoll:
.string "คุณเลือก CHARIZARD DOLL แล้ว.\nถูกต้องไหม?$"

BattleFrontier_ExchangeServiceCorner_Text_ConfirmBlastoiseDoll:
.string "คุณเลือก BLASTOISE DOLL แล้ว.\nถูกต้องไหม?$"

BattleFrontier_ExchangeServiceCorner_Text_ConfirmProtein:
.string "คุณเลือก PROTEIN แล้ว.\nถูกต้องไหม?$"

BattleFrontier_ExchangeServiceCorner_Text_ConfirmCalcium:
.string "คุณเลือก CALCIUM แล้ว.\nถูกต้องไหม?$"

BattleFrontier_ExchangeServiceCorner_Text_ConfirmIron:
.string "คุณเลือก IRON แล้ว.\nถูกต้องไหม?$"

BattleFrontier_ExchangeServiceCorner_Text_ConfirmZinc:
.string "คุณเลือก ZINC แล้ว.\nถูกต้องไหม?$"

BattleFrontier_ExchangeServiceCorner_Text_ConfirmCarbos:
.string "คุณเลือก CARBOS แล้ว.\nถูกต้องไหม?$"

BattleFrontier_ExchangeServiceCorner_Text_ConfirmHPUp:
.string "คุณเลือก HP UP แล้ว.\nถูกต้องไหม?$"

BattleFrontier_ExchangeServiceCorner_Text_ConfirmBrightpowder:
.string "คุณเลือก BRIGHTPOWDER แล้ว.\nถูกต้องไหม?$"

BattleFrontier_ExchangeServiceCorner_Text_ConfirmWhiteHerb:
.string "คุณเลือก WHITE HERB แล้ว.\nถูกต้องไหม?$"

BattleFrontier_ExchangeServiceCorner_Text_ConfirmQuickClaw:
.string "คุณเลือก QUICK CLAW แล้ว.\nถูกต้องไหม?$"

BattleFrontier_ExchangeServiceCorner_Text_ConfirmMentalHerb:
.string "คุณเลือก MENTAL HERB แล้ว.\nถูกต้องไหม?$"

BattleFrontier_ExchangeServiceCorner_Text_ConfirmChoiceBand:
.string "คุณเลือก CHOICE BAND แล้ว.\nถูกต้องไหม?$"

BattleFrontier_ExchangeServiceCorner_Text_ConfirmKingsRock:
.string "คุณเลือก KING'S ROCK แล้ว.\nถูกต้องไหม?$"

BattleFrontier_ExchangeServiceCorner_Text_ConfirmFocusBand:
.string "คุณเลือก FOCUS BAND แล้ว.\nถูกต้องไหม?$"

BattleFrontier_ExchangeServiceCorner_Text_ConfirmScopeLens:
.string "คุณเลือก SCOPE LENS แล้ว.\nถูกต้องไหม?$"

BattleFrontier_ExchangeServiceCorner_Text_ConfirmLeftovers:
.string "คุณเลือก LEFTOVERS แล้ว.\nถูกต้องไหม?$"

BattleFrontier_ExchangeServiceCorner_Text_WellSendItToPC:
.string "ขอบคุณ!\nเราจะส่งไปยัง PC ที่บ้านของคุณ.$"

BattleFrontier_ExchangeServiceCorner_Text_HereIsYourPrize:
.string "นี่คือของรางวัลของคุณ!$"

BattleFrontier_ExchangeServiceCorner_Text_DontHaveEnoughPoints:
.string "ขออภัยจริง ๆ…\nแบทเทิลพอยต์ของคุณไม่พอ…$"

BattleFrontier_ExchangeServiceCorner_Text_PCIsFull:
.string "ขออภัยจริง ๆ…\nดูเหมือน PC ของคุณจะเต็มแล้ว…$"

BattleFrontier_ExchangeServiceCorner_Text_DontHaveSpaceToHoldIt:
.string "ขออภัยจริง ๆ…\nคุณไม่มีที่ว่างสำหรับถือมัน…$"

BattleFrontier_ExchangeServiceCorner_Text_ThankYouVisitWithPoints:
.string "ขอบคุณมาก.\pเชิญมาอีกเมื่อคุณสะสม\nแบทเทิลพอยต์ได้มากพอแล้ว.$"

BattleFrontier_ExchangeServiceCorner_Text_WishIHadAllDolls:
.string "โอ้ น่ารักจัง!\nฉันอยากได้พวกนั้น!\lเบาะก็น่ารัก!\lตุ๊กตาผ้าตัวใหญ่!\lตุ๊กตาผ้าตัวเล็ก!\lฉันอยากได้ทั้งหมดเลย!$"

BattleFrontier_ExchangeServiceCorner_Text_GetYouAnythingYouWant:
.string "ปล่อยให้แม่จัดการเอง!\pถ้าเป็นของที่ลูกอยากได้ แม่จะ\nทำทุกอย่างเพื่อหามาให้เลยจ้ะ!$"

BattleFrontier_ExchangeServiceCorner_Text_ItemsWillGetMonTougher:
.string "ถ้าได้ไอเทมจากที่นี่มา\nโปเกมอนของฉันจะแกร่งขึ้น.\pต้องแกร่งขึ้นแน่!\nไม่มีข้อสงสัยเลย!$"

BattleFrontier_ExchangeServiceCorner_Text_GoGetYourOwnDoll:
.string "หา?\nจ้องอะไรอยู่?\pฉันไม่ชอบให้ใครมาจ้อง\nตุ๊กตาผ้าของฉันแบบนั้น.\pถ้าอยากได้ก็ไปหามาเองสิ!\nจริงไหม มูจูรู?$"

BattleFrontier_ExchangeServiceCorner_Text_MoreBattlePointsForRecord:
.string "รู้ไหม?\pถ้าทำสถิติได้ยาวขึ้นที่\nสถานที่แบทเทิลต่าง ๆ ก็จะ\lได้รับแบทเทิลพอยต์มากขึ้นเรื่อย ๆ.$"

BattleFrontier_ExchangeServiceCorner_Text_KissPosterDesc::
.string "โปสเตอร์ขนาดใหญ่ลายมูจูรู.$"

BattleFrontier_ExchangeServiceCorner_Text_KissCushionDesc::
.string "เบาะรองนั่งลายมูจูรู.\nวางบนเสื่อหรือโต๊ะได้.$"

BattleFrontier_ExchangeServiceCorner_Text_SmoochumDollDesc::
.string "SMOOCHUM DOLL.\nวางบนเสื่อหรือโต๊ะได้.$"

BattleFrontier_ExchangeServiceCorner_Text_TogepiDollDesc::
.string "TOGEPI DOLL.\nวางบนเสื่อหรือโต๊ะได้.$"

BattleFrontier_ExchangeServiceCorner_Text_MeowthDollDesc::
.string "MEOWTH DOLL.\nวางบนเสื่อหรือโต๊ะได้.$"

BattleFrontier_ExchangeServiceCorner_Text_ClefairyDollDesc::
.string "CLEFAIRY DOLL.\nวางบนเสื่อหรือโต๊ะได้.$"

BattleFrontier_ExchangeServiceCorner_Text_DittoDollDesc::
.string "DITTO DOLL.\nวางบนเสื่อหรือโต๊ะได้.$"

BattleFrontier_ExchangeServiceCorner_Text_CyndaquilDollDesc::
.string "CYNDAQUIL DOLL.\nวางบนเสื่อหรือโต๊ะได้.$"

BattleFrontier_ExchangeServiceCorner_Text_ChikoritaDollDesc::
.string "CHIKORITA DOLL.\nวางบนเสื่อหรือโต๊ะได้.$"

BattleFrontier_ExchangeServiceCorner_Text_TotodileDollDesc::
.string "TOTODILE DOLL.\nวางบนเสื่อหรือโต๊ะได้.$"

BattleFrontier_ExchangeServiceCorner_Text_LargeDollDesc::
.string "ตุ๊กตาขนาดใหญ่.\nวางบนเสื่อหรือโต๊ะได้.$"

BattleFrontier_ExchangeServiceCorner_Text_ProteinDesc::
.string "เพิ่มพลังโจมตีของโปเกมอน\nหนึ่งตัว.$"

BattleFrontier_ExchangeServiceCorner_Text_CalciumDesc::
.string "เพิ่มพลังโจมตีพิเศษของโปเกมอน\nหนึ่งตัว.$"

BattleFrontier_ExchangeServiceCorner_Text_IronDesc::
.string "เพิ่มพลังป้องกันของโปเกมอน\nหนึ่งตัว.$"

BattleFrontier_ExchangeServiceCorner_Text_ZincDesc::
.string "เพิ่มพลังป้องกันพิเศษของโปเกมอน\nหนึ่งตัว.$"

BattleFrontier_ExchangeServiceCorner_Text_CarbosDesc::
.string "เพิ่มความเร็วของโปเกมอน\nหนึ่งตัว.$"

BattleFrontier_ExchangeServiceCorner_Text_HPUpDesc::
.string "เพิ่ม HP ของโปเกมอนหนึ่งตัว.$"

BattleFrontier_ExchangeServiceCorner_Text_LeftoversDesc::
.string "ไอเทมถือที่ค่อย ๆ ฟื้นฟู HP\nระหว่างการต่อสู้.$"

BattleFrontier_ExchangeServiceCorner_Text_WhiteHerbDesc::
.string "ไอเทมถือที่ฟื้นคืน\nค่าสถานะที่ถูกลด.$"

BattleFrontier_ExchangeServiceCorner_Text_QuickClawDesc::
.string "ไอเทมถือที่บางครั้งทำให้\nได้โจมตีก่อน.$"

BattleFrontier_ExchangeServiceCorner_Text_MentalHerbDesc::
.string "ไอเทมถือที่แก้อาการหลงเสน่ห์\nของโปเกมอน.$"

BattleFrontier_ExchangeServiceCorner_Text_BrightpowderDesc::
.string "ไอเทมถือที่ส่องแสง\nลดความแม่นยำของคู่ต่อสู้.$"

BattleFrontier_ExchangeServiceCorner_Text_ChoiceBandDesc::
.string "เพิ่มพลังของท่า แต่จะใช้ได้\nเพียงท่านั้น.$"

BattleFrontier_ExchangeServiceCorner_Text_KingsRockDesc::
.string "ไอเทมถือที่อาจทำให้คู่ต่อสู้ชะงัก\nเมื่อถูกโจมตี.$"

BattleFrontier_ExchangeServiceCorner_Text_FocusBandDesc::
.string "ไอเทมถือที่บางครั้ง\nป้องกันการหมดสภาพ.$"

BattleFrontier_ExchangeServiceCorner_Text_ScopeLensDesc::
.string "ไอเทมถือที่เพิ่ม\nโอกาสโจมตีคริติคอล.$"
