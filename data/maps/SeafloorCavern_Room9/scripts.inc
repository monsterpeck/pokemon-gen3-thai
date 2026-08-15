SeafloorCavern_Room9_MapScripts::
	.byte 0

SeafloorCavern_Room9_EventScript_ArchieAwakenKyogre::
	lockall
	setvar VAR_0x8004, LOCALID_SEAFLOOR_CAVERN_ARCHIE
	setvar VAR_0x8005, LOCALID_SEAFLOOR_CAVERN_MAXIE
	setvar VAR_0x8006, LOCALID_SEAFLOOR_CAVERN_GRUNT_1
	setvar VAR_0x8007, LOCALID_SEAFLOOR_CAVERN_GRUNT_2
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterUp
	waitmovement 0
	applymovement LOCALID_PLAYER, SeafloorCavern_Room9_Movement_Delay32
	waitmovement 0
	playbgm MUS_ENCOUNTER_AQUA, FALSE
	msgbox SeafloorCavern_Room9_Text_ArchieHoldItRightThere, MSGBOX_DEFAULT
	closemessage
	addobject VAR_0x8004
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterLeft
	waitmovement 0
	applymovement VAR_0x8004, SeafloorCavern_Room9_Movement_ArchieApproachPlayer
	waitmovement 0
	msgbox SeafloorCavern_Room9_Text_ArchieSoItWasYou, MSGBOX_DEFAULT
	applymovement VAR_0x8004, Common_Movement_WalkInPlaceFasterUp
	waitmovement 0
	msgbox SeafloorCavern_Room9_Text_ArchieBeholdKyogre, MSGBOX_DEFAULT
	applymovement VAR_0x8004, Common_Movement_FacePlayer
	waitmovement 0
	msgbox SeafloorCavern_Room9_Text_ArchieYouMustDisappear, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_ARCHIE, SeafloorCavern_Room9_Text_ArchieDefeat
	msgbox SeafloorCavern_Room9_Text_ArchieWithThisRedOrb, MSGBOX_DEFAULT
	setweather WEATHER_NONE
	doweather
	special Script_FadeOutMapMusic
	msgbox SeafloorCavern_Room9_Text_RedOrbShinesByItself, MSGBOX_DEFAULT
	special WaitWeather
	setvar VAR_RESULT, 1
	playse SE_M_DETECT
	dofieldeffectsparkle 16, 42, 0
	waitfieldeffect FLDEFF_SPARKLE
	closemessage
	setvar VAR_RESULT, 0
	playfanfare MUS_AWAKEN_LEGEND
	playse SE_ORB
	special DoOrbEffect
	applymovement VAR_0x8004, Common_Movement_WalkInPlaceFasterUp
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterUp
	waitmovement 0
	delay 150
	removeobject LOCALID_SEAFLOOR_CAVERN_KYOGRE_SLEEPING
	addobject LOCALID_SEAFLOOR_CAVERN_KYOGRE
	waitstate
	delay 60
	applymovement LOCALID_SEAFLOOR_CAVERN_KYOGRE, SeafloorCavern_Room9_Movement_KyogreApproach
	waitmovement 0
	special FadeOutOrbEffect
	setvar VAR_0x8004, 1  @ vertical pan
	setvar VAR_0x8005, 1  @ horizontal pan
	setvar VAR_0x8006, 8  @ num shakes
	setvar VAR_0x8007, 5  @ shake delay
	special ShakeCamera
	waitstate
	applymovement LOCALID_SEAFLOOR_CAVERN_KYOGRE, SeafloorCavern_Room9_Movement_KyogreExit
	waitmovement 0
	removeobject LOCALID_SEAFLOOR_CAVERN_KYOGRE
	delay 4
	setvar VAR_0x8004, 2  @ vertical pan
	setvar VAR_0x8005, 2  @ horizontal pan
	setvar VAR_0x8006, 8  @ num shakes
	setvar VAR_0x8007, 5  @ shake delay
	special ShakeCamera
	waitstate
	delay 30
	setvar VAR_0x8004, LOCALID_SEAFLOOR_CAVERN_ARCHIE
	setvar VAR_0x8005, LOCALID_SEAFLOOR_CAVERN_MAXIE
	setvar VAR_0x8006, LOCALID_SEAFLOOR_CAVERN_GRUNT_1
	setvar VAR_0x8007, LOCALID_SEAFLOOR_CAVERN_GRUNT_2
	msgbox SeafloorCavern_Room9_Text_ArchieWhereDidKyogreGo, MSGBOX_DEFAULT
	playse SE_PC_LOGIN
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterLeft
	waitmovement 0
	msgbox SeafloorCavern_Room9_Text_ArchieAMessageFromOutside, MSGBOX_DEFAULT
	closemessage
	applymovement VAR_0x8004, SeafloorCavern_Room9_Movement_ArchieListenMessage
	waitmovement 0
	msgbox SeafloorCavern_Room9_Text_ArchieWhatRainingTooHard, MSGBOX_DEFAULT
	closemessage
	playse SE_PC_OFF
	delay 20
	applymovement VAR_0x8004, Common_Movement_WalkInPlaceFasterDown
	waitmovement 0
	msgbox SeafloorCavern_Room9_Text_ArchieWhyDidKyogreDisappear, MSGBOX_DEFAULT
	closemessage
	addobject VAR_0x8005
	addobject VAR_0x8006
	addobject VAR_0x8007
	applymovement VAR_0x8007, SeafloorCavern_Room9_Movement_MagmaGruntArrive
	applymovement VAR_0x8006, SeafloorCavern_Room9_Movement_MagmaGruntArrive
	applymovement VAR_0x8005, SeafloorCavern_Room9_Movement_MaxieArrive
	waitmovement 0
	applymovement VAR_0x8004, Common_Movement_WalkInPlaceFasterLeft
	waitmovement 0
	msgbox SeafloorCavern_Room9_Text_MaxieWhatHaveYouWrought, MSGBOX_DEFAULT
	playse SE_PIN
	applymovement VAR_0x8004, Common_Movement_ExclamationMark
	waitmovement 0
	applymovement VAR_0x8004, Common_Movement_Delay48
	waitmovement 0
	msgbox SeafloorCavern_Room9_Text_ArchieDontGetAllHighAndMighty, MSGBOX_DEFAULT
	msgbox SeafloorCavern_Room9_Text_MaxieWeDontHaveTimeToArgue, MSGBOX_DEFAULT
	closemessage
	applymovement VAR_0x8005, SeafloorCavern_Room9_Movement_MaxieExit
	applymovement VAR_0x8004, SeafloorCavern_Room9_Movement_ArchieExit
	waitmovement 0
	msgbox SeafloorCavern_Room9_Text_MaxieComeOnPlayer, MSGBOX_DEFAULT
	setvar VAR_ROUTE128_STATE, 1
	setvar VAR_SOOTOPOLIS_CITY_STATE, 1
	clearflag FLAG_HIDE_SOOTOPOLIS_CITY_STEVEN
	clearflag FLAG_HIDE_SOOTOPOLIS_CITY_ARCHIE
	clearflag FLAG_HIDE_SOOTOPOLIS_CITY_MAXIE
	clearflag FLAG_HIDE_SOOTOPOLIS_CITY_RESIDENTS
	clearflag FLAG_HIDE_SOOTOPOLIS_CITY_GROUDON
	clearflag FLAG_HIDE_SOOTOPOLIS_CITY_KYOGRE
	setflag FLAG_HIDE_SOOTOPOLIS_CITY_MAN_1
	setflag FLAG_LEGENDARIES_IN_SOOTOPOLIS
	clearflag FLAG_HIDE_ROUTE_128_ARCHIE
	clearflag FLAG_HIDE_ROUTE_128_MAXIE
	setflag FLAG_SYS_WEATHER_CTRL
	setflag FLAG_KYOGRE_ESCAPED_SEAFLOOR_CAVERN
	setflag FLAG_HIDE_MOSSDEEP_CITY_STEVENS_HOUSE_STEVEN
	setvar VAR_STEVENS_HOUSE_STATE, 2
	setvar VAR_SEAFLOOR_CAVERN_STATE, 1
	setflag FLAG_HIDE_SEAFLOOR_CAVERN_ROOM_9_ARCHIE
	setflag FLAG_HIDE_SEAFLOOR_CAVERN_ROOM_9_MAXIE
	setflag FLAG_HIDE_SEAFLOOR_CAVERN_ROOM_9_MAGMA_GRUNTS
	setflag FLAG_HIDE_SEAFLOOR_CAVERN_ROOM_9_KYOGRE
	setflag FLAG_HIDE_SEAFLOOR_CAVERN_AQUA_GRUNTS
	setflag FLAG_HIDE_MAP_NAME_POPUP
	warp MAP_ROUTE128, 38, 22
	waitstate
	releaseall
	end

SeafloorCavern_Room9_Movement_ArchieApproachPlayer:
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	step_end

SeafloorCavern_Room9_Movement_Unused1:
	walk_left
	walk_left
	step_end

SeafloorCavern_Room9_Movement_ArchieListenMessage:
	walk_left
	delay_16
	step_end

SeafloorCavern_Room9_Movement_Unused2:
	walk_right
	step_end

SeafloorCavern_Room9_Movement_ArchieExit:
	face_up
	lock_facing_direction
	walk_down
	unlock_facing_direction
	walk_in_place_faster_right
	step_end

SeafloorCavern_Room9_Movement_KyogreApproach:
	delay_16
	delay_16
	walk_slow_down
	delay_16
	delay_16
	delay_16
	walk_slow_down
	delay_16
	delay_16
	delay_16
	step_end

SeafloorCavern_Room9_Movement_KyogreExit:
	slide_up
	slide_up
	step_end

SeafloorCavern_Room9_Movement_MaxieArrive:
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	step_end

SeafloorCavern_Room9_Movement_MaxieExit:
	walk_right
	walk_right
	step_end

SeafloorCavern_Room9_Movement_MagmaGruntArrive:
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	step_end

SeafloorCavern_Room9_Movement_Delay32:
	delay_16
	delay_16
	step_end

SeafloorCavern_Room9_Text_ArchieHoldItRightThere:
.string "อาโอกิริ: หยุดอยู่ตรงนั้น$"

SeafloorCavern_Room9_Text_ArchieSoItWasYou:
.string "อาโอกิริ: หึ ๆ ๆ…\nเป็นแกจริง ๆ สินะ$"

SeafloorCavern_Room9_Text_ArchieBeholdKyogre:
.string "อาโอกิริ: จงดูให้ดี!\pดูร่างอันงดงามของโปเกมอนยุคบรรพกาล\nไคโอกาที่กำลังหลับใหล!\pฉันเฝ้ารอวันนี้มา\nแสนนาน…$"

SeafloorCavern_Room9_Text_ArchieYouMustDisappear:
.string "อาโอกิริ: น่าประหลาดใจจริง ๆ ที่แก\nตามฉันมาถึงที่นี่ได้\pแต่ทุกอย่างจบลงแล้ว\pเพื่อให้ความฝันของฉันเป็นจริง\nแกต้องหายไปเดี๋ยวนี้!$"

SeafloorCavern_Room9_Text_ArchieDefeat:
	.string "What?!\n"
	.string "I lost to a mere child like you?!$"

SeafloorCavern_Room9_Text_ArchieWithThisRedOrb:
.string "อาโอกิริ: หึ ๆ ๆ…\pต้องยอมรับเลยว่าแกมีฝีมือ\nไม่ธรรมดาจริง ๆ\pแต่ว่า!\nฉันมีสิ่งนี้อยู่ในมือ!\pด้วยลูกแก้วสีแดงนี้ ฉันจะทำให้ไคโอกา…$"

SeafloorCavern_Room9_Text_RedOrbShinesByItself:
.string "จู่ ๆ ลูกแก้วสีแดงก็เริ่มส่องแสง\nขึ้นมาเอง!$"

SeafloorCavern_Room9_Text_ArchieWhereDidKyogreGo:
.string "อาโอกิริ: อะไรนะ?!\pฉันยังไม่ได้ทำอะไรเลย\nทำไมลูกแก้วสีแดงถึง…\pไคโอกาหายไปไหนแล้ว?$"

SeafloorCavern_Room9_Text_ArchieAMessageFromOutside:
.string "อาโอกิริ: หืม? ข้อความจาก\nพวกที่อยู่ข้างนอก…$"

SeafloorCavern_Room9_Text_ArchieWhatRainingTooHard:
.string "อาโอกิริ: ว่าไง มีอะไร?\pหืม…\nฝนตกหนักงั้นหรือ?\pดี… ต้องเป็นแบบนั้นอยู่แล้ว\nเราเลยปลุกไคโอกาขึ้นมา\lเพื่อทำให้อุดมการณ์ในการขยายผืนทะเล\lของทีมอควาเป็นจริง\pว่าไงนะ?!\pฝนตกหนักกว่าที่เราคาดไว้มาก?\nพวกแกกำลังตกอยู่ในอันตราย?\pเป็นไปไม่ได้…\nไม่มีทางเป็นแบบนั้น…\pอยู่ประจำตำแหน่งและเฝ้าดู\nสถานการณ์ต่อไป!$"

SeafloorCavern_Room9_Text_ArchieWhyDidKyogreDisappear:
.string "อาโอกิริ: มีอะไรผิดปกติ…\pลูกแก้วสีแดงควรจะปลุก\nและควบคุมไคโอกาได้…\pแต่… ทำไม?\nทำไมไคโอกาถึงหายไป?\pทำไมกัน?!$"

SeafloorCavern_Room9_Text_MaxieWhatHaveYouWrought:
.string "มัตสึบูสะ: แกทำอะไรลงไป?\pอาโอกิริ… ในที่สุดแกก็ปลุกไคโอกา\nขึ้นมาแล้วสินะ?\pถ้าฝนเทลงมาเช่นนี้ชั่วนิรันดร์\nโลกจะเป็นอย่างไร?\pผืนแผ่นดินทั้งโลกจะจมลง\nในทะเลที่สูงขึ้น…$"

SeafloorCavern_Room9_Text_ArchieDontGetAllHighAndMighty:
.string "อาโอกิริ: อะ… อะไรนะ?!\nอย่ามาทำเป็นวางท่าเหนือฉัน!\pทีมแมกมาของแกไม่ใช่หรือ\nที่ทำให้กราดอนโกรธเกรี้ยว?\pตราบใดที่ฉันมีลูกแก้วสีแดง\nฉันก็ควรควบคุมไคโอกาได้…\pฉันควรควบคุมมันได้สิ…$"

SeafloorCavern_Room9_Text_MaxieWeDontHaveTimeToArgue:
.string "มัตสึบูสะ: เราไม่มีเวลา\nมาเถียงกันที่นี่!\pออกไปดูด้วยตาตัวเอง!\pดูเสียว่าโลกที่แกสร้างขึ้น\nคือโลกที่เราปรารถนาจริงหรือ!$"

SeafloorCavern_Room9_Text_MaxieComeOnPlayer:
.string "มัตสึบูสะ: {PLAYER} เร็วเข้า แกเอง\nก็ต้องออกไปจากที่นี่!$"
