Route113_MapScripts::
	map_script MAP_SCRIPT_ON_RESUME, Route113_OnResume
	map_script MAP_SCRIPT_ON_TRANSITION, Route113_OnTransition
	.byte 0

Route113_OnResume:
	setstepcallback STEP_CB_ASH
	end

Route113_OnTransition:
	clearflag FLAG_FORCE_MIRAGE_TOWER_VISIBLE
	call Route113_EventScript_CheckSetAshWeather
	end

Route113_EventScript_CheckSetAshWeather::
	getplayerxy VAR_TEMP_0, VAR_TEMP_1
	goto_if_lt VAR_TEMP_0, 19, Route113_EventScript_DontSetAshWeather
	goto_if_gt VAR_TEMP_0, 84, Route113_EventScript_DontSetAshWeather
	setweather WEATHER_VOLCANIC_ASH
	return

Route113_EventScript_DontSetAshWeather::
	return

Route113_EventScript_Gentleman::
	msgbox Route113_Text_AshCanBeFashionedIntoGlass, MSGBOX_NPC
	end

Route113_EventScript_NinjaBoy::
	msgbox Route113_Text_FunWalkingThroughAsh, MSGBOX_NPC
	end

Route113_EventScript_RouteSign111::
	msgbox Route113_Text_RouteSign111, MSGBOX_SIGN
	end

Route113_EventScript_RouteSignFallarbor::
	msgbox Route113_Text_RouteSignFallarbor, MSGBOX_SIGN
	end

Route113_EventScript_GlassWorkshopSign::
	msgbox Route113_Text_GlassWorkshopSign, MSGBOX_SIGN
	end

Route113_EventScript_TrainerTipsRegisterKeyItems::
	msgbox Route113_Text_TrainerTipsRegisterKeyItems, MSGBOX_SIGN
	end

Route113_EventScript_Jaylen::
	trainerbattle_single TRAINER_JAYLEN, Route113_Text_JaylenIntro, Route113_Text_JaylenDefeat
	msgbox Route113_Text_JaylenPostBattle, MSGBOX_AUTOCLOSE
	end

Route113_EventScript_Dillon::
	trainerbattle_single TRAINER_DILLON, Route113_Text_DillonIntro, Route113_Text_DillonDefeat
	msgbox Route113_Text_DillonPostBattle, MSGBOX_AUTOCLOSE
	end

Route113_EventScript_Madeline::
	trainerbattle_single TRAINER_MADELINE_1, Route113_Text_MadelineIntro, Route113_Text_MadelineDefeat, Route113_EventScript_RegisterMadeline
	specialvar VAR_RESULT, ShouldTryRematchBattle
	goto_if_eq VAR_RESULT, TRUE, Route113_EventScript_RematchMadeline
	msgbox Route113_Text_MadelinePostBattle, MSGBOX_DEFAULT
	release
	end

Route113_EventScript_RegisterMadeline::
	special PlayerFaceTrainerAfterBattle
	waitmovement 0
	msgbox Route113_Text_MadelineRegister, MSGBOX_DEFAULT
	register_matchcall TRAINER_MADELINE_1
	release
	end

Route113_EventScript_RematchMadeline::
	trainerbattle_rematch TRAINER_MADELINE_1, Route113_Text_MadelineRematchIntro, Route113_Text_MadelineRematchDefeat
	msgbox Route113_Text_MadelinePostRematch, MSGBOX_AUTOCLOSE
	end

Route113_EventScript_Lao::
	trainerbattle_single TRAINER_LAO_1, Route113_Text_LaoIntro, Route113_Text_LaoDefeat, Route113_EventScript_RegisterLao
	specialvar VAR_RESULT, ShouldTryRematchBattle
	goto_if_eq VAR_RESULT, TRUE, Route113_EventScript_RematchLao
	msgbox Route113_Text_LaoPostBattle, MSGBOX_DEFAULT
	release
	end

Route113_EventScript_RegisterLao::
	special PlayerFaceTrainerAfterBattle
	waitmovement 0
	msgbox Route113_Text_LaoRegister, MSGBOX_DEFAULT
	register_matchcall TRAINER_LAO_1
	release
	end

Route113_EventScript_RematchLao::
	trainerbattle_rematch TRAINER_LAO_1, Route113_Text_LaoRematchIntro, Route113_Text_LaoRematchDefeat
	msgbox Route113_Text_LaoPostRematch, MSGBOX_AUTOCLOSE
	end

Route113_EventScript_Lung::
	trainerbattle_single TRAINER_LUNG, Route113_Text_LungIntro, Route113_Text_LungDefeat
	msgbox Route113_Text_LungPostBattle, MSGBOX_AUTOCLOSE
	end

Route113_EventScript_Tori::
	trainerbattle_double TRAINER_TORI_AND_TIA, Route113_Text_ToriIntro, Route113_Text_ToriDefeat, Route113_Text_ToriNotEnoughMons
	msgbox Route113_Text_ToriPostBattle, MSGBOX_AUTOCLOSE
	end

Route113_EventScript_Tia::
	trainerbattle_double TRAINER_TORI_AND_TIA, Route113_Text_TiaIntro, Route113_Text_TiaDefeat, Route113_Text_TiaNotEnoughMons
	msgbox Route113_Text_TiaPostBattle, MSGBOX_AUTOCLOSE
	end

Route113_EventScript_Sophie::
	trainerbattle_single TRAINER_SOPHIE, Route113_Text_SophieIntro, Route113_Text_SophieDefeat
	msgbox Route113_Text_SophiePostBattle, MSGBOX_AUTOCLOSE
	end

Route113_EventScript_Coby::
	trainerbattle_single TRAINER_COBY, Route113_Text_CobyIntro, Route113_Text_CobyDefeat
	msgbox Route113_Text_CobyPostBattle, MSGBOX_AUTOCLOSE
	end

Route113_EventScript_Lawrence::
	trainerbattle_single TRAINER_LAWRENCE, Route113_Text_LawrenceIntro, Route113_Text_LawrenceDefeat
	msgbox Route113_Text_LawrencePostBattle, MSGBOX_AUTOCLOSE
	end

Route113_EventScript_Wyatt::
	trainerbattle_single TRAINER_WYATT, Route113_Text_WyattIntro, Route113_Text_WyattDefeat
	msgbox Route113_Text_WyattPostBattle, MSGBOX_AUTOCLOSE
	end

Route113_Text_AshCanBeFashionedIntoGlass:
.string "{252}{25}{42}{0}{0}{244}{6}{1}{252}{25}{7}{0}{0}{244}{5}{1}{252}{25}{182}{2}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{182}{2}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}! {252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{28}{0}{0}{244}{7}{1}{252}{25}{10}{0}{0}{244}{7}{1}{252}{25}{0}{0}{0}{244}{5}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{0}{0}{0}{244}{5}{1}{252}{25}{41}{0}{0}{244}{6}{1}{252}{25}{135}{0}{0}{244}{6}{1}{252}{25}{45}{0}{0}{244}{6}{1}{252}{25}{44}{2}{0}{244}{7}{1}{252}{25}{39}{0}{0}{244}{6}{1}\n{252}{25}{178}{0}{0}{244}{8}{1}{252}{25}{62}{1}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{69}{1}{0}{244}{8}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{223}{0}{0}{244}{7}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{13}{0}{0}{244}{6}{1}{252}{25}{78}{0}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1} {252}{25}{1}{0}{0}{244}{6}{1}!\p{252}{25}{209}{1}{0}{244}{7}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{94}{1}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{220}{1}{0}{244}{7}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{9}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{36}{0}{0}{244}{8}{1}{252}{25}{35}{0}{0}{244}{8}{1}{252}{25}{42}{0}{0}{244}{6}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{178}{0}{0}{244}{8}{1}{252}{25}{81}{0}{0}{244}{6}{1}\n{252}{25}{44}{2}{0}{244}{7}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{118}{1}{0}{244}{11}{1}{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{32}{0}{0}{244}{7}{1}{252}{25}{117}{1}{0}{244}{11}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{8}{2}{0}{244}{7}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{2}{0}{0}{244}{7}{1}{252}{25}{84}{1}{0}{244}{6}{1}{252}{25}{42}{0}{0}{244}{6}{1}{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{92}{1}{0}{244}{7}{1}$"

Route113_Text_FunWalkingThroughAsh:
.string "{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{64}{0}{0}{244}{7}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{79}{1}{0}{244}{6}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{31}{0}{0}{244}{7}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{94}{1}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{220}{1}{0}{244}{7}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{9}{0}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{36}{0}{0}{244}{8}{1}\n{252}{25}{26}{0}{0}{244}{7}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{117}{2}{0}{244}{9}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{24}{2}{0}{244}{6}{1}{252}{25}{31}{0}{0}{244}{7}{1}{252}{25}{46}{0}{0}{244}{7}{1}{252}{25}{237}{2}{0}{244}{8}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{45}{0}{0}{244}{6}{1}{252}{25}{152}{1}{0}{244}{8}{1}{252}{25}{8}{0}{0}{244}{6}{1}{252}{25}{123}{0}{0}{244}{7}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{7}{0}{0}{244}{5}{1}\p{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{14}{2}{0}{244}{7}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{40}{0}{0}{244}{5}{1}{252}{25}{48}{0}{0}{244}{6}{1}{252}{25}{39}{0}{0}{244}{6}{1}{252}{25}{28}{0}{0}{244}{7}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{154}{0}{0}{244}{7}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{64}{0}{0}{244}{7}{1}{252}{25}{30}{0}{0}{244}{8}{1}{252}{25}{72}{1}{0}{244}{6}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{30}{0}{0}{244}{8}{1}\n{252}{25}{38}{0}{0}{244}{7}{1}{252}{25}{6}{0}{0}{244}{4}{1}{252}{25}{5}{0}{0}{244}{6}{1}{252}{25}{92}{1}{0}{244}{7}{1}{252}{25}{92}{1}{0}{244}{7}{1}{252}{25}{42}{0}{0}{244}{6}{1}{252}{25}{39}{0}{0}{244}{6}{1}{252}{25}{3}{0}{0}{244}{4}{1}{252}{25}{196}{2}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1}{252}{25}{13}{0}{0}{244}{6}{1}{252}{25}{78}{0}{0}{244}{6}{1}{252}{25}{12}{0}{0}{244}{4}{1} {252}{25}{1}{0}{0}{244}{6}{1}!$"

Route113_Text_RouteSign111:
	.string "ROUTE 113\n"
	.string "{RIGHT_ARROW} ROUTE 111$"

Route113_Text_RouteSignFallarbor:
	.string "ROUTE 113\n"
	.string "{LEFT_ARROW} FALLARBOR TOWN$"

Route113_Text_TrainerTipsRegisterKeyItems:
	.string "TRAINER TIPS\p"
	.string "You may register one of the KEY ITEMS\n"
	.string "in your BAG as SELECT.\p"
	.string "Simply press SELECT to use\n"
	.string "the registered item conveniently.$"

Route113_Text_GlassWorkshopSign:
	.string "GLASS WORKSHOP\n"
	.string "“Turning Volcanic Ash into Glass Items”$"

