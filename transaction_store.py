from typing import List, Optional
from datetime import datetime
from transaction import Transaction

class TransactionStore:
    def __init__(self):
        self._mem = {}

    def current_balance(self, account_number: int) -> float:
        lst = self._mem.get(account_number, [])
        return lst[-1].balance_after if lst else 0.0

    def book(self, account_number: int, ttype: str, amount: float) -> Transaction:
        if ttype not in ("storten", "opnemen"):
            raise ValueError("type moet 'storten' of 'opnemen' zijn")
        signed = amount if ttype == "storten" else -abs(amount)
        new_bal = self.current_balance(account_number) + signed
        tx = Transaction(
            account_number=account_number,
            timestamp=datetime.now(),
            ttype=ttype,
            amount=signed,
            balance_after=new_bal,
        )
        self._mem.setdefault(account_number, []).append(tx)
        return tx

    def list_all(self, account_number: int) -> List[Transaction]:
        return list(self._mem.get(account_number, []))

    def list_between(self, account_number: int, start: Optional[datetime], end: Optional[datetime]) -> List[Transaction]:
        out = []
        for tx in self._mem.get(account_number, []):
            if start and tx.timestamp < start:
                continue
            if end and tx.timestamp > end:
                continue
            out.append(tx)
        return out
