import os
import hashlib
from flask import Flask, request, redirect

app = Flask(__name__)

# 从环境变量获取配置
MY_PID = os.environ.get("PID")
MY_KEY = os.environ.get("KEY")

def generate_sign(params, secret_key):
    # 1. 过滤 & 排序
    sorted_keys = sorted([k for k in params if k not in ['sign', 'sign_type'] and params[k]])
    # 2. 拼接 k=v
    query_string = "&".join([f"{k}={params[k]}" for k in sorted_keys])
    # 3. 直接拼接密钥
    sign_str = query_string + secret_key
    # 4. MD5 加密
    return hashlib.md5(sign_str.encode('utf-8')).hexdigest()

# 首页
@app.route('/')
def home():
    return "<h1>Vercel 服务运行中</h1><p>请访问 <a href='/pay'>/pay</a> 测试</p>"

# 1. 发起支付
@app.route('/pay')
def pay():
    # 动态获取当前域名
    base_url = request.url_root.rstrip('/')
    # 如果是 http 强制转 https (Vercel特性)
    if base_url.startswith('http://'):
        base_url = base_url.replace('http://', 'https://')

    data = {
        'pid': MY_PID,
        'type': 'epay',
        'out_trade_no': 'VERCEL_' + os.urandom(4).hex(),
        'notify_url': f"{base_url}/notify",
        'return_url': f"{base_url}/return",
        'name': 'Vercel 稳定版测试',
        'money': '0.10',
        'sign_type': 'MD5'
    }
    
    data['sign'] = generate_sign(data, MY_KEY)
    
    api_url = "https://credit.linux.do/epay/pay/submit.php"
    form_inputs = ''.join([f'<input type="hidden" name="{k}" value="{v}">' for k, v in data.items()])
    
    return f"""
    <form id="payform" action="{api_url}" method="post">
        {form_inputs}
    </form>
    <script>document.getElementById("payform").submit();</script>
    """

# 2. 异步通知
@app.route('/notify', methods=['GET'])
def notify():
    params = request.args.to_dict()
    if not params: return "fail"
    
    if generate_sign(params, MY_KEY) == params.get('sign'):
        if params.get('trade_status') == 'TRADE_SUCCESS':
            print(f"Success: {params.get('out_trade_no')}")
            return "success"
    return "fail"

# 3. 同步跳转
@app.route('/return')
def return_page():
    return "支付成功！(Vercel Hosted)"

# 注意：Vercel 不需要 app.run()，它会自动寻找 app 对象
