import pytest
from bank import transfer_funds


@pytest.fixture
def source_account():
    """A source account with sufficient funds."""
    return {"id": 1, "balance": 1000.0, "owner": "Alice"}


@pytest.fixture
def destination_account():
    """A destination account."""
    return {"id": 2, "balance": 500.0, "owner": "Bob"}


class TestTransferFundsValidation:
    """Tests for input validation."""
    
    def test_transfer_amount_must_be_positive(self, source_account, destination_account):
        """Transfer amount must be greater than zero."""
        with pytest.raises(ValueError):
            transfer_funds(source_account, destination_account, 0)
    
    def test_transfer_amount_cannot_be_negative(self, source_account, destination_account):
        """Transfer amount cannot be negative."""
        with pytest.raises(ValueError):
            transfer_funds(source_account, destination_account, -100)
    
    def test_insufficient_funds_raises_error(self, source_account, destination_account):
        """Source account must have sufficient funds."""
        with pytest.raises(ValueError):
            transfer_funds(source_account, destination_account, 1500)
    
    def test_cannot_transfer_to_same_account(self, source_account):
        """Source and destination accounts must be different."""
        with pytest.raises(ValueError):
            transfer_funds(source_account, source_account, 100)
    
    def test_transfer_exact_balance_allowed(self, source_account, destination_account):
        """Transfer should succeed when amount equals source balance."""
        result = transfer_funds(source_account, destination_account, 1000.0)
        assert result is not None


class TestTransferFundsBalanceUpdates:
    """Tests for balance updates."""
    
    def test_source_balance_decreases_by_amount(self, source_account, destination_account):
        """Source balance should decrease by transfer amount."""
        initial_balance = source_account["balance"]
        amount = 250.0
        transfer_funds(source_account, destination_account, amount)
        assert source_account["balance"] == initial_balance - amount
    
    def test_destination_balance_increases_by_amount(self, source_account, destination_account):
        """Destination balance should increase by transfer amount."""
        initial_balance = destination_account["balance"]
        amount = 250.0
        transfer_funds(source_account, destination_account, amount)
        assert destination_account["balance"] == initial_balance + amount
    
    def test_both_balances_updated_correctly(self, source_account, destination_account):
        """Both balances should be updated correctly in a single transfer."""
        source_initial = source_account["balance"]
        dest_initial = destination_account["balance"]
        amount = 150.0
        
        transfer_funds(source_account, destination_account, amount)
        
        assert source_account["balance"] == source_initial - amount
        assert destination_account["balance"] == dest_initial + amount


class TestTransferFundsReturnValue:
    """Tests for return value (transaction dict)."""
    
    def test_returns_transaction_dict(self, source_account, destination_account):
        """Should return a transaction dictionary."""
        result = transfer_funds(source_account, destination_account, 100)
        assert isinstance(result, dict)
    
    def test_transaction_contains_from_id(self, source_account, destination_account):
        """Transaction dict should contain from_id."""
        result = transfer_funds(source_account, destination_account, 100)
        assert "from_id" in result
        assert result["from_id"] == source_account["id"]
    
    def test_transaction_contains_to_id(self, source_account, destination_account):
        """Transaction dict should contain to_id."""
        result = transfer_funds(source_account, destination_account, 100)
        assert "to_id" in result
        assert result["to_id"]