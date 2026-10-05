"""副本钥匙：每服务日限量发放、跨日重置、未用钥匙作废，带文本存档。"""


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
        """发一把钥匙，返回是否成功。同一 req_id 幂等，跨日先清零已发计数。"""
        if req_id in self.seen:
            return False
        if day < self.day:
            return False
        if day > self.day:
            self.day = day
            self.issued.clear()
        used = self.issued.get(player, 0)
        if used >= self.limit:
            return False
        self.seen.add(req_id)
        self.issued[player] = used + 1
        self.pending[player] = self.pending.get(player, 0) + 1
        return True

    def use(self, player, count):
        """用掉若干把钥匙，未用钥匙不足时返回 False 且不改状态。"""
        have = self.pending.get(player, 0)
        if count < 0 or count > have:
            return False
        self.pending[player] = have - count
        return True

    def roll_day(self, day):
        """切到新服务日，作废全部未用钥匙并清零已发计数，返回作废数量。"""
        if day <= self.day:
            return 0
        expired = sum(self.pending.values())
        self.pending.clear()
        self.issued.clear()
        self.day = day
        return expired

    def remaining(self, player, day):
        """当日还能领几把。O(1) 查询，不全扫玩家表。"""
        self.work += 1
        if day > self.day:
            return self.limit
        if day < self.day:
            return 0
        return self.limit - self.issued.get(player, 0)

    def dump(self):
        """序列化台账：上限、服务日、已发计数、未用钥匙。"""
        lines = ["limit=%d" % self.limit, "day=%d" % self.day]
        for player, used in sorted(self.issued.items()):
            lines.append("issued %s %d" % (player, used))
        for player, count in sorted(self.pending.items()):
            lines.append("pending %s %d" % (player, count))
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
            elif line.startswith("pending "):
                _, player, count = line.split()
                ledger.pending[player] = int(count)
        return ledger

    def work_count(self):
        return self.work
