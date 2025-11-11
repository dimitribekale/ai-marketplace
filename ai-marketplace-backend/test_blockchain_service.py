import pytest
import blockchain_service

def test_get_model_count(mocker):
    mock_contract = mocker.MagicMock()

    # Configure the mock: "When contract.functions.modelCount().call() is called,
    # just return the number 5, don't actually do anything."
    mock_contract.functions.modelCount.return_value.call.return_value = 5

    # Replace the real contract with a fake one
    mocker.patch('blockchain_service.contract', mock_contract)

    result = blockchain_service.get_model_count_from_chain()
    assert result == 5

    mock_contract.functions.modelCount.assert_called_once()
    mock_contract.functions.modelCount.return_value.call.assert_called_once()

