MysteryGiftScript_BattleCard::
	setvaddress MysteryGiftScript_BattleCard
	vgoto_if_set FLAG_MYSTERY_GIFT_DONE, MysteryGiftScript_BattleCardInfo
	setorcopyvar VAR_RESULT, GET_CARD_BATTLES_WON
	specialvar VAR_0x8008, GetMysteryGiftCardStat
	vgoto_if_ne VAR_0x8008, REQUIRED_CARD_BATTLES, MysteryGiftScript_BattleCardInfo
	lock
	faceplayer
	vmessage sText_MysteryGiftBattleCountCard_WonPrize
	waitmessage
	waitbuttonpress
	giveitem ITEM_POTION
	release
	setflag FLAG_MYSTERY_GIFT_DONE
	end

MysteryGiftScript_BattleCardInfo:
	lock
	faceplayer
	vmessage sText_MysteryGiftBattleCountCard
	waitmessage
	waitbuttonpress
	release
	end

sText_MysteryGiftBattleCountCard:
.string "ขอบคุณที่ใช้ระบบของขวัญ\nลึกลับ.\pแบทเทิลเคานต์การ์ดของคุณจะ\nบันทึกผลการต่อสู้กับเทรนเนอร์\lที่ถือการ์ดแบบเดียวกัน.\pลองตามหาและต่อสู้กับเทรนเนอร์\nที่ถือการ์ดแบบเดียวกับคุณ.\pคุณตรวจอันดับรวมได้\nจากการอ่านข่าว.\pลองใช้ดูนะ!$"

sText_MysteryGiftBattleCountCard_WonPrize:
.string "ขอบคุณที่ใช้ระบบของขวัญ\nลึกลับ.\pยินดีด้วย!\pคุณได้รับรางวัลจากการชนะ\nการต่อสู้ครบสามครั้ง!\pหวังว่าคุณจะมีกำลังใจ\nออกไปต่อสู้อีกนะ.$"
