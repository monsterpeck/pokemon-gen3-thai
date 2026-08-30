Route114_FossilManiacsHouse_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Route114_FossilManiacsHouse_OnTransition
	.byte 0

Route114_FossilManiacsHouse_OnTransition:
	setflag FLAG_LANDMARK_FOSSIL_MANIACS_HOUSE
	end

Route114_FossilManiacsHouse_EventScript_FossilManiacsBrother::
	lock
	faceplayer
	goto_if_set FLAG_RECEIVED_TM_DIG, Route114_FossilManiacsHouse_EventScript_ReceivedDig
	msgbox Route114_FossilManiacsHouse_Text_HaveThisToDigLikeMyBrother, MSGBOX_DEFAULT
	giveitem ITEM_TM_DIG
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag FLAG_RECEIVED_TM_DIG
	release
	end

Route114_FossilManiacsHouse_EventScript_ReceivedDig::
	msgbox Route114_FossilManiacsHouse_Text_DigReturnsYouToEntrance, MSGBOX_DEFAULT
	release
	end

Route114_FossilManiacsHouse_EventScript_RockDisplay::
	msgbox Route114_FossilManiacsHouse_Text_RocksFillDisplayCase, MSGBOX_SIGN
	end

Route114_FossilManiacsHouse_EventScript_Bookshelf::
	msgbox Route114_FossilManiacsHouse_Text_CrammedWithBooks, MSGBOX_SIGN
	end

Route114_FossilManiacsHouse_Text_HaveThisToDigLikeMyBrother:
	.string "My big brother's the FOSSIL MANIAC…\n"
	.string "He's a nice guy who loves FOSSILS…\p"
	.string "He loves digging holes, too…\n"
	.string "He dug this hole by himself…\p"
	.string "You can have this, so you can DIG\n"
	.string "holes just like my big brother…$"

Route114_FossilManiacsHouse_Text_DigReturnsYouToEntrance:
	.string "If you make a POKéMON DIG inside a\n"
	.string "cave, you're returned to the entrance…$"

Route114_FossilManiacsHouse_Text_RocksFillDisplayCase:
.string "{252}{25}{209}{2}{0}{244}{7}{1}{252}{25}{28}{2}{0}{244}{6}{1}{252}{25}{25}{0}{0}{244}{7}{1}{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{45}{0}{0}{244}{6}{1}{252}{25}{25}{0}{0}{244}{7}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{4}{2}{0}{244}{7}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{32}{0}{0}{244}{7}{1}{252}{25}{92}{1}{0}{244}{7}{1}{252}{25}{42}{0}{0}{244}{6}{1}{252}{25}{39}{0}{0}{244}{6}{1}\n{252}{25}{82}{0}{0}{244}{7}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{223}{1}{0}{244}{5}{1}{252}{25}{32}{0}{0}{244}{7}{1}{252}{25}{28}{0}{0}{244}{7}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{32}{0}{0}{244}{7}{1}{252}{25}{41}{0}{0}{244}{6}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{26}{0}{0}{244}{7}{1}{252}{25}{6}{0}{0}{244}{4}{1}…$"

Route114_FossilManiacsHouse_Text_CrammedWithBooks:
	.string "THE COMPOSITION OF STRATA…\n"
	.string "HOW RAIN SHAPES THE LAND…\l"
	.string "STONES, SOIL, AND ROCK…\p"
	.string "It's crammed with books.$"

