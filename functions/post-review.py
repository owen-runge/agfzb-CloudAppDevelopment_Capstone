import sys
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

import sys
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
def main(dict):
    # my IAM_API_KEY
    authenticator = IAMAuthenticator("TWMzuQCBlAZWNi3nVXfmueobUg6i63n49xF8w7G0G7nG")
    service = CloudantV1(authenticator=authenticator)
    # my COUCH_URL
    service.set_service_url("https://apikey-v2-axihl5yl8jvktabs644nvaqelgaoj686nssgc6c6q2:b4cfc6868bb69eff823f47ed58551c11@f7db7a2a-3352-4f21-82cb-aca6224ad74c-bluemix.cloudantnosqldb.appdomain.cloud")
    response = service.post_document(db='reviews', document=dict["review"]).get_result()
    try:
    # result_by_filter=my_database.get_query_result(selector,raw_result=True)
        result= {
        'headers': {'Content-Type':'application/json'},
        'body': {'data':response}
        }
        return result
    except:
        return {
        'statusCode': 404,
        'message': 'Something went wrong'
        }
