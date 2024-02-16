from django.shortcuts import render
import logging
from django.urls import reverse
from django.shortcuts import render
from azbankgateways import bankfactories, models as bank_models, default_settings as settings
from azbankgateways.exceptions import AZBankGatewaysException
from django.http import JsonResponse
from .models import Order,Payment,OrderProduct
from django.shortcuts import get_object_or_404
from django.db import transaction


import logging

from django.http import HttpResponse, Http404
from django.urls import reverse

from azbankgateways import bankfactories, models as bank_models, default_settings as settings


def go_to_gateway_view(request,order_id):
    o=get_object_or_404(Order,id=order_id,
                        payment__isnull=True,
                        status="New",
                        is_ordered=False
                        )
    

    amount = int(o.total_after_use_copon)
    # تنظیم شماره موبایل کاربر از هر جایی که مد نظر است
    user_mobile_number = '+989112221234'  # اختیاری

    factory = bankfactories.BankFactory()
    try:
        bank = factory.auto_create() # or factory.create(bank_models.BankType.BMI) or set identifier
        bank.set_request(request)
        bank.set_amount(amount)
        # یو آر ال بازگشت به نرم افزار برای ادامه فرآیند
        bank.set_client_callback_url(reverse('callback-gateway',kwargs={"order_id":o.id}))
        bank.set_mobile_number(user_mobile_number)  # اختیاری
    
    
        bank_record = bank.ready()
        data=bank.safe_get_gateway_payment_url()
        
        return JsonResponse({
            "data":data
        })
    
    except AZBankGatewaysException as e:
        # logging.critical(e)
        # return render(request, 'redirect_to_bank.html')
        return JsonResponse({
            "error":True,
            
        })










def callback_gateway_view(request,order_id):
    o=get_object_or_404(Order,id=order_id,
                        payment__isnull=True,
                        status="New",
                        is_ordered=False
                        )
    
    tracking_code = request.GET.get(settings.TRACKING_CODE_QUERY_PARAM, None)
    if not tracking_code:
        logging.debug("این لینک معتبر نیست.")
        raise Http404

    try:
        bank_record = bank_models.Bank.objects.get(tracking_code=tracking_code)
    except bank_models.Bank.DoesNotExist:
        logging.debug("این لینک معتبر نیست.")
        raise Http404

    # در این قسمت باید از طریق داده هایی که در بانک رکورد وجود دارد، رکورد متناظر یا هر اقدام مقتضی دیگر را انجام دهیم
    if bank_record.is_success:
        with transaction.atomic():
            o.is_ordered=True
            o.status="Completed"
            pay=Payment.objects.create(
                user=o.user,
                tracking_code=bank_record.tracking_code,
                bank_name=bank_record.bank_type,
                amount=bank_record.amount,
                status=bank_record.status,
            )
            o.payment=pay
            o.save()

            for i in o.carts.all():
                i.is_paid=True
                if not OrderProduct.objects.filter(
                    user=o.user,
                    category=i.category
                ):
                    p=OrderProduct(
                        category=i.category,
                        order=o,
                        payment=p,
                        user=o.user,
                        quantity=i.quantity,
                        package_price=i.category.price,
                        ordered=True
                    )
                    p.save()


                i.save()
                o.save()
            o.save()

            return JsonResponse({
                "done":True
            })
        
    return JsonResponse({
        "error":True,
        "msg":"پرداخت با شکست مواجه شده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت."
    })