"""
快速测试API的脚本
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_send_code(phone):
    """测试发送验证码"""
    print(f"\n1. 测试发送验证码到 {phone}")
    response = requests.post(f"{BASE_URL}/auth/send-code", json={"phone": phone})
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
    return response.json()

def test_register(phone, code, nickname="测试用户"):
    """测试注册"""
    print(f"\n2. 测试注册用户")
    data = {
        "phone": phone,
        "verification_code": code,
        "nickname": nickname
    }
    response = requests.post(f"{BASE_URL}/auth/register", json=data)
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
    return response.json()

def test_login(phone, code):
    """测试登录"""
    print(f"\n3. 测试登录")
    data = {
        "phone": phone,
        "verification_code": code
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=data)
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
    return response.json()

def test_get_me(token):
    """测试获取用户信息"""
    print(f"\n4. 测试获取当前用户信息")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
    return response.json()

def main():
    print("="*60)
    print("API测试脚本")
    print("="*60)
    
    # 测试手机号
    phone = "13900139000"
    
    try:
        # 1. 发送验证码
        code_response = test_send_code(phone)
        code = code_response.get("code")
        
        if not code:
            print("❌ 获取验证码失败")
            return
        
        # 2. 尝试注册（如果已注册会失败，这是正常的）
        try:
            register_response = test_register(phone, code, "API测试用户")
            token = register_response.get("access_token")
            if token:
                print("\n✓ 注册成功")
                # 测试获取用户信息
                test_get_me(token)
                return
        except Exception as e:
            print(f"注册失败（可能已存在）: {e}")
        
        # 3. 重新获取验证码并登录
        code_response = test_send_code(phone)
        code = code_response.get("code")
        
        login_response = test_login(phone, code)
        token = login_response.get("access_token")
        
        if token:
            print("\n✓ 登录成功")
            # 测试获取用户信息
            test_get_me(token)
        else:
            print("\n❌ 登录失败")
        
        print("\n" + "="*60)
        print("测试完成")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

