def assert_is_calls(mock, calls, any_order=False):
    assert len(mock.mock_calls) == len(calls)
    mock.assert_has_calls(calls, any_order=any_order)