"""命令行入口：样例、--dump 导出与 --state 载入。"""

import argparse
import os

from .ledger import Ledger


def build_parser():
    parser = argparse.ArgumentParser(prog="dungeon-key", description="副本钥匙发放")
    parser.add_argument("--sample", default=None, help="limit / day / expire / idem / round / work")
    parser.add_argument("--dump", action="store_true", help="导出存档文本")
    parser.add_argument("--state", default=None, help="载入存档文本并打印未用钥匙")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    if args.sample == "limit":
        ledger = Ledger(1)
        ledger.issue("r1", "p", 1, 0)
        print("second=%s" % str(ledger.issue("r2", "p", 1, 10)).lower())
    elif args.sample == "day":
        ledger = Ledger(1)
        ledger.issue("r1", "p", 1, 0)
        print("renew=%s" % str(ledger.issue("r2", "p", 2, 100)).lower())
    elif args.sample == "expire":
        ledger = Ledger(2)
        ledger.issue("r1", "p", 1, 0)
        print("expired=%d" % ledger.roll_day(2))
    elif args.sample == "idem":
        ledger = Ledger(2)
        ledger.issue("r1", "p", 1, 0)
        print("second=%s" % str(ledger.issue("r1", "p", 1, 10)).lower())
    elif args.sample == "round":
        ledger = Ledger(2)
        ledger.issue("r1", "p", 1, 0)
        text = ledger.dump()
        restored = Ledger.load(text)
        print("pending=%d" % restored.pending.get("p", 0))
    elif args.sample == "work":
        ledger = Ledger(1000000)
        for index in range(3000):
            ledger.issue("r-%d" % index, "p-%d" % index, 1, 0)
        for index in range(3000):
            ledger.remaining("p-0", 1)
        print("work=%d" % ledger.work_count())
    elif args.sample is not None:
        raise SystemExit("需要 --sample limit|day|expire|idem|round|work")
    elif args.dump:
        ledger = Ledger(2)
        ledger.issue("r1", "p", 1, 0)
        print(ledger.dump().strip())
    elif args.state:
        with open(args.state, encoding="utf-8") as handle:
            restored = Ledger.load(handle.read())
        print("pending=%d" % restored.pending.get("p", 0))
    else:
        raise SystemExit("需要 --sample limit|day|expire|idem|round|work，或 --dump / --state")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
