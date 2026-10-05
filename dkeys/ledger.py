"""副本钥匙：每服务日限量发放、跨日重置、未用钥匙作废，带文本存档。

缺陷：跨服务日不自动重置、切日不清理未用钥匙、同一个 req_id 重复发放、
存档漏写未用钥匙（往返丢数据）、查询全扫玩家。
"""


class Ledger:
    """钥匙台账。"""

    def __init__(self, limit):
        self.limit = limit
        self.day = 1
        self.issued = {}
        self.pending = {}
        self.seen = set()
        self.work = 0

    def issue(self, req_id, player, day, at_ms):
        """发一把钥匙，返回是否成功。缺陷：不查 req_id、不按 day 重置。"""
        self.day = day
        used = self.issued.get(player, 0)
        if used >= self.limit:
            return False
        self.issued[player] = used + 1
        self.pending[player] = self.pending.get(player, 0) + 1
        return True

    def use(self, player, count):
        """用掉若干把钥匙。缺陷：不校验够不够。"""
        self.pending[player] = self.pending.get(player, 0) - count
        return True

    def roll_day(self, day):
        """切到新服务日，返回作废的未用钥匙数。缺陷：不清已发计数也不作废未用钥匙。"""
        self.day = day
        return 0

    def remaining(self, player, day):
        """当日还能领几把。缺陷：全扫玩家表。"""
        self.work += len(self.issued)
        return self.limit - self.issued.get(player, 0)

    def dump(self):
        """序列化台账。缺陷：不写未用钥匙，也不写已用记录。"""
        lines = ["limit=%d" % self.limit, "day=%d" % self.day]
        for player, used in sorted(self.issued.items()):
            lines.append("issued %s %d" % (player, used))
        return "\n".join(lines) + "\n"

    @classmethod
    def load(cls, text):
        """从文本恢复台账。"""
        ledger = cls(1)
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            if line.startswith("limit="):
                ledger.limit = int(line.split("=", 1)[1])
            elif line.startswith("day="):
                ledger.day = int(line.split("=", 1)[1])
            elif line.startswith("issued "):
                _, player, used = line.split()
                ledger.issued[player] = int(used)
        return ledger

    def work_count(self):
        return self.work
