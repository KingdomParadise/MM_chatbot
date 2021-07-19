import requests
check_avaliability_url = 'https://lifeline.cgmllc.net/api/v2/CheckAvailability'
user_confituration_url = 'https://lifeline.cgmllc.net/api/v2/UserConfiguration'
state_configuration_url = 'https://lifeline.cgmllc.net/api/v2/StateConfiguration'
start_order_url = 'https://lifeline.cgmllc.net/api/v2/StateConfiguration'

token='d3a1b634-90a7-eb11-a963-005056a96ce9'


def CheckAvailability_API(zipcode,email):
    print('-->> Calling CheckAvailability_API')
    res = requests.post(check_avaliability_url, data={'Token':token,'ZipCode':zipcode,'Email':email}).json()
    if res['Status']=='Success':
        # print(res.json())
        return res
        
    else:  
        return None




def UserConfiguration_API():
    print('-->> Calling UserConfiguration_API')
    res = requests.post(user_confituration_url,data={'Token':token}).json()
    
    if res['Status']=='Success':
            return res
    else:
        return None

def StateConfiguration_API():
    print('-->> Calling StateConfiguration_API')
    res = requests.post(state_configuration_url,data={'Token':token,'state':'GA'}).json()
    # print(res['TribalEligible'])
    if res['Status']=='Success':
        return res
    else:
        return None



def StartOrder_API():
    print('-->> Calling StartOrder_API')
    data = {
        'Token':token,
        'State':'GA',
        'AppVersion':'89.0.4389.72',
        'Platform':'WebApp',
        'SerialNumber':'www.zapier.com',
        'SaleTypeid':3
        }
    res = requests.post(start_order_url,data=data).json()
    
    if res['Status']=='Success':
        return res
    else:
        return None


def FLOWCHART3(zipcode,email):
    if CheckAvailability_API(zipcode,email):
        if UserConfiguration_API():
            if StateConfiguration_API():
                if StartOrder_API():
                    print('==>>>>  All API Layers PASSED')
                    return'send_link'
                else:
                    print('** API_1 FAILED :(')
                    return 'error_at_api4'

            else:
                print('** API_1 FAILED :(')
                return 'error_at_api3'
        else:
            print('** API_1 FAILED :(')
            return 'error_at_api2'
    else:
        print('** API_1 FAILED :(')
        return 'error_at_api1'



if __name__ == '__main__':
    email='denea1288@gmail.com'
    email='denea128822@gmail.com'
    zipcode=30314
    print(FLOWCHART3(zipcode,email))