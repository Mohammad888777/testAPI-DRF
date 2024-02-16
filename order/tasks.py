from celery import shared_task
import requests


@shared_task(
    name='send request to gateway',
    bind=True
)
def send_payment_request(self,order_id):
    try:
        r=requests.get(f'http://127.0.0.1:8000/order/gateway/{order_id}/')
        print(r.json())
        if r.status_code==200:
            j=r.json()
            return {
                "url":j.get("url")
            }
        return {
            "error":True
        }


        # return {
        #     "url":
        # }

    except Exception as e:
        print("EEEEEEEEEEEEEEE")
        print("EEEEEEEEEEEEEEE")
        print("EEEEEEEEEEEEEEE")
        print("EEEEEEEEEEEEEEE")
        print(e)
        print("EEEEEEEEEEEEEEE")
        print("EEEEEEEEEEEEEEE")
        print("EEEEEEEEEEEEEEE")
        print("EEEEEEEEEEEEEEE")

        self.retry(
            max_retries=5,
            countdown=5
        )