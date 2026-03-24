| Исходное состояние | Переходное состояние | Событие |
|---|---|---|---|
| init | create_order_state | create_order_event  |
| create_order_state | pre_payment_state | payment_event   |
| create_order_state | canceled_state  | user_cancel_event    | 
| pre_payment_state | refund_state | user_cancel_event   | 
| pre_payment_state | fraud_check_state  |  fraud_check_event   |
| fraud_check_state | counterparty_payment_state | fraud_check_success_event |
| fraud_check_state | refund_state | fraud_check_failed_event |
| fraud_check_state | refund_state | user_cancel_event |
| fraud_check_state | fraud_manual_check_state | fraud_manual_check_event |
| fraud_manual_check_state | refund_state | fraud_manual_check_failed_event |
| fraud_manual_check_state | refund_state | user_cancel_event |
| fraud_manual_check_state | counterparty_payment_state | fraud_manual_check_success_event |
| fraud_manual_check_state | counterparty_payment_state | fraud_manual_check_timeout_event |
| counterparty_payment_state | done_state | successfull_payment_event   |
| counterparty_payment_state | refund_state | failed_payment_event   | 
| refund_state |  canceled_state |  refund_event   | 