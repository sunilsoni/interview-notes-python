import sys
import time
from abc import ABC, abstractmethod
from typing import Optional, Dict


# ==========================================
# 1. Interface Definition (banking_system.py)
# ==========================================
class BankingSystem(ABC):
    """
    The abstract interface for the Banking System.
    """

    @abstractmethod
    def create_account(self, timestamp: int, account_id: str) -> bool:
        pass

    @abstractmethod
    def deposit(self, timestamp: int, account_id: str, amount: int) -> Optional[int]:
        pass

    @abstractmethod
    def transfer(self, timestamp: int, source_account_id: str, target_account_id: str, amount: int) -> Optional[int]:
        pass