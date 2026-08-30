Route116_TunnelersRestHouse_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Route116_TunnelersRestHouse_OnTransition
	.byte 0

Route116_TunnelersRestHouse_OnTransition:
	setflag FLAG_LANDMARK_TUNNELERS_REST_HOUSE
	end

Route116_TunnelersRestHouse_EventScript_Tunneler1::
	msgbox Route116_TunnelersRestHouse_Text_WeHadToStopBoring, MSGBOX_NPC
	end

Route116_TunnelersRestHouse_EventScript_Tunneler2::
	msgbox Route116_TunnelersRestHouse_Text_ManDiggingHisWayToVerdanturf, MSGBOX_NPC
	end

Route116_TunnelersRestHouse_EventScript_Tunneler3::
	lock
	faceplayer
	goto_if_set FLAG_RUSTURF_TUNNEL_OPENED, Route116_TunnelersRestHouse_EventScript_TunnelOpened
	msgbox Route116_TunnelersRestHouse_Text_GetToVerdanturfWithoutTunnel, MSGBOX_DEFAULT
	release
	end

Route116_TunnelersRestHouse_EventScript_TunnelOpened::
	msgbox Route116_TunnelersRestHouse_Text_TunnelHasGoneThrough, MSGBOX_DEFAULT
	release
	end

Route116_TunnelersRestHouse_Text_WeHadToStopBoring:
	.string "That RUSTURF TUNNEL there…\p"
	.string "At first, we had a huge work crew boring\n"
	.string "through rock with the latest machinery.\l"
	.string "But, we had to stop.\p"
	.string "It turns out that we would have had\n"
	.string "a negative effect on wild POKéMON in\l"
	.string "the area.\p"
	.string "So, we've got nothing to do but loll\n"
	.string "around here doing nothing.$"

Route116_TunnelersRestHouse_Text_ManDiggingHisWayToVerdanturf:
	.string "There's a man digging his way to\n"
	.string "VERDANTURF all by his lonesome.\l"
	.string "He's desperate to get through.\p"
	.string "He says that if he digs little by little\n"
	.string "without using machines, he won't\l"
	.string "disturb POKéMON, and he'll avoid\l"
	.string "harming the natural environment.\p"
	.string "I wonder if he made it through yet.$"

Route116_TunnelersRestHouse_Text_GetToVerdanturfWithoutTunnel:
	.string "To get to VERDANTURF without using\n"
	.string "this TUNNEL, you'd have to cross the\l"
	.string "sea to DEWFORD, sail on to SLATEPORT,\l"
	.string "then travel through MAUVILLE.$"

Route116_TunnelersRestHouse_Text_TunnelHasGoneThrough:
.string "{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{92}{1}{0}{244}{7}{1}{252}{25}{77}{0}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{46}{0}{0}{244}{7}{1}{252}{25}{21}{1}{0}{244}{6}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{45}{2}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}? {252}{25}{166}{1}{0}{244}{6}{1}{252}{25}{0}{0}{0}{244}{5}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{123}{2}{0}{244}{7}{1}{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{32}{0}{0}{244}{7}{1}\n{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{19}{1}{0}{244}{7}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{55}{0}{0}{244}{6}{1}{252}{25}{25}{0}{0}{244}{7}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{7}{0}{0}{244}{5}{1}{252}{25}{141}{1}{0}{244}{6}{1}{252}{25}{25}{0}{0}{244}{7}{1}{252}{25}{28}{0}{0}{244}{7}{1}{252}{25}{7}{0}{0}{244}{5}{1}{252}{25}{162}{1}{0}{244}{6}{1}{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{106}{1}{0}{244}{6}{1}{252}{25}{42}{0}{0}{244}{6}{1}!\p{252}{25}{31}{0}{0}{244}{7}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{10}{0}{0}{244}{7}{1}{252}{25}{93}{2}{0}{244}{7}{1}{252}{25}{12}{0}{0}{244}{4}{1} {252}{25}{94}{1}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{32}{0}{0}{244}{7}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{27}{0}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{106}{1}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}\n{252}{25}{35}{0}{0}{244}{8}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{10}{0}{0}{244}{7}{1}{252}{25}{42}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{40}{2}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{0}{2}{0}{244}{6}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{8}{2}{0}{244}{7}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{13}{0}{0}{244}{6}{1}{252}{25}{78}{0}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{92}{1}{0}{244}{7}{1}$"

