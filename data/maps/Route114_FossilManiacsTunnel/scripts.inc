Route114_FossilManiacsTunnel_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Route114_FossilManiacsTunnel_OnTransition
	map_script MAP_SCRIPT_ON_LOAD, Route114_FossilManiacsTunnel_OnLoad
	.byte 0

Route114_FossilManiacsTunnel_OnTransition:
	call_if_set FLAG_SYS_GAME_CLEAR, Route114_FossilManiacsTunnel_EventScript_MoveFossilManiac
	end

Route114_FossilManiacsTunnel_EventScript_MoveFossilManiac::
	setobjectxyperm LOCALID_FOSSIL_MANIAC, 6, 5
	setobjectmovementtype LOCALID_FOSSIL_MANIAC, MOVEMENT_TYPE_FACE_DOWN
	return

Route114_FossilManiacsTunnel_OnLoad:
	call_if_unset FLAG_SYS_GAME_CLEAR, Route114_FossilManiacsTunnel_EventScript_CloseDesertUnderpass
	end

Route114_FossilManiacsTunnel_EventScript_CloseDesertUnderpass::
	setmetatile 6, 1, METATILE_Fallarbor_RedRockWall, TRUE
	setmetatile 6, 2, METATILE_Fallarbor_RedRockWall, TRUE
	return

Route114_FossilManiacsTunnel_EventScript_ManiacMentionCaveIn::
	lockall
	applymovement LOCALID_FOSSIL_MANIAC, Common_Movement_WalkInPlaceFasterUp
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterDown
	waitmovement 0
	msgbox Route114_FossilManiacsTunnel_Text_NotSafeThatWay, MSGBOX_DEFAULT
	setvar VAR_FOSSIL_MANIAC_STATE, 2
	releaseall
	end

Route114_FossilManiacsTunnel_EventScript_FossilManiac::
	lock
	faceplayer
	goto_if_set FLAG_RECEIVED_REVIVED_FOSSIL_MON, Route114_FossilManiacsTunnel_EventScript_PlayerRevivedFossil
	checkitem ITEM_ROOT_FOSSIL
	goto_if_eq VAR_RESULT, TRUE, Route114_FossilManiacsTunnel_EventScript_PlayerHasFossil
	checkitem ITEM_CLAW_FOSSIL
	goto_if_eq VAR_RESULT, TRUE, Route114_FossilManiacsTunnel_EventScript_PlayerHasFossil
	msgbox Route114_FossilManiacsTunnel_Text_LookInDesertForFossils, MSGBOX_DEFAULT
	release
	end

Route114_FossilManiacsTunnel_EventScript_PlayerHasFossil::
	msgbox Route114_FossilManiacsTunnel_Text_DevonCorpRevivingFossils, MSGBOX_DEFAULT
	release
	end

Route114_FossilManiacsTunnel_EventScript_PlayerRevivedFossil::
	msgbox Route114_FossilManiacsTunnel_Text_FossilsAreWonderful, MSGBOX_DEFAULT
	release
	end

Route114_FossilManiacsTunnel_Text_LookInDesertForFossils:
.string "{252}{25}{29}{2}{0}{244}{8}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{4}{1}{0}{244}{7}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{10}{0}{0}{244}{7}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{10}{0}{0}{244}{7}{1}{252}{25}{75}{2}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{36}{0}{0}{244}{8}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{45}{0}{0}{244}{6}{1}{252}{25}{56}{0}{0}{244}{7}{1}{252}{25}{41}{0}{0}{244}{6}{1}…\n{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{8}{2}{0}{244}{7}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{10}{0}{0}{244}{7}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{123}{0}{0}{244}{7}{1}{252}{25}{154}{0}{0}{244}{7}{1}{252}{25}{46}{2}{0}{244}{5}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{36}{0}{0}{244}{8}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{45}{0}{0}{244}{6}{1}{252}{25}{56}{0}{0}{244}{7}{1}{252}{25}{41}{0}{0}{244}{6}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{8}{0}{0}{244}{6}{1}…\p{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{39}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{92}{1}{0}{244}{7}{1}{252}{25}{36}{0}{0}{244}{8}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{45}{0}{0}{244}{6}{1}{252}{25}{56}{0}{0}{244}{7}{1}{252}{25}{41}{0}{0}{244}{6}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{46}{0}{0}{244}{7}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{48}{0}{0}{244}{6}{1}?\p{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{66}{1}{0}{244}{7}{1}{252}{25}{36}{0}{0}{244}{8}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{45}{0}{0}{244}{6}{1}{252}{25}{56}{0}{0}{244}{7}{1}{252}{25}{41}{0}{0}{244}{6}{1}{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{27}{0}{0}{244}{6}{1}{252}{25}{42}{0}{0}{244}{6}{1}{252}{25}{178}{0}{0}{244}{8}{1}{252}{25}{143}{2}{0}{244}{8}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{46}{0}{0}{244}{7}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{25}{0}{0}{244}{7}{1}\n{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{8}{2}{0}{244}{7}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{9}{0}{0}{244}{6}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{29}{2}{0}{244}{8}{1}{252}{25}{30}{0}{0}{244}{8}{1}… {252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{76}{1}{0}{244}{7}{1}{252}{25}{4}{0}{0}{244}{6}{1}{252}{25}{109}{1}{0}{244}{7}{1}{252}{25}{46}{0}{0}{244}{7}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{8}{0}{0}{244}{6}{1}…\p{252}{25}{94}{1}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{28}{0}{0}{244}{7}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{76}{1}{0}{244}{7}{1}{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{92}{1}{0}{244}{7}{1}{252}{25}{154}{0}{0}{244}{7}{1}{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{76}{1}{0}{244}{7}{1}{252}{25}{134}{0}{0}{244}{7}{1}{252}{25}{36}{0}{0}{244}{8}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{45}{0}{0}{244}{6}{1}{252}{25}{56}{0}{0}{244}{7}{1}{252}{25}{41}{0}{0}{244}{6}{1}\n{252}{25}{41}{0}{0}{244}{6}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{32}{0}{0}{244}{7}{1}{252}{25}{46}{0}{0}{244}{7}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{4}{0}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{28}{0}{0}{244}{7}{1}{252}{25}{7}{0}{0}{244}{5}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{41}{0}{0}{244}{6}{1}{252}{25}{28}{0}{0}{244}{7}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{39}{0}{0}{244}{6}{1}{252}{25}{154}{0}{0}{244}{7}{1}{252}{25}{134}{0}{0}{244}{7}{1}\l{252}{25}{84}{1}{0}{244}{6}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{82}{0}{0}{244}{7}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{24}{2}{0}{244}{6}{1}{252}{25}{31}{0}{0}{244}{7}{1}{252}{25}{28}{0}{0}{244}{7}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{39}{0}{0}{244}{6}{1}{252}{25}{149}{2}{0}{244}{8}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{13}{0}{0}{244}{6}{1}{252}{25}{63}{1}{0}{244}{7}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}\l{252}{25}{36}{0}{0}{244}{8}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{45}{0}{0}{244}{6}{1}{252}{25}{56}{0}{0}{244}{7}{1}{252}{25}{41}{0}{0}{244}{6}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{248}{1}{0}{244}{6}{1}{252}{25}{81}{0}{0}{244}{6}{1}…$"

Route114_FossilManiacsTunnel_Text_DevonCorpRevivingFossils:
	.string "You found a FOSSIL, didn't you?\n"
	.string "That's so nice… It's so dreamy…\p"
	.string "What are you going to do with that\n"
	.string "FOSSIL?\p"
	.string "From what I've heard, DEVON is doing\n"
	.string "research on reviving POKéMON from\l"
	.string "FOSSILS…\p"
	.string "I love my FOSSILS, so I would never\n"
	.string "do anything like that…$"

Route114_FossilManiacsTunnel_Text_FossilsAreWonderful:
.string "{252}{25}{36}{0}{0}{244}{8}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{45}{0}{0}{244}{6}{1}{252}{25}{56}{0}{0}{244}{7}{1}{252}{25}{41}{0}{0}{244}{6}{1}{252}{25}{62}{1}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{12}{0}{0}{244}{4}{1}… {252}{25}{80}{0}{0}{244}{6}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{43}{0}{0}{244}{7}{1}{252}{25}{44}{0}{0}{244}{8}{1}{252}{25}{13}{0}{0}{244}{6}{1}{252}{25}{78}{0}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1} {252}{25}{1}{0}{0}{244}{6}{1}\n…{252}{25}{15}{0}{0}{244}{6}{1}{252}{25}{42}{0}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{40}{2}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{46}{0}{0}{244}{7}{1}{252}{25}{22}{1}{0}{244}{6}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{50}{0}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}…$"

Route114_FossilManiacsTunnel_Text_NotSafeThatWay:
	.string "Oh…\n"
	.string "It's not safe that way…\p"
	.string "I was digging away, you see…\n"
	.string "When the whole wall collapsed…\p"
	.string "I think there's a giant cavern\n"
	.string "underneath now…\p"
	.string "But I've left it alone because I don't\n"
	.string "think there are any FOSSILS there…$"

