const u8 gEasyChatWord_MatchUp[] = _("ประมือ");
const u8 gEasyChatWord_Go[] = _("ลุย");
const u8 gEasyChatWord_No1[] = _("อันดับ 1");
const u8 gEasyChatWord_Decide[] = _("ตัดสิน");
const u8 gEasyChatWord_LetMeWin[] = _("ให้ฉันชนะ");
const u8 gEasyChatWord_Wins[] = _("ชนะ");
const u8 gEasyChatWord_Win[] = _("ชนะ");
const u8 gEasyChatWord_Won[] = _("ชนะแล้ว");
const u8 gEasyChatWord_IfIWin[] = _("ถ้าฉันชนะ");
const u8 gEasyChatWord_WhenIWin[] = _("เมื่อฉันชนะ");
const u8 gEasyChatWord_CantWin[] = _("ชนะไม่ได้");
const u8 gEasyChatWord_CanWin[] = _("ชนะได้");
const u8 gEasyChatWord_NoMatch[] = _("สู้ไม่ได้");
const u8 gEasyChatWord_Spirit[] = _("ใจสู้");
const u8 gEasyChatWord_Decided[] = _("ตัดสินแล้ว");
const u8 gEasyChatWord_TrumpCard[] = _("ไพ่ตาย");
const u8 gEasyChatWord_TakeThat[] = _("รับไปซะ");
const u8 gEasyChatWord_ComeOn[] = _("เข้ามา");
const u8 gEasyChatWord_Attack[] = _("โจมตี");
const u8 gEasyChatWord_Surrender[] = _("ยอมแพ้");
const u8 gEasyChatWord_Gutsy[] = _("ใจกล้า");
const u8 gEasyChatWord_Talent[] = _("ฝีมือ");
const u8 gEasyChatWord_Strategy[] = _("กลยุทธ์");
const u8 gEasyChatWord_Smite[] = _("พิชิต");
const u8 gEasyChatWord_Match[] = _("ประลอง");
const u8 gEasyChatWord_Victory[] = _("ชัยชนะ");
const u8 gEasyChatWord_Offensive[] = _("บุก");
const u8 gEasyChatWord_Sense[] = _("เซนส์");
const u8 gEasyChatWord_Versus[] = _("ปะทะ");
const u8 gEasyChatWord_Fights[] = _("สู้");
const u8 gEasyChatWord_Power[] = _("พลัง");
const u8 gEasyChatWord_Challenge[] = _("ท้าทาย");
const u8 gEasyChatWord_Strong[] = _("แกร่ง");
const u8 gEasyChatWord_TooStrong[] = _("แกร่งเกิน");
const u8 gEasyChatWord_GoEasy[] = _("ออมมือ");
const u8 gEasyChatWord_Foe[] = _("คู่ต่อสู้");
const u8 gEasyChatWord_Genius[] = _("อัจฉริยะ");
const u8 gEasyChatWord_Legend[] = _("ตำนาน");
const u8 gEasyChatWord_Escape[] = _("หนี");
const u8 gEasyChatWord_Aim[] = _("เล็ง");
const u8 gEasyChatWord_Battle[] = _("แบทเทิล");
const u8 gEasyChatWord_Fight[] = _("ต่อสู้");
const u8 gEasyChatWord_Resuscitate[] = _("ฟื้นคืน");
const u8 gEasyChatWord_Points[] = _("คะแนน");
const u8 gEasyChatWord_Serious[] = _("เอาจริง");
const u8 gEasyChatWord_GiveUp[] = _("ยอมแพ้");
const u8 gEasyChatWord_Loss[] = _("พ่ายแพ้");
const u8 gEasyChatWord_IfILose[] = _("ถ้าฉันแพ้");
const u8 gEasyChatWord_Lost[] = _("แพ้แล้ว");
const u8 gEasyChatWord_Lose[] = _("แพ้");
const u8 gEasyChatWord_Guard[] = _("ป้องกัน");
const u8 gEasyChatWord_Partner[] = _("คู่หู");
const u8 gEasyChatWord_Reject[] = _("ปฏิเสธ");
const u8 gEasyChatWord_Accept[] = _("ยอมรับ");
const u8 gEasyChatWord_Invincible[] = _("ไร้พ่าย");
const u8 gEasyChatWord_Received[] = _("ได้รับ");
const u8 gEasyChatWord_Easy[] = _("ง่าย");
const u8 gEasyChatWord_Weak[] = _("อ่อนแอ");
const u8 gEasyChatWord_TooWeak[] = _("อ่อนเกินไป");
const u8 gEasyChatWord_Pushover[] = _("หมู");
const u8 gEasyChatWord_Leader[] = _("ผู้นำ");
const u8 gEasyChatWord_Rule[] = _("กฎ");
const u8 gEasyChatWord_Move[] = _("ท่า");

const struct EasyChatWordInfo gEasyChatGroup_Battle[] = {
    [EC_INDEX(EC_WORD_MATCH_UP)] =
    {
        .text = gEasyChatWord_MatchUp,
        .alphabeticalOrder = EC_INDEX(EC_WORD_ACCEPT),
        .enabled = TRUE,
    },
    [EC_INDEX(EC_WORD_GO)] =
    {
        .text = gEasyChatWord_Go,
        .alphabeticalOrder = EC_INDEX(EC_WORD_AIM),
        .enabled = TRUE,
    },
    [EC_INDEX(EC_WORD_NO_1)] =
    {
        .text = gEasyChatWord_No1,
        .alphabeticalOrder = EC_INDEX(EC_WORD_ATTACK),
        .enabled = TRUE,
    },
    [EC_INDEX(EC_WORD_DECIDE)] =
    {
        .text = gEasyChatWord_Decide,
        .alphabeticalOrder = EC_INDEX(EC_WORD_BATTLE),
        .enabled = TRUE,
    },
    [EC_INDEX(EC_WORD_LET_ME_WIN)] =
    {
        .text = gEasyChatWord_LetMeWin,
        .alphabeticalOrder = EC_INDEX(EC_WORD_CAN_WIN),
        .enabled = TRUE,
    },
    [EC_INDEX(EC_WORD_WINS)] =
    {
        .text = gEasyChatWord_Wins,
        .alphabeticalOrder = EC_INDEX(EC_WORD_CAN_T_WIN),
        .enabled = TRUE,
    },
    [EC_INDEX(EC_WORD_WIN)] =
    {
        .text = gEasyChatWord_Win,
        .alphabeticalOrder = EC_INDEX(EC_WORD_CHALLENGE),
        .enabled = TRUE,
    },
    [EC_INDEX(EC_WORD_WON)] =
    {
        .text = gEasyChatWord_Won,
        .alphabeticalOrder = EC_INDEX(EC_WORD_COME_ON),
        .enabled = TRUE,
    },
    [EC_INDEX(EC_WORD_IF_I_WIN)] =
    {
        .text = gEasyChatWord_IfIWin,
        .alphabeticalOrder = EC_INDEX(EC_WORD_DECIDE),
        .enabled = TRUE,
    },
    [EC_INDEX(EC_WORD_WHEN_I_WIN)] =
    {
        .text = gEasyChatWord_WhenIWin,
        .alphabeticalOrder = EC_INDEX(EC_WORD_DECIDED),
        .enabled = TRUE,
    },
    [EC_INDEX(EC_WORD_CAN_T_WIN)] =
    {
        .text = gEasyChatWord_CantWin,
        .alphabeticalOrder = EC_INDEX(EC_WORD_EASY),
        .enabled = TRUE,
    },
    [EC_INDEX(EC_WORD_CAN_WIN)] =
    {
        .text = gEasyChatWord_CanWin,
        .alphabeticalOrder = EC_INDEX(EC_WORD_ESCAPE),
        .enabled = TRUE,
    },
    [EC_INDEX(EC_WORD_NO_MATCH)] =
    {
        .text = gEasyChatWord_NoMatch,
        .alphabeticalOrder = EC_INDEX(EC_WORD_FIGHT),
        .enabled = TRUE,
    },
    [EC_INDEX(EC_WORD_SPIRIT)] =
    {
        .text = gEasyChatWord_Spirit,
        .alphabeticalOrder = EC_INDEX(EC_WORD_FIGHTS),
        .enabled = TRUE,
    },
    [EC_INDEX(EC_WORD_DECIDED)] =
    {
        .text = gEasyChatWord_Decided,
        .alphabeticalOrder = EC_INDEX(EC_WORD_FOE),
        .enabled = TRUE,
    },
    [EC_INDEX(EC_WORD_TRUMP_CARD)] =
    {
        .text = gEasyChatWord_TrumpCard,
        .alphabeticalOrder = EC_INDEX(EC_WORD_GENIUS),
        .enabled = TRUE,
    },
    [EC_INDEX(EC_WORD_TAKE_THAT)] =
    {
        .text = gEasyChatWord_TakeThat,
        .alphabeticalOrder = EC_INDEX(EC_WORD_GIVE_UP),
        .enabled = TRUE,
    },
    [EC_INDEX(EC_WORD_COME_ON)] =
    {
        .text = gEasyChatWord_ComeOn,
        .alphabeticalOrder = EC_INDEX(EC_WORD_GO),
        .enabled = TRUE,
    },
    [EC_INDEX(EC_WORD_ATTACK)] =
    {
        .text = gEasyChatWord_Attack,
        .alphabeticalOrder = EC_INDEX(EC_WORD_GO_EASY),
        .enabled = TRUE,
    },
    [EC_INDEX(EC_WORD_SURRENDER)] =
    {
        .text = gEasyChatWord_Surrender,
        .alphabeticalOrder = EC_INDEX(EC_WORD_GUARD),
        .enabled = TRUE,
    },
    [EC_INDEX(EC_WORD_GUTSY)] =
    {
        .text = gEasyChatWord_Gutsy,
        .alphabeticalOrder = EC_INDEX(EC_WORD_GUTSY),
        .enabled = TRUE,
    },
    [EC_INDEX(EC_WORD_TALENT)] =
    {
        .text = gEasyChatWord_Talent,
        .alphabeticalOrder = EC_INDEX(EC_WORD_IF_I_LOSE),
        .enabled = TRUE,
    },
    [EC_INDEX(EC_WORD_STRATEGY)] =
    {
        .text = gEasyChatWord_Strategy,
        .alphabeticalOrder = EC_INDEX(EC_WORD_IF_I_WIN),
        .enabled = TRUE,
    },
    [EC_INDEX(EC_WORD_SMITE)] =
    {
        .text = gEasyChatWord_Smite,
        .alphabeticalOrder = EC_INDEX(EC_WORD_INVINCIBLE),
        .enabled = TRUE,
    },
    [EC_INDEX(EC_WORD_MATCH)] =
    {
        .text = gEasyChatWord_Match,
        .alphabeticalOrder = EC_INDEX(EC_WORD_LEADER),
        .enabled = TRUE,
    },
    [EC_INDEX(EC_WORD_VICTORY)] =
    {
        .text = gEasyChatWord_Victory,
        .alphabeticalOrder = EC_INDEX(EC_WORD_LEGEND),
        .enabled = TRUE,
    },
    [EC_INDEX(EC_WORD_OFFENSIVE)] =
    {
        .text = gEasyChatWord_Offensive,
        .alphabeticalOrder = EC_INDEX(EC_WORD_LET_ME_WIN),
        .enabled = TRUE,
    },
    [EC_INDEX(EC_WORD_SENSE)] =
    {
        .text = gEasyChatWord_Sense,
        .alphabeticalOrder = EC_INDEX(EC_WORD_LOSE),
        .enabled = TRUE,
    },
    [EC_INDEX(EC_WORD_VERSUS)] =
    {
        .text = gEasyChatWord_Versus,
        .alphabeticalOrder = EC_INDEX(EC_WORD_LOSS),
        .enabled = TRUE,
    },
    [EC_INDEX(EC_WORD_FIGHTS)] =
    {
        .text = gEasyChatWord_Fights,
        .alphabeticalOrder = EC_INDEX(EC_WORD_LOST),
        .enabled = TRUE,
    },
    [EC_INDEX(EC_WORD_POWER)] =
    {
        .text = gEasyChatWord_Power,
        .alphabeticalOrder = EC_INDEX(EC_WORD_MATCH),
        .enabled = TRUE,
    },
    [EC_INDEX(EC_WORD_CHALLENGE)] =
    {
        .text = gEasyChatWord_Challenge,
        .alphabeticalOrder = EC_INDEX(EC_WORD_MATCH_UP),
        .enabled = TRUE,
    },
    [EC_INDEX(EC_WORD_STRONG)] =
    {
        .text = gEasyChatWord_Strong,
        .alphabeticalOrder = EC_INDEX(EC_WORD_MOVE),
        .enabled = TRUE,
    },
    [EC_INDEX(EC_WORD_TOO_STRONG)] =
    {
        .text = gEasyChatWord_TooStrong,
        .alphabeticalOrder = EC_INDEX(EC_WORD_NO_MATCH),
        .enabled = TRUE,
    },
    [EC_INDEX(EC_WORD_GO_EASY)] =
    {
        .text = gEasyChatWord_GoEasy,
        .alphabeticalOrder = EC_INDEX(EC_WORD_NO_1),
        .enabled = TRUE,
    },
    [EC_INDEX(EC_WORD_FOE)] =
    {
        .text = gEasyChatWord_Foe,
        .alphabeticalOrder = EC_INDEX(EC_WORD_OFFENSIVE),
        .enabled = TRUE,
    },
    [EC_INDEX(EC_WORD_GENIUS)] =
    {
        .text = gEasyChatWord_Genius,
        .alphabeticalOrder = EC_INDEX(EC_WORD_PARTNER),
        .enabled = TRUE,
    },
    [EC_INDEX(EC_WORD_LEGEND)] =
    {
        .text = gEasyChatWord_Legend,
        .alphabeticalOrder = EC_INDEX(EC_WORD_POINTS),
        .enabled = TRUE,
    },
    [EC_INDEX(EC_WORD_ESCAPE)] =
    {
        .text = gEasyChatWord_Escape,
        .alphabeticalOrder = EC_INDEX(EC_WORD_POWER),
        .enabled = TRUE,
    },
    [EC_INDEX(EC_WORD_AIM)] =
    {
        .text = gEasyChatWord_Aim,
        .alphabeticalOrder = EC_INDEX(EC_WORD_PUSHOVER),
        .enabled = TRUE,
    },
    [EC_INDEX(EC_WORD_BATTLE)] =
    {
        .text = gEasyChatWord_Battle,
        .alphabeticalOrder = EC_INDEX(EC_WORD_RECEIVED),
        .enabled = TRUE,
    },
    [EC_INDEX(EC_WORD_FIGHT)] =
    {
        .text = gEasyChatWord_Fight,
        .alphabeticalOrder = EC_INDEX(EC_WORD_REJECT),
        .enabled = TRUE,
    },
    [EC_INDEX(EC_WORD_RESUSCITATE)] =
    {
        .text = gEasyChatWord_Resuscitate,
        .alphabeticalOrder = EC_INDEX(EC_WORD_RESUSCITATE),
        .enabled = TRUE,
    },
    [EC_INDEX(EC_WORD_POINTS)] =
    {
        .text = gEasyChatWord_Points,
        .alphabeticalOrder = EC_INDEX(EC_WORD_RULE),
        .enabled = TRUE,
    },
    [EC_INDEX(EC_WORD_SERIOUS)] =
    {
        .text = gEasyChatWord_Serious,
        .alphabeticalOrder = EC_INDEX(EC_WORD_SENSE),
        .enabled = TRUE,
    },
    [EC_INDEX(EC_WORD_GIVE_UP)] =
    {
        .text = gEasyChatWord_GiveUp,
        .alphabeticalOrder = EC_INDEX(EC_WORD_SERIOUS),
        .enabled = TRUE,
    },
    [EC_INDEX(EC_WORD_LOSS)] =
    {
        .text = gEasyChatWord_Loss,
        .alphabeticalOrder = EC_INDEX(EC_WORD_SMITE),
        .enabled = TRUE,
    },
    [EC_INDEX(EC_WORD_IF_I_LOSE)] =
    {
        .text = gEasyChatWord_IfILose,
        .alphabeticalOrder = EC_INDEX(EC_WORD_SPIRIT),
        .enabled = TRUE,
    },
    [EC_INDEX(EC_WORD_LOST)] =
    {
        .text = gEasyChatWord_Lost,
        .alphabeticalOrder = EC_INDEX(EC_WORD_STRATEGY),
        .enabled = TRUE,
    },
    [EC_INDEX(EC_WORD_LOSE)] =
    {
        .text = gEasyChatWord_Lose,
        .alphabeticalOrder = EC_INDEX(EC_WORD_STRONG),
        .enabled = TRUE,
    },
    [EC_INDEX(EC_WORD_GUARD)] =
    {
        .text = gEasyChatWord_Guard,
        .alphabeticalOrder = EC_INDEX(EC_WORD_SURRENDER),
        .enabled = TRUE,
    },
    [EC_INDEX(EC_WORD_PARTNER)] =
    {
        .text = gEasyChatWord_Partner,
        .alphabeticalOrder = EC_INDEX(EC_WORD_TAKE_THAT),
        .enabled = TRUE,
    },
    [EC_INDEX(EC_WORD_REJECT)] =
    {
        .text = gEasyChatWord_Reject,
        .alphabeticalOrder = EC_INDEX(EC_WORD_TALENT),
        .enabled = TRUE,
    },
    [EC_INDEX(EC_WORD_ACCEPT)] =
    {
        .text = gEasyChatWord_Accept,
        .alphabeticalOrder = EC_INDEX(EC_WORD_TOO_STRONG),
        .enabled = TRUE,
    },
    [EC_INDEX(EC_WORD_INVINCIBLE)] =
    {
        .text = gEasyChatWord_Invincible,
        .alphabeticalOrder = EC_INDEX(EC_WORD_TOO_WEAK),
        .enabled = TRUE,
    },
    [EC_INDEX(EC_WORD_RECEIVED)] =
    {
        .text = gEasyChatWord_Received,
        .alphabeticalOrder = EC_INDEX(EC_WORD_TRUMP_CARD),
        .enabled = TRUE,
    },
    [EC_INDEX(EC_WORD_EASY)] =
    {
        .text = gEasyChatWord_Easy,
        .alphabeticalOrder = EC_INDEX(EC_WORD_VERSUS),
        .enabled = TRUE,
    },
    [EC_INDEX(EC_WORD_WEAK)] =
    {
        .text = gEasyChatWord_Weak,
        .alphabeticalOrder = EC_INDEX(EC_WORD_VICTORY),
        .enabled = TRUE,
    },
    [EC_INDEX(EC_WORD_TOO_WEAK)] =
    {
        .text = gEasyChatWord_TooWeak,
        .alphabeticalOrder = EC_INDEX(EC_WORD_WEAK),
        .enabled = TRUE,
    },
    [EC_INDEX(EC_WORD_PUSHOVER)] =
    {
        .text = gEasyChatWord_Pushover,
        .alphabeticalOrder = EC_INDEX(EC_WORD_WHEN_I_WIN),
        .enabled = TRUE,
    },
    [EC_INDEX(EC_WORD_LEADER)] =
    {
        .text = gEasyChatWord_Leader,
        .alphabeticalOrder = EC_INDEX(EC_WORD_WIN),
        .enabled = TRUE,
    },
    [EC_INDEX(EC_WORD_RULE)] =
    {
        .text = gEasyChatWord_Rule,
        .alphabeticalOrder = EC_INDEX(EC_WORD_WINS),
        .enabled = TRUE,
    },
    [EC_INDEX(EC_WORD_MOVE)] =
    {
        .text = gEasyChatWord_Move,
        .alphabeticalOrder = EC_INDEX(EC_WORD_WON),
        .enabled = TRUE,
    },
};
