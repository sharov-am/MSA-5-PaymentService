import logging
from pyzeebe import ZeebeWorker, create_insecure_channel
import uuid
import random
import os
import asyncio

logging.basicConfig(
    level=logging.INFO, # Set the minimum level to log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s', # Define the output format
    datefmt='%Y-%m-%d %H:%M:%S' # Define the timestamp format
)


def register_tasks(worker: ZeebeWorker):
       
        @worker.task(task_type="create_payment")
        async def create_payment():
                payment_id = str( uuid.uuid4() )

                logging.info(f"create_payment called, new payment_id {payment_id}.")
                return {
                        "create_payment": True,
                        "payment_id":payment_id
                }

        @worker.task(task_type="pre_payment")
        async def pre_payment(payment_id: str):
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
        async def fraud_check(payment_id: str):
                val = random.random() 
                
                if val < 1/10:
                        logging.info(f"manual fraud check {payment_id}.")
                        return {
                                "manual_check": True,
                                "denied": False,
                                "cancel":False,
                                "payment_id":payment_id
                                }
                if val >= 1/10 and val <.2 :
                        logging.info(f"denying payment {payment_id}.")
                        return {
                                "denied": True,
                                "cancel":False,
                                "manual_check": False,
                                 "success":False,
                                "payment_id":payment_id
                                }                
                logging.info(f"successful payment {payment_id}.")
                return {
                        "denied": False,
                        "cancel":False,
                        "manual_check": False,
                        "success": True,
                        "payment_id":payment_id
                        }     

        @worker.task(task_type="refund")
        async def refund(payment_id: str):
                logging.info(f"refund payment {payment_id}.")
                return {
                        "refund": True,
                        "payment_id":payment_id
                        }   
                


        @worker.task(task_type="manual_check")
        async def manual_check(payment_id: str):
                val = random.random() 
                
                if val < 1/4:
                   import time
                   time.sleep(val*100)
                
                val = random.random() 
                if val < 1/2:
                        logging.info(f"manual fraud check failed: {payment_id}.")
                        return {
                                "denied": True,
                                "payment_id":payment_id
                                }
                return {
                        "denied": False,
                        "payment_id":payment_id
                        }               
                                
        @worker.task(task_type="counterparty_payment")
        async def counterparty_payment(payment_id: str):
                logging.info(f"counterparty payment {payment_id} successful.")
                return {
                        "payment_id":payment_id
                        }      


        @worker.task(task_type="notify")
        async def notify(**kwargs):
                logging.info(f"notify called {kwargs} .")

async def main():
   
    try:
        zeebe_address = os.getenv("ZEEBE_ADDRESS", "localhost:26500")
        logging.info(f"Worker is connecting to {zeebe_address}...")
        channel = create_insecure_channel( zeebe_address)
        worker = ZeebeWorker(channel)
        register_tasks(worker)
        await worker.work()
    except Exception as e:
        import traceback
        logging.error(traceback.format_exc()) 


if __name__ == "__main__":
    asyncio.run(main())
