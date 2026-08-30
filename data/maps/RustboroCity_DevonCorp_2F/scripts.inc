RustboroCity_DevonCorp_2F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, RustboroCity_DevonCorp_2F_OnTransition
	.byte 0

RustboroCity_DevonCorp_2F_OnTransition:
	call_if_eq VAR_FOSSIL_RESURRECTION_STATE, 1, RustboroCity_DevonCorp_2F_EventScript_SetFossilReady
	end

RustboroCity_DevonCorp_2F_EventScript_SetFossilReady::
	setvar VAR_FOSSIL_RESURRECTION_STATE, 2
	return

RustboroCity_DevonCorp_2F_EventScript_TalkToPokemonScientist::
	lock
	faceplayer
	call_if_eq VAR_FOSSIL_RESURRECTION_STATE, 1, RustboroCity_DevonCorp_2F_EventScript_SetFossilReady
	msgbox RustboroCity_DevonCorp_2F_Text_DeviceForTalkingToPokemon, MSGBOX_DEFAULT
	release
	end

RustboroCity_DevonCorp_2F_EventScript_BallScientist::
	lock
	faceplayer
	call_if_eq VAR_FOSSIL_RESURRECTION_STATE, 1, RustboroCity_DevonCorp_2F_EventScript_SetFossilReady
	goto_if_set FLAG_MET_DEVON_EMPLOYEE, RustboroCity_DevonCorp_2F_EventScript_DevelopedBalls
	msgbox RustboroCity_DevonCorp_2F_Text_DevelopingNewBalls, MSGBOX_DEFAULT
	release
	end

RustboroCity_DevonCorp_2F_EventScript_DevelopedBalls::
	msgbox RustboroCity_DevonCorp_2F_Text_WeFinallyMadeNewBalls, MSGBOX_DEFAULT
	release
	end

RustboroCity_DevonCorp_2F_EventScript_PokenavScientist::
	lock
	faceplayer
	call_if_eq VAR_FOSSIL_RESURRECTION_STATE, 1, RustboroCity_DevonCorp_2F_EventScript_SetFossilReady
	goto_if_set FLAG_RECEIVED_POKENAV, RustboroCity_DevonCorp_2F_EventScript_HasPokenav
	msgbox RustboroCity_DevonCorp_2F_Text_IMadePokenav, MSGBOX_DEFAULT
	release
	end

RustboroCity_DevonCorp_2F_EventScript_HasPokenav::
	msgbox RustboroCity_DevonCorp_2F_Text_WowThatsAPokenav, MSGBOX_DEFAULT
	release
	end

RustboroCity_DevonCorp_2F_EventScript_PokemonDreamsScientist::
	lock
	faceplayer
	call_if_eq VAR_FOSSIL_RESURRECTION_STATE, 1, RustboroCity_DevonCorp_2F_EventScript_SetFossilReady
	msgbox RustboroCity_DevonCorp_2F_Text_DeviceToVisualizePokemonDreams, MSGBOX_DEFAULT
	release
	end

RustboroCity_DevonCorp_2F_EventScript_FossilScientist::
	lock
	faceplayer
	goto_if_eq VAR_FOSSIL_RESURRECTION_STATE, 2, RustboroCity_DevonCorp_2F_EventScript_FossilMonReady
	goto_if_eq VAR_FOSSIL_RESURRECTION_STATE, 1, RustboroCity_DevonCorp_2F_EventScript_StillRegenerating
	msgbox RustboroCity_DevonCorp_2F_Text_DevelopDeviceToResurrectFossils, MSGBOX_DEFAULT
	checkitem ITEM_ROOT_FOSSIL
	goto_if_eq VAR_RESULT, TRUE, RustboroCity_DevonCorp_2F_EventScript_NoticeRootFossil
	checkitem ITEM_CLAW_FOSSIL
	goto_if_eq VAR_RESULT, TRUE, RustboroCity_DevonCorp_2F_EventScript_NoticeClawFossil
	release
	end

@ This whole section has needless duplication and could be condensed considerably
RustboroCity_DevonCorp_2F_EventScript_NoticeRootFossil::
	closemessage
	playse SE_PIN
	applymovement LOCALID_FOSSIL_SCIENTIST, Common_Movement_ExclamationMark
	waitmovement 0
	applymovement LOCALID_FOSSIL_SCIENTIST, Common_Movement_Delay48
	waitmovement 0
	msgbox RustboroCity_DevonCorp_2F_Text_WantToBringFossilBackToLife, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, RustboroCity_DevonCorp_2F_EventScript_DeclineGiveFossil
	checkitem ITEM_CLAW_FOSSIL
	goto_if_eq VAR_RESULT, TRUE, RustboroCity_DevonCorp_2F_EventScript_ChooseFossil
	goto RustboroCity_DevonCorp_2F_EventScript_GiveRootFossil
	end

RustboroCity_DevonCorp_2F_EventScript_GiveRootFossil::
	bufferitemname STR_VAR_1, ITEM_ROOT_FOSSIL
	msgbox RustboroCity_DevonCorp_2F_Text_HandedFossilToResearcher, MSGBOX_DEFAULT
	removeitem ITEM_ROOT_FOSSIL
	setvar VAR_FOSSIL_RESURRECTION_STATE, 1
	setvar VAR_WHICH_FOSSIL_REVIVED, 1
	release
	end

RustboroCity_DevonCorp_2F_EventScript_NoticeClawFossil::
	closemessage
	playse SE_PIN
	applymovement LOCALID_FOSSIL_SCIENTIST, Common_Movement_ExclamationMark
	waitmovement 0
	applymovement LOCALID_FOSSIL_SCIENTIST, Common_Movement_Delay48
	waitmovement 0
	msgbox RustboroCity_DevonCorp_2F_Text_WantToBringFossilBackToLife, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, RustboroCity_DevonCorp_2F_EventScript_DeclineGiveFossil
	checkitem ITEM_ROOT_FOSSIL
	goto_if_eq VAR_RESULT, TRUE, RustboroCity_DevonCorp_2F_EventScript_ChooseFossil
	goto RustboroCity_DevonCorp_2F_EventScript_GiveClawFossil
	end

RustboroCity_DevonCorp_2F_EventScript_GiveClawFossil::
	bufferitemname STR_VAR_1, ITEM_CLAW_FOSSIL
	msgbox RustboroCity_DevonCorp_2F_Text_HandedFossilToResearcher, MSGBOX_DEFAULT
	removeitem ITEM_CLAW_FOSSIL
	setvar VAR_FOSSIL_RESURRECTION_STATE, 1
	setvar VAR_WHICH_FOSSIL_REVIVED, 2
	release
	end

RustboroCity_DevonCorp_2F_EventScript_DeclineGiveFossil::
	msgbox RustboroCity_DevonCorp_2F_Text_OhIsThatSo, MSGBOX_DEFAULT
	release
	end

RustboroCity_DevonCorp_2F_EventScript_StillRegenerating::
	msgbox RustboroCity_DevonCorp_2F_Text_FossilRegeneratorTakesTime, MSGBOX_DEFAULT
	release
	end

RustboroCity_DevonCorp_2F_EventScript_FossilMonReady::
	goto_if_eq VAR_WHICH_FOSSIL_REVIVED, 1, RustboroCity_DevonCorp_2F_EventScript_LileepReady
	goto_if_eq VAR_WHICH_FOSSIL_REVIVED, 2, RustboroCity_DevonCorp_2F_EventScript_AnorithReady
	end

RustboroCity_DevonCorp_2F_EventScript_LileepReady::
	bufferspeciesname STR_VAR_2, SPECIES_LILEEP
	msgbox RustboroCity_DevonCorp_2F_Text_FossilizedMonBroughtBackToLife, MSGBOX_DEFAULT
	goto RustboroCity_DevonCorp_2F_EventScript_ReceiveLileep
	end

RustboroCity_DevonCorp_2F_EventScript_AnorithReady::
	bufferspeciesname STR_VAR_2, SPECIES_ANORITH
	msgbox RustboroCity_DevonCorp_2F_Text_FossilizedMonBroughtBackToLife, MSGBOX_DEFAULT
	goto RustboroCity_DevonCorp_2F_EventScript_ReceiveAnorith
	end

RustboroCity_DevonCorp_2F_EventScript_ReceiveLileep::
	setvar VAR_TEMP_TRANSFERRED_SPECIES, SPECIES_LILEEP
	givemon SPECIES_LILEEP, 20
	goto_if_eq VAR_RESULT, MON_GIVEN_TO_PARTY, RustboroCity_DevonCorp_2F_EventScript_ReceiveLileepParty
	goto_if_eq VAR_RESULT, MON_GIVEN_TO_PC, RustboroCity_DevonCorp_2F_EventScript_ReceiveLileepPC
	goto Common_EventScript_NoMoreRoomForPokemon
	end

RustboroCity_DevonCorp_2F_EventScript_ReceiveLileepParty::
	call RustboroCity_DevonCorp_2F_EventScript_ReceivedLileepFanfare
	msgbox gText_NicknameThisPokemon, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, RustboroCity_DevonCorp_2F_EventScript_FinishReceivingLileep
	call Common_EventScript_GetGiftMonPartySlot
	call Common_EventScript_NameReceivedPartyMon
	goto RustboroCity_DevonCorp_2F_EventScript_FinishReceivingLileep
	end

RustboroCity_DevonCorp_2F_EventScript_ReceiveLileepPC::
	call RustboroCity_DevonCorp_2F_EventScript_ReceivedLileepFanfare
	msgbox gText_NicknameThisPokemon, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, RustboroCity_DevonCorp_2F_EventScript_TransferLileepToPC
	call Common_EventScript_NameReceivedBoxMon
	goto RustboroCity_DevonCorp_2F_EventScript_TransferLileepToPC
	end

RustboroCity_DevonCorp_2F_EventScript_TransferLileepToPC::
	call Common_EventScript_TransferredToPC
	goto RustboroCity_DevonCorp_2F_EventScript_FinishReceivingLileep
	end

RustboroCity_DevonCorp_2F_EventScript_ReceivedLileepFanfare::
	bufferspeciesname STR_VAR_2, SPECIES_LILEEP
	playfanfare MUS_OBTAIN_ITEM
	message RustboroCity_DevonCorp_2F_Text_ReceivedMonFromResearcher
	waitmessage
	waitfanfare
	bufferspeciesname STR_VAR_1, SPECIES_LILEEP
	return

RustboroCity_DevonCorp_2F_EventScript_FinishReceivingLileep::
	setvar VAR_FOSSIL_RESURRECTION_STATE, 0
	setflag FLAG_RECEIVED_REVIVED_FOSSIL_MON
	release
	end

RustboroCity_DevonCorp_2F_EventScript_ReceiveAnorith::
	setvar VAR_TEMP_TRANSFERRED_SPECIES, SPECIES_ANORITH
	givemon SPECIES_ANORITH, 20
	goto_if_eq VAR_RESULT, MON_GIVEN_TO_PARTY, RustboroCity_DevonCorp_2F_EventScript_ReceiveAnorithParty
	goto_if_eq VAR_RESULT, MON_GIVEN_TO_PC, RustboroCity_DevonCorp_2F_EventScript_ReceiveAnorithPC
	goto Common_EventScript_NoMoreRoomForPokemon
	end

RustboroCity_DevonCorp_2F_EventScript_ReceiveAnorithParty::
	call RustboroCity_DevonCorp_2F_EventScript_ReceivedAnorithFanfare
	msgbox gText_NicknameThisPokemon, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, RustboroCity_DevonCorp_2F_EventScript_FinishReceivingAnorith
	call Common_EventScript_GetGiftMonPartySlot
	call Common_EventScript_NameReceivedPartyMon
	goto RustboroCity_DevonCorp_2F_EventScript_FinishReceivingAnorith
	end

RustboroCity_DevonCorp_2F_EventScript_ReceiveAnorithPC::
	call RustboroCity_DevonCorp_2F_EventScript_ReceivedAnorithFanfare
	msgbox gText_NicknameThisPokemon, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, RustboroCity_DevonCorp_2F_EventScript_TransferAnorithToPC
	call Common_EventScript_NameReceivedBoxMon
	goto RustboroCity_DevonCorp_2F_EventScript_TransferAnorithToPC
	end

RustboroCity_DevonCorp_2F_EventScript_TransferAnorithToPC::
	call Common_EventScript_TransferredToPC
	goto RustboroCity_DevonCorp_2F_EventScript_FinishReceivingAnorith
	end

RustboroCity_DevonCorp_2F_EventScript_ReceivedAnorithFanfare::
	bufferspeciesname STR_VAR_2, SPECIES_ANORITH
	playfanfare MUS_OBTAIN_ITEM
	message RustboroCity_DevonCorp_2F_Text_ReceivedMonFromResearcher
	waitmessage
	waitfanfare
	bufferspeciesname STR_VAR_1, SPECIES_ANORITH
	return

RustboroCity_DevonCorp_2F_EventScript_FinishReceivingAnorith::
	setvar VAR_FOSSIL_RESURRECTION_STATE, 0
	setflag FLAG_RECEIVED_REVIVED_FOSSIL_MON
	release
	end

RustboroCity_DevonCorp_2F_EventScript_ChooseFossil::
	message RustboroCity_DevonCorp_2F_Text_TwoFossilsPickOne
	waitmessage
	multichoice 17, 6, MULTI_FOSSIL, FALSE
	switch VAR_RESULT
	case 0, RustboroCity_DevonCorp_2F_EventScript_ChooseClawFossil
	case 1, RustboroCity_DevonCorp_2F_EventScript_ChooseRootFossil
	case 2, RustboroCity_DevonCorp_2F_EventScript_CancelFossilSelect
	case MULTI_B_PRESSED, RustboroCity_DevonCorp_2F_EventScript_CancelFossilSelect
	end

RustboroCity_DevonCorp_2F_EventScript_ChooseClawFossil::
	goto RustboroCity_DevonCorp_2F_EventScript_GiveClawFossil
	end

RustboroCity_DevonCorp_2F_EventScript_ChooseRootFossil::
	goto RustboroCity_DevonCorp_2F_EventScript_GiveRootFossil
	end

RustboroCity_DevonCorp_2F_EventScript_CancelFossilSelect::
	release
	end

RustboroCity_DevonCorp_2F_EventScript_MatchCallScientist::
	lock
	faceplayer
	call_if_eq VAR_FOSSIL_RESURRECTION_STATE, 1, RustboroCity_DevonCorp_2F_EventScript_SetFossilReady
	goto_if_ge VAR_RUSTBORO_CITY_STATE, 6, RustboroCity_DevonCorp_2F_EventScript_WorkOnNext
	msgbox RustboroCity_DevonCorp_2F_Text_DevelopNewPokenavFeature, MSGBOX_DEFAULT
	release
	end

RustboroCity_DevonCorp_2F_EventScript_WorkOnNext::
	msgbox RustboroCity_DevonCorp_2F_Text_WhatToWorkOnNext, MSGBOX_DEFAULT
	release
	end

RustboroCity_DevonCorp_2F_Text_DeviceForTalkingToPokemon:
	.string "We're developing a device for talking\n"
	.string "with POKéMON.\p"
	.string "But we haven't had much success…$"

RustboroCity_DevonCorp_2F_Text_DevelopingNewBalls:
	.string "I'm developing new kinds of\n"
	.string "POKé BALLS…\p"
	.string "But I haven't made much headway…$"

RustboroCity_DevonCorp_2F_Text_WeFinallyMadeNewBalls:
	.string "We finally made new kinds of\n"
	.string "POKé BALLS!\p"
	.string "The REPEAT BALL makes it easier to\n"
	.string "catch POKéMON you've caught before.\p"
	.string "The TIMER BALL gets better at catching\n"
	.string "POKéMON the longer a battle runs.\p"
	.string "Both are proudly developed by\n"
	.string "the DEVON CORPORATION.\p"
	.string "Please give them a try!$"

RustboroCity_DevonCorp_2F_Text_IMadePokenav:
	.string "I made the POKéNAV!\p"
	.string "As an engineer, I feel blessed to have\n"
	.string "made something so great!$"

RustboroCity_DevonCorp_2F_Text_WowThatsAPokenav:
	.string "Oh, wow!\n"
	.string "That's a POKéNAV!\p"
	.string "It came about as a result of our\n"
	.string "PRESIDENT's desire to learn about\l"
	.string "the feelings of POKéMON.\p"
	.string "Would you like me to describe its\n"
	.string "features in detail?\p"
	.string "No, no. I think you'll find out just by\n"
	.string "trying the POKéNAV out.$"

RustboroCity_DevonCorp_2F_Text_DeviceToVisualizePokemonDreams:
	.string "I'm trying to develop a device that\n"
	.string "visually reproduces the dreams of\l"
	.string "POKéMON…\p"
	.string "But it's not going well.$"

RustboroCity_DevonCorp_2F_Text_DevelopDeviceToResurrectFossils:
.string "{252}{25}{29}{2}{0}{244}{8}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{35}{0}{0}{244}{8}{1}{252}{25}{39}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{39}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{41}{2}{0}{244}{8}{1}{252}{25}{23}{0}{0}{244}{9}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{166}{1}{0}{244}{6}{1}{252}{25}{32}{0}{0}{244}{7}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{140}{2}{0}{244}{10}{1}{252}{25}{146}{1}{0}{244}{6}{1}{252}{25}{31}{0}{0}{244}{7}{1}\n{252}{25}{121}{0}{0}{244}{6}{1}{252}{25}{80}{0}{0}{244}{6}{1}{252}{25}{26}{0}{0}{244}{7}{1}{252}{25}{0}{0}{0}{244}{5}{1}{252}{25}{32}{0}{0}{244}{7}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{13}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{36}{0}{0}{244}{8}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{45}{0}{0}{244}{6}{1}{252}{25}{56}{0}{0}{244}{7}{1}{252}{25}{41}{0}{0}{244}{6}{1}…\p{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{41}{0}{0}{244}{6}{1}{252}{25}{7}{0}{0}{244}{5}{1}{252}{25}{44}{2}{0}{244}{7}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{4}{0}{0}{244}{6}{1}{252}{25}{90}{1}{0}{244}{6}{1}{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{92}{1}{0}{244}{7}{1}{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{106}{1}{0}{244}{6}{1}{252}{25}{42}{0}{0}{244}{6}{1}!$"

RustboroCity_DevonCorp_2F_Text_WantToBringFossilBackToLife:
	.string "Wait! That thing you have there…\n"
	.string "Is that a POKéMON fossil?\p"
	.string "Would you like to bring that POKéMON\n"
	.string "back to life?\p"
	.string "I can with my newly developed\n"
	.string "FOSSIL REGENERATOR.$"

RustboroCity_DevonCorp_2F_Text_OhIsThatSo:
	.string "Oh, is that so?\p"
	.string "DEVON's technological expertise\n"
	.string "is outstanding, I tell you.$"

RustboroCity_DevonCorp_2F_Text_TwoFossilsPickOne:
	.string "Oh, now that's a surprise!\n"
	.string "You have not one, but two, fossils?\p"
	.string "Unfortunately, my machine can only\n"
	.string "regenerate one POKéMON at a time.\p"
	.string "Would you like to pick one of your\n"
	.string "fossils for regeneration?$"

RustboroCity_DevonCorp_2F_Text_HandedFossilToResearcher:
	.string "Excellent!\n"
	.string "Let's do this right away.\p"
	.string "{PLAYER} handed the {STR_VAR_1} to\n"
	.string "the DEVON RESEARCHER.$"

RustboroCity_DevonCorp_2F_Text_FossilRegeneratorTakesTime:
.string "FOSSIL REGENERATOR \n{252}{25}{154}{0}{0}{244}{7}{1}{252}{25}{29}{2}{0}{244}{8}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{45}{0}{0}{244}{6}{1}{252}{25}{105}{1}{0}{244}{5}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{8}{2}{0}{244}{7}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{10}{0}{0}{244}{7}{1}{252}{25}{46}{1}{0}{244}{6}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{154}{0}{0}{244}{7}{1}{252}{25}{69}{1}{0}{244}{8}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{223}{0}{0}{244}{7}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{8}{0}{0}{244}{6}{1}\p{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{66}{1}{0}{244}{7}{1}{252}{25}{134}{0}{0}{244}{7}{1}{252}{25}{85}{1}{0}{244}{6}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{140}{0}{0}{244}{6}{1}{252}{25}{39}{0}{0}{244}{6}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{77}{1}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{46}{0}{0}{244}{7}{1}{252}{25}{224}{0}{0}{244}{8}{1}{252}{25}{12}{0}{0}{244}{4}{1} \n{252}{25}{4}{1}{0}{244}{7}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{93}{1}{0}{244}{7}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{4}{0}{0}{244}{6}{1}{252}{25}{90}{1}{0}{244}{6}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{42}{0}{0}{244}{6}{1}{252}{25}{41}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{117}{1}{0}{244}{11}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{30}{0}{0}{244}{8}{1}\p{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{35}{0}{0}{244}{8}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{7}{0}{0}{244}{5}{1}{252}{25}{84}{2}{0}{244}{7}{1}{252}{25}{30}{0}{0}{244}{8}{1} {252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{83}{1}{0}{244}{6}{1}{252}{25}{48}{0}{0}{244}{6}{1}… {252}{25}{41}{0}{0}{244}{6}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{32}{0}{0}{244}{7}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{64}{0}{0}{244}{7}{1}{252}{25}{30}{0}{0}{244}{8}{1}\n{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{79}{1}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{209}{1}{0}{244}{7}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{31}{0}{0}{244}{7}{1} {252}{25}{1}{0}{0}{244}{6}{1} {252}{25}{50}{2}{0}{244}{6}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{41}{2}{0}{244}{8}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{46}{0}{0}{244}{7}{1}{252}{25}{38}{0}{0}{244}{7}{1}?$"

RustboroCity_DevonCorp_2F_Text_FossilizedMonBroughtBackToLife:
	.string "Thanks for waiting!\p"
	.string "Your fossilized POKéMON has been\n"
	.string "brought back to life!\p"
	.string "The fossil was an ancient POKéMON.\n"
	.string "{STR_VAR_2}, it was!$"

RustboroCity_DevonCorp_2F_Text_ReceivedMonFromResearcher:
	.string "{PLAYER} received {STR_VAR_2} from\n"
	.string "the DEVON RESEARCHER.$"

@ Unused
RustboroCity_DevonCorp_2F_Text_TooManyPokemon:
	.string "Uh-oh, you've got too many POKéMON.\n"
	.string "You have no room for this one.$"

RustboroCity_DevonCorp_2F_Text_DevelopNewPokenavFeature:
	.string "I'm trying to develop a new feature\n"
	.string "for the POKéNAV…\p"
	.string "But it's not going well.$"

RustboroCity_DevonCorp_2F_Text_WhatToWorkOnNext:
.string "{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{79}{1}{0}{244}{6}{1}{252}{25}{7}{0}{0}{244}{5}{1} \n{252}{25}{66}{1}{0}{244}{7}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{32}{0}{0}{244}{7}{1}{252}{25}{13}{0}{0}{244}{6}{1}{252}{25}{7}{0}{0}{244}{5}{1}{252}{25}{41}{2}{0}{244}{8}{1}{252}{25}{23}{0}{0}{244}{9}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{7}{0}{0}{244}{5}{1}{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{123}{0}{0}{244}{7}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{7}{0}{0}{244}{5}{1}?\p{252}{25}{31}{0}{0}{244}{7}{1}{252}{25}{78}{0}{0}{244}{6}{1}{252}{25}{249}{2}{0}{244}{8}{1}{252}{25}{28}{0}{0}{244}{7}{1}{252}{25}{9}{0}{0}{244}{6}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{71}{0}{0}{244}{7}{1}{252}{25}{25}{0}{0}{244}{7}{1}{252}{25}{0}{0}{0}{244}{5}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{45}{0}{0}{244}{6}{1}{252}{25}{4}{0}{0}{244}{6}{1}{252}{25}{109}{1}{0}{244}{7}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{32}{0}{0}{244}{7}{1}{252}{25}{165}{0}{0}{244}{6}{1}{252}{25}{39}{0}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}\n{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{37}{2}{0}{244}{9}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{25}{0}{0}{244}{7}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{41}{0}{0}{244}{6}{1}{252}{25}{4}{0}{0}{244}{6}{1}{252}{25}{13}{0}{0}{244}{6}{1}{252}{25}{4}{0}{0}{244}{6}{1}{252}{25}{109}{1}{0}{244}{7}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{41}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{39}{0}{0}{244}{6}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{8}{2}{0}{244}{7}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{13}{0}{0}{244}{6}{1}{252}{25}{78}{0}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}\p{252}{25}{101}{2}{0}{244}{10}{1}{252}{25}{46}{0}{0}{244}{7}{1}{252}{25}{46}{2}{0}{244}{5}{1}{252}{25}{31}{0}{0}{244}{7}{1}{252}{25}{80}{0}{0}{244}{6}{1}{252}{25}{43}{0}{0}{244}{7}{1}{252}{25}{42}{0}{0}{244}{6}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{106}{1}{0}{244}{6}{1}{252}{25}{42}{0}{0}{244}{6}{1} \n{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{76}{1}{0}{244}{7}{1}{252}{25}{134}{0}{0}{244}{7}{1}{252}{25}{45}{0}{0}{244}{6}{1}{252}{25}{37}{0}{0}{244}{7}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{35}{0}{0}{244}{8}{1}{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{42}{0}{0}{244}{6}{1}{252}{25}{25}{0}{0}{244}{7}{1}{252}{25}{106}{1}{0}{244}{6}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{46}{0}{0}{244}{7}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{123}{0}{0}{244}{7}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{80}{1}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{178}{0}{0}{244}{8}{1}{252}{25}{142}{0}{0}{244}{6}{1}{252}{25}{8}{0}{0}{244}{6}{1}$"

