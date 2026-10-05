# dungeon-key

副本钥匙：每服务日限量发放、跨日重置、未用钥匙作废，台账能导出成文本再读回来，只用 Python 标准库。

```
python3 -m dkeys.cli --sample limit
python3 -m dkeys.cli --sample day
python3 -m dkeys.cli --sample expire
python3 -m dkeys.cli --sample idem
python3 -m dkeys.cli --sample round
python3 -m dkeys.cli --sample work
python3 -m unittest discover -s tests -v
```

## 口径（README 为准）

- **每日上限**：同一玩家同一服务日最多成功领 `limit` 把钥匙，超出返回 false。
- **跨日重置**：`issue` 收到更大的服务日时，先把已发计数清零再发放。
- **未用作废**：`roll_day` 切到新服务日时把未使用的钥匙作废，并返回作废数量。
- **幂等**：同一个 `req_id` 只发一次，重复调用返回 false。
- **存档往返**：`dump` 写出的文本用 `load` 读回来，服务日、已发数、未用钥匙都要一致。
- **代价**：`remaining` 不许全扫玩家表，`work_count()` 不随玩家数乘查询次数增长；10 万玩家每秒 10 万次查询。

## 输出契约（不改格式）

```
second=..
renew=..
expired=..
pending=..
work=..
```

## 目录

```
dkeys/ledger.py      服务日、上限、作废与存档
dkeys/cli.py         命令行入口（含 --dump / --state）
tests/test_ledger.py unittest 用例
```
