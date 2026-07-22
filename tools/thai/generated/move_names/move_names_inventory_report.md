# Move Name Inventory Report

- Move entries: **355**
- Current fixed slot: **13 bytes including EOS**
- Thai positioned command: **8 bytes per cluster**
- Seeded Thai examples: **3**
- Seeded examples fitting current slot: **0/3**

## Seeded examples

| Constant | English | Thai draft | Clusters | Encoded bytes | Fits slot |
|---|---|---|---:|---:|---|
| `MOVE_TACKLE` | `TACKLE` | `พุ่งชน` | 4 | 33 | NO |
| `MOVE_EMBER` | `EMBER` | `สะเก็ดไฟ` | 7 | 57 | NO |
| `MOVE_THUNDERBOLT` | `THUNDERBOLT` | `แสนโวลต์` | 7 | 57 | NO |

## Conclusion

The current fixed-width `gMoveNames[][13]` layout cannot hold ordinary Thai precompose names.
The move-name storage architecture must be changed before production Thai names are inserted.
