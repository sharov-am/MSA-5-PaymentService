import logging
from pyzeebe import ZeebeWorker, create_insecure_channel
import uuid
import random


logging.basicConfig(
    level=logging.INFO, # Set the minimum level to log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s', # Define the output format
    datefmt='%Y-%m-%d %H:%M:%S' # Define the timestamp format
)

# 1. Получаем строку из переменной окружения (с дефолтом на всякий случай)
zeebe_address = os.getenv("ZEEBE_ADDRESS", "localhost:26500")

# 2. Парсим строку: разделяем по двоеточию
# host будет "zeebe", port_str будет "26500"
host, port_str = zeebe_address.split(":")
port = int(port_str) # Конвертируем порт в число

# 3. Используем при создании канала
channel = create_insecure_channel(hostname=host, port=port)

#channel = create_insecure_channel(hostname="zeebe", port=26500)
worker = ZeebeWorker(channel)


@worker.task(task_type="create_payment")
def create_payment():
    payment_id = str( uuid.uuid4() )
  
    logging.info(f"create_payment called, new payment_id {payment_id}.")
    return {
            "create_payment": True,
            "payment_id":payment_id
           }

@worker.task(task_type="pre_payment")
def pre_payment(payment_id: str):
    if random.random() < 1/10:
             logging.info(f"canceling payment {payment_id}.")
             return {
                     "cancel": True,
                     "success":False,
                     "payment_id":payment_id
                    }
    return {
              "success":True,
              "payment_id":payment_id
           }                
                     

@worker.task(task_type="fraud_check")
def fraud_check(payment_id: str):
    val = random.random() 
    
    if val < 1/20:
             logging.info(f"manual fraud check {payment_id}.")
             return {
                     "fraud_check": 'manual',
                     "payment_id":payment_id
                    }
    if val >= 1/20 and val <.2 :
             logging.info(f"denying payment {payment_id}.")
             return {
                     "fraud_check_result": False,
                     "payment_id":payment_id
                    }                
    logging.info(f"successful payment {payment_id}.")
    return {
              "fraud_check_result": True,
              "payment_id":payment_id
            }     

@worker.task(task_type="refund")
def refund(payment_id: str):
    logging.info(f"refund payment {payment_id}.")
    return {
              "refund": True,
              "payment_id":payment_id
            }   
    


@worker.task(task_type="manual_check")
def manual_check(payment_id: str):
     val = random.random() 
    
     if val < 1/20:
             logging.info(f"manual fraud check {payment_id}.")
             return {
                     "fraud_manual_check": False,
                     "payment_id":payment_id
                    }
     return {
              "fraud_manual_check": True,
              "payment_id":payment_id
            }               
                    
@worker.task(task_type="counterparty_payment")
def counterparty_payment(payment_id: str):
     logging.info(f"counterparty payment {payment_id} successful.")
     return {
              "payment_id":payment_id
            }      


# Запускаем всё одним махом
worker.work()
