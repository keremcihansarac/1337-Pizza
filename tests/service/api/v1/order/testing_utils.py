def check_for_id_in_response_list(response, element_id):
    assert any(element.get('id') == element_id for element in response.json())


def check_for_id_not_in_response_list(response, element_id):
    assert all(element.get('id') != element_id for element in response.json())


def check_all_orders_have_status(response, order_status):
    for element in response.json():
        assert element.get('order_status') == order_status
