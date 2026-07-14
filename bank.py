def transfer_funds(from_account, to_account, amount):
    """
    Transfer amount from from_account to to_account.

    Each account is a dict: {"id": int, "balance": float, "owner": str}

    Returns a transaction dict on success.
    Raises ValueError for invalid inputs.
    """
    if amount <= 0:
        raise ValueError("Transfer amount must be positive.")
    if from_account["id"] == to_account["id"]:
        raise ValueError("Source and destination accounts must be different.")
    if from_account["balance"] < amount:
        raise ValueError("Insufficient funds in source account.")

    from_account["balance"] -= amount
    to_account["balance"] += amount

    return {"from_id": from_account["id"], "to_id": to_account["id"], "amount": amount}