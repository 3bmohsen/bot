# api/booking.py
from http.server import BaseHTTPRequestHandler
import requests
import json
from datetime import datetime

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            result = self.check_availability()
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response_data = {
                'timestamp': datetime.now().isoformat(),
                'status': result['status'],
                'message': result['message'],
                'data': result.get('data', {}),
                'appointment_available': result.get('appointment_available', False)
            }
            
            self.wfile.write(json.dumps(response_data, ensure_ascii=False).encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            error_response = {
                'timestamp': datetime.now().isoformat(),
                'status': 'error',
                'message': f'خطأ: {str(e)}',
                'appointment_available': False
            }
            
            self.wfile.write(json.dumps(error_response, ensure_ascii=False).encode('utf-8'))

    def check_availability(self):
        url = "https://tms.tabadul.sa/api/appointment/tas/v2/zone/schedule/land"
        params = {
            "departure": "KFC",
            "arrival": "31",
            "type": "TRANSIT",
            "economicOperator": ""
        }

        headers = {
            "Accept": "application/json",
            "Accept-Language": "ar",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "application/json; charset=utf-8",
            "Origin": "https://oga.fasah.sa",
            "Pragma": "no-cache",
            "Referer": "https://oga.fasah.sa/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "Sec-GPC": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
            "sec-ch-ua": '"Not;A=Brand";v="99", "Brave";v="139", "Chromium";v="139"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "token": "Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJiYWx1ZHMwMDE2MCIsIkdST1VQUyAiOiJUQVNHRU4sVFJOUFJULFRSTlBSVEYsVFJOUFJURkksVFJBTlNQT1JUX0FHRU5UIiwiR1JPVVBTIjoiVEFTR0VOLFRSTlBSVCxUUk5QUlRGLFRSTlBSVEZJLFRSQU5TUE9SVF9BR0VOVCIsIklTX1NTTyAiOmZhbHNlLCJTU09fVE9LRU4gIjoiIiwiSVNfU1NPIjpmYWxzZSwiU1NPX1RPS0VOIjoiIiwiQ0xJRU5UX05BTUUiOiJGQVNBSCIsImlzcyI6IkZBU0FIIiwiYXVkIjoiRkFTQUggQXBwbGljYXRpb24iLCJleHAiOjE3NTY5NjgwOTF9.0UFfGxMqll1bHErASb9GOZw3RgZWfZd69h5Y-hlOuuvdXAu-t-IoNcMUxaLyourL2ehThH7-biVNp862gFiqJQ"
        }

        try:
            response = requests.get(url, headers=headers, params=params, timeout=20)
            
            if response.status_code == 200:
                data = response.json()
                
                # فحص إذا كان مفيش مواعيد متاحة
                if (not data.get("success") 
                    and data.get("errors") 
                    and len(data["errors"]) > 0
                    and data["errors"][0].get("message") == "لا يوجد مواعيد متاحة"):
                    
                    return {
                        'status': 'no_appointments',
                        'message': 'لا يوجد مواعيد متاحة حالياً',
                        'appointment_available': False,
                        'data': data
                    }
                
                # إذا كان الرد مختلف = يعني في مواعيد متاحة
                else:
                    return {
                        'status': 'appointments_found',
                        'message': '🎉 تم العثور على مواعيد متاحة!',
                        'appointment_available': True,
                        'data': data
                    }
            
            else:
                return {
                    'status': 'api_error',
                    'message': f'خطأ في الاتصال: {response.status_code}',
                    'appointment_available': False,
                    'data': {'error': response.text}
                }
                
        except requests.exceptions.Timeout:
            return {
                'status': 'timeout',
                'message': 'انتهت مهلة الاتصال',
                'appointment_available': False
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'خطأ غير متوقع: {str(e)}',
                'appointment_available': False
            }
