# payment_views.py
import uuid
import json
import hmac
import hashlib
import urllib.request
import urllib.parse

from time import time
from datetime import datetime
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import PaymentTransaction
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from dateutil.relativedelta import relativedelta
from django.utils import timezone

"""
zalo sẽ callback tới server django để trả về kết quả thanh toán
vì django chạy localhost nên cần ngrok để public ip cho zalopay gọi
cài ngrok tại: https://ngrok.com/downloads/windows?tab=download
cài xong chạy lệnh: 
sau đó lấy ip dán vào biến ngrok bên dưới là run đc
còn khi đã deploy lên aws thì ko cần ngrok

thanh toán xong bấm verify cũng đc, ko cần cài ngrok
"""
ngrok = "https://8404-115-79-138-142.ngrok-free.app"

# Config ZaloPay
config = {
    "app_id": 2554,
    "key1": "sdngKKJmqEMzvh5QQcdD2A9XBSKUNaYn",
    "key2": "trMrHtvjo6myautxDUiAcYsVtaeQ8nhf",
    "endpoint": "https://sb-openapi.zalopay.vn/v2/create",
    "query_endpoint": "https://sb-openapi.zalopay.vn/v2/query",
    "redirect_url": ngrok + "/zp-return/",
    "callback_url": ngrok + "/api/payment/callback/"
}


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_payment(request):
    user = request.user
    # Dùng UUID ngắn gọn (8 ký tự đầu)
    trans_id = str(uuid.uuid4())[:8]
    app_trans_id = "{:%y%m%d}_{}".format(datetime.today(), trans_id)

    order = {
        "app_id": config["app_id"],
        "app_trans_id": app_trans_id,
        "app_user": str(request.user.id),
        "app_time": int(round(time() * 1000)),
        "amount": 99000,
        "item": json.dumps([]),
        "embed_data": json.dumps({}),
        "description": f"Thanh toán gói Premium - #{app_trans_id}",
        "bank_code": "",
        "callback_url": config["callback_url"],
        "redirect_url": config["redirect_url"]
    }

    # Chuỗi cần ký hash
    data = "|".join([
        str(order["app_id"]),
        order["app_trans_id"],
        order["app_user"],
        str(order["amount"]),
        str(order["app_time"]),
        order["embed_data"],
        order["item"]
    ])

    order["mac"] = hmac.new(config['key1'].encode(), data.encode(), hashlib.sha256).hexdigest()

    # Gửi request đến ZaloPay
    try:
        response = urllib.request.urlopen(
            url=config["endpoint"],
            data=urllib.parse.urlencode(order).encode()
        )
        result = json.loads(response.read())

        # ✅ Lưu vào database
        PaymentTransaction.objects.create(
            user=user,
            amount=order["amount"],
            currency='VND',
            payment_method='zalopay',
            payment_status='pending',
            transaction_type='subscription',
            invoice_id=app_trans_id,
            tax_amount=0.0
        )

        return Response({
            "status": "success",
            "order_url": result.get("order_url"),  # URL để client chuyển sang thanh toán
            "zp_trans_token": result.get("zp_trans_token"),
            "app_trans_id": app_trans_id,
        })

    except Exception as e:
        return Response({
            "status": "error",
            "message": str(e)
        }, status=500)

@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def zalopay_callback(request):
    result = {}
    try:
        cbdata = json.loads(request.body)  # callback gửi dưới dạng raw JSON
        mac = hmac.new(config['key2'].encode(), cbdata['data'].encode(), hashlib.sha256).hexdigest()

        if mac != cbdata.get('mac'):
            result['return_code'] = -1
            result['return_message'] = 'mac not equal'
        else:
            # Dữ liệu hợp lệ từ ZaloPay
            data_json = json.loads(cbdata['data'])
            app_trans_id = data_json.get('app_trans_id')
            try:
                transaction = PaymentTransaction.objects.get(invoice_id=app_trans_id)
                transaction.payment_status = 'completed'
                transaction.transaction_date = datetime.now()
                transaction.save()
                
                # Cập nhật premium_expired cho user
                user = transaction.user
                now = timezone.now()
                if user.premium_expired and user.premium_expired > now:
                    user.premium_expired += relativedelta(years=1)
                else:
                    user.premium_expired = now + relativedelta(years=1)
                user.save()

                result['return_code'] = 1
                result['return_message'] = 'success'
                print(f"✅ Updated transaction {app_trans_id} to completed.")
            except PaymentTransaction.DoesNotExist:
                result['return_code'] = 0
                result['return_message'] = 'transaction not found'
                print(f"❌ Transaction with ID {app_trans_id} not found.")
    except Exception as e:
        result['return_code'] = 0  # ZaloPay sẽ retry tối đa 3 lần
        result['return_message'] = str(e)
        print(f"⚠️ Callback processing failed: {e}")

    return Response(result)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def order_status(request):
    user = request.user
    # Lấy app_trans_id từ body request
    app_trans_id = request.data.get("app_trans_id")

    if not app_trans_id:
        return Response({"error": "Missing app_trans_id"}, status=400)

    params = {
        "app_id": config["app_id"],
        "app_trans_id": app_trans_id
    }

    # Tạo chuỗi data và mã hóa HMAC SHA256
    data = "{}|{}|{}".format(params["app_id"], params["app_trans_id"], config["key1"])
    params["mac"] = hmac.new(config['key1'].encode(), data.encode(), hashlib.sha256).hexdigest()

    try:
        # Gửi request đến ZaloPay
        response = urllib.request.urlopen(
            url=config["query_endpoint"],
            data=urllib.parse.urlencode(params).encode()
        )
        result = json.loads(response.read())
        # Kiểm tra nếu thanh toán thành công
        if result.get("return_code") == 1:
            transaction = PaymentTransaction.objects.get(invoice_id=app_trans_id)
            transaction.payment_status = 'completed'
            transaction.transaction_date = datetime.now()
            transaction.save()

            # Cập nhật premium_expired cho user
            now = timezone.now()
            if user.premium_expired and user.premium_expired > now:
                user.premium_expired += relativedelta(years=1)
            else:
                user.premium_expired = now + relativedelta(years=1)
            user.save()
        return Response(result)
    except Exception as e:
        return Response({"error": str(e)}, status=500)




