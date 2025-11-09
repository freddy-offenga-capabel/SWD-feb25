from dataclasses import dataclass
from datetime import datetime

@dataclass
class Transaction:
    account_number: int
    timestamp: datetime
    ttype: str
    amount: float
    balance_after: float

    def to_row(self):
        return [
            str(self.account_number),
            self.timestamp.isoformat(timespec="seconds"),
            self.ttype,
            f"{self.amount:.2f}",
            f"{self.balance_after:.2f}",
        ]

    @staticmethod
    def from_row(row):
        return Transaction(
            account_number=int(row[0]),
            timestamp=datetime.fromisoformat(row[1]),
            ttype=row[2],
            amount=float(row[3]),
            balance_after=float(row[4]),
        )
