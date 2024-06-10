import os.path
import json

import sys
sys.path.insert(0, '/usr/local/lib/python3.10/site-packages')
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from googleapiclient.discovery import build

from . import lpnLogger
from .lpnLogger import LoggerModule
GLOBAL_SCOPES = ['https://www.googleapis.com/auth/contacts']
GLOBAL_CONNECTION_LIST = None

GLOBAL_CREDS=None
GLOBAL_CONTACT_TO_UPDATE=None
GLOBAL_LOGGER=None
GLOBAL_GOOGLE_SERVICE=None


def SetGoogleCredentials():

    creds = None
    global GLOBAL_CONNECTION_LIST
    global GLOBAL_CREDS
    global GLOBAL_LOGGER
    global GLOBAL_GOOGLE_SERVICE
    GLOBAL_LOGGER=LoggerModule(__name__)

    current_directory = os.path.dirname(os.path.abspath(__file__)) +'/../json/'
    credentials_json_path = os.path.join(current_directory, 'credentials.json')
    serviceAccount_json_path = os.path.join(current_directory, 'serviceAccount.key.json')
    token_json_path = os.path.join(current_directory, 'token.json')

    GLOBAL_LOGGER.logger.info("currentDir des Json:" + str(current_directory))
    if not os.path.exists(serviceAccount_json_path):
        GLOBAL_LOGGER.logger.error("Check if serviceAccount.key.json : KO")
        return(False)

    if os.path.exists(token_json_path):
        GLOBAL_LOGGER.logger.info("fichier token.json trouvé")
        creds = Credentials.from_authorized_user_file(token_json_path, GLOBAL_SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            GLOBAL_LOGGER.logger.warning("token loaded byt  Creds KO - tring to refresh")
            creds.refresh(Request())
    if not creds or not creds.valid:
        GLOBAL_LOGGER.logger.info("load creds from service_account json file")
        creds = service_account.Credentials.from_service_account_file(serviceAccount_json_path , scopes=['https://www.googleapis.com/auth/contacts'])
        creds.refresh(Request())
        access_token = creds.token

    if not creds or not creds.valid:
        GLOBAL_LOGGER.logger.error("IMPOSSIBLE TO LOAD  CREDENTIALS")
        return(false)

    with open(token_json_path, 'w') as token:
         token.write(creds.to_json())

    GLOBAL_CREDS=creds

    try:
        # recherche de contact
        GLOBAL_GOOGLE_SERVICE = build('people', 'v1', credentials=GLOBAL_CREDS, cache_discovery=False)
        # Reception de la liste des contacts
        connections_Name= GLOBAL_GOOGLE_SERVICE.people().connections().list(resourceName='people/me', personFields='names', pageSize=500).execute().get('connections', [])
    except Exception as e:
        GLOBAL_LOGGER.logger.info("Error while lookinf for contact : {e}")
        GLOBAL_LOGGER.logger.info("CREDS : " + str(GLOBAL_CREDS)) 
        return(False)
    
    GLOBAL_CONNECTION_LIST=connections_Name
    return(True)


def Recherche_main(lpn_query):
    global GLOBAL_CONNECTION_LIST
    global GLOBAL_CREDS
    global GLOBAL_CONTACT_TO_UPDATE
    global GLOBAL_LOGGER
    contact_trouve=False
    for contact in GLOBAL_CONNECTION_LIST:
        names = contact.get('names', [])
        try:
            display_name = names[0].get('displayName')+' '+names[0].get('givenName')
        except Exception as e:
            GLOBAL_LOGGER.logger.error("Contact Exception on " + str(contact) + " frrom the Google list")
        contact_indice = display_name.lower().find(lpn_query.lower())
        if contact_indice != -1:
            contact_trouve=True
            GLOBAL_CONTACT_TO_UPDATE=contact
            return(contact_trouve)
    return(contact_trouve)

def update_contact(Nouveau_nom,email_add,tel_num,mob,compagnie,Job):

    global GLOBAL_CREDS
    global GLOBAL_CONTACT_TO_UPDATE
    global GLOBAL_LOGGER
    global GLOBAL_GOOGLE_SERVICE

    try:
        contact_id = GLOBAL_CONTACT_TO_UPDATE['resourceName']
        etag_id = GLOBAL_CONTACT_TO_UPDATE['etag']
        update_Metadata = 'names,emailAddresses,phoneNumbers,organizations'
        ToBeUpdated_contact = {
            'names': [
                {
                    'givenName': Nouveau_nom,
                    'unstructuredName': Nouveau_nom
                }
            ],
            'emailAddresses': [
                {
                    'value': email_add,
                    "type": "home"
                }
            ],
            "phoneNumbers": [
                {
                    "value": mob,
                    "type": "Mobile"
                },
                {
                    "value": tel_num,
                    "type": "Work"
                }
            ],
            "organizations": [
                {
                    "name": compagnie,
                    'title':Job
                }
            ],
            "etag":etag_id
        }
        GLOBAL_GOOGLE_SERVICE.people().updateContact(resourceName=f'{contact_id}', updatePersonFields=update_Metadata, body=ToBeUpdated_contact).execute()
        GLOBAL_LOGGER.logger.info('Contact updated:'  +  Nouveau_nom)
    except Exception as err:
        GLOBAL_LOGGER.logger.error("Error while updating Google contact : " + err)



def create_contact(Nouveau_nom,email_add,tel_num,mob,compagnie,Job):
    global GLOBAL_CREDS
    global GLOBAL_LOGGER
    global GLOBAL_GOOGLE_SERVICE
    try:
        ToBeCreated_contact = {
            'names': [
                {
                    'givenName': Nouveau_nom,
                    'unstructuredName': Nouveau_nom
                }
            ],
            'emailAddresses': [
                {
                    'value': email_add,
                    "type": "home"
                }
            ],
            "phoneNumbers": [
                {
                    "value": mob,
                    "type": "Mobile"
                },
                {
                    "value": tel_num,
                    "type": "Work"
                }
            ],
            "organizations": [
                {
                    "name": compagnie,
                    'title':Job
                }
            ]
        }
        GLOBAL_LOGGER.logger.info('Contact about to be created:' +  Nouveau_nom) 
        GLOBAL_GOOGLE_SERVICE.people().createContact(body=ToBeCreated_contact).execute()
    except Exception as err:
        GLOBAL_LOGGER.logger.error("Error while creating Google contact : " + err)


class callgoogle:
    def __init__(self):
        # init variables 
        LPN_BOUL_MAIN=SetGoogleCredentials()

    def feed_Google_Contact(self,Contact_recherche,Contact_email,Contact_tel,Contact_mobile,Contact_cie,Contact_JobRole):
        global GLOBAL_LOGGER
        GLOBAL_LOGGER.logger.info("launch feed_Google_Contact : " + str(Contact_recherche))
        try:
            if Recherche_main(Contact_recherche):
                GLOBAL_LOGGER.logger.info("Contact found, lancement de update_contact") 
                update_contact(Contact_recherche,Contact_email,Contact_tel,Contact_mobile,Contact_cie,Contact_JobRole)
            else:
                GLOBAL_LOGGER.logger.info("Contact NOT found, lancement de create_contact")
                create_contact(Contact_recherche,Contact_email,Contact_tel,Contact_mobile,Contact_cie,Contact_JobRole)
            return(True) 
        except Exception as err:
            GLOBAL_LOGGER.logger.error("BIM error while feeding contact through feed_Google_Contact:" + str(err))
            return(False)
        return(True)


