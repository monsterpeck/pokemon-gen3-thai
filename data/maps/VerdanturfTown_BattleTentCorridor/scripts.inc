VerdanturfTown_BattleTentCorridor_MapScripts::
	map_script MAP_SCRIPT_ON_FRAME_TABLE, VerdanturfTown_BattleTentCorridor_OnFrame
	.byte 0

VerdanturfTown_BattleTentCorridor_OnFrame:
	map_script_2 VAR_TEMP_0, 0, VerdanturfTown_BattleTentCorridor_EventScript_EnterCorridor
	.2byte 0

VerdanturfTown_BattleTentCorridor_EventScript_EnterCorridor::
	lockall
	setvar VAR_TEMP_0, 1
	applymovement LOCALID_VERDANTURF_TENT_CORRIDOR_ATTENDANT, VerdanturfTown_BattleTentCorridor_Movement_WalkToDoor
	applymovement LOCALID_PLAYER, VerdanturfTown_BattleTentCorridor_Movement_WalkToDoor
	waitmovement 0
	opendoor 2, 1
	waitdooranim
	applymovement LOCALID_VERDANTURF_TENT_CORRIDOR_ATTENDANT, VerdanturfTown_BattleTentCorridor_Movement_AttendantEnterDoor
	applymovement LOCALID_PLAYER, VerdanturfTown_BattleTentCorridor_Movement_PlayerEnterDoor
	waitmovement 0
	closedoor 2, 1
	waitdooranim
	setvar VAR_0x8006, 0
	warp MAP_VERDANTURF_TOWN_BATTLE_TENT_BATTLE_ROOM, 6, 5
	waitstate
	releaseall
	end

VerdanturfTown_BattleTentCorridor_Movement_WalkToDoor:
	walk_up
	walk_up
	walk_up
	walk_up
	step_end

VerdanturfTown_BattleTentCorridor_Movement_PlayerEnterDoor:
	walk_up
VerdanturfTown_BattleTentCorridor_Movement_AttendantEnterDoor:
	walk_up
	set_invisible
	step_end


@ Leftover text from when this was a Contest Hall in R/S
@ Unused
VerdanturfTown_ContestHall_Text_WhichContestYouEntering:
.string "คุณจะลงคอนเทสต์ไหน?\nอยากได้คำแนะนำไหม?\pไม่ว่าจะเป็นคอนเทสต์ไหน เช่น\nคอนเทสต์ความน่ารัก ฉันว่าเขาไม่ได้\lตัดสินกันแค่ความน่ารักในรอบแรก\pต้องคิดหาวิธีเลี้ยงโปเกมอน\nให้ดียิ่งขึ้นด้วย$"

@ Unused
VerdanturfTown_ContestHall_Text_RaisedMonToBeCute:
.string "ฉันเลี้ยงโปเกมอนของฉันให้น่ารักมาตลอด\pเพิ่งรู้ว่าเอาโปเกมอน\nลงคอนเทสต์ความน่ารักได้!\pดีใจจังที่เลี้ยงโปเกมอนของฉัน\nด้วยความรักมาตลอด…$"

@ Unused
VerdanturfTown_ContestHall_Text_MyMonRules:
.string "โปเกมอนของฉันสุดยอด!\pทั้งเท่ แกร่ง สวย น่ารัก\nแถมฉลาด ครบทุกด้านเลย!\pแบบนี้ก็ไปคว้าชัยใน\nทุกคอนเทสต์เลยดีกว่า$"

@ Unused
VerdanturfTown_ContestHall_Text_NormalRankStage:
.string "โปเกมอนคอนเทสต์\nเวทีระดับนอร์มอล!$"

