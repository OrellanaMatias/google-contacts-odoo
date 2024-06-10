
# -*- coding: utf-8 -*-
from odoo import http,models,fields
import json
import os
from . import lpnGoogleInteraction
from . import lpnLogger
from .lpnLogger import LoggerModule

class lpnContactModule(http.Controller):
    @http.route('/lpn_contact_module/lpn_contact_module/pushMyContactsToGoogle', auth='public')
    def index(self, **kw):
        lpnLogger_instance=LoggerModule(__name__)
        output = "<h1> Push to Google In Progress </h1> <ul>"
        lpnLogger_instance.logger.info("lpnContactModule.callHTTP.pushMyContactsToGoogle ==> Push to Google In Progress" )

        lpn_res_partner = http.request.env['res.partner'].sudo().search([])
        google_instance = lpnGoogleInteraction.callgoogle()
        for lpn_contact in lpn_res_partner:
            ToGoogle_Name = ''
            ToGoogle_Email= ''
            ToGoogle_Tel= ''
            ToGoogle_Mobile= ''
            ToGoogle_Cie= 'SOCIETE NON RENSEIGNEE'
            ToGoogle_JobRole= ''
            truecontactverified=False
            truecontactverified = 'email' in lpn_contact and lpn_contact['email'] or ('mobile' in lpn_contact and lpn_contact['mobile']) or ('phone' in lpn_contact and lpn_contact['phone'])
            if truecontactverified:
                ToGoogle_Name =       str(lpn_contact['name'])
                ToGoogle_Email=       str(lpn_contact['email'])
                if lpn_contact['phone']:
                    ToGoogle_Tel=     str(lpn_contact['phone'])
                if lpn_contact['mobile']:
                    ToGoogle_Mobile=  str(lpn_contact['mobile'])
                company = lpn_contact.parent_id  
                if company:
                    ToGoogle_Cie=     str(f"{company.name}")
                if lpn_contact['function']:
                    ToGoogle_JobRole= str(lpn_contact['function'])

                lpnLogger_instance.logger.info("Contact envoyé vers Google Contacts : " + ToGoogle_Name + ToGoogle_Email + ToGoogle_Tel + ToGoogle_Mobile + ToGoogle_Cie + ToGoogle_JobRole)
                result = google_instance.feed_Google_Contact(ToGoogle_Name,ToGoogle_Email,ToGoogle_Tel,ToGoogle_Mobile,ToGoogle_Cie,ToGoogle_JobRole)
                if not result:
                    lpnLogger_instance.logger.info(".pushMyContactsToGoogle ==> Push to Google KO KO KO KO KO KO KO KO" )
                    output += "<h2> =======> Push to Google KO KO KO KO KO </h2>"
                    return output
        output += "<h2> =======> Push to Google DONE </h2>"
        lpnLogger_instance.logger.info("lpnContactModule.callHTTP.pushMyContactsToGoogle ==> Push to Google DONE" )
        return output

class lpnContactModule(http.Controller):
    @http.route('/lpn_contact_module/lpn_contact_module/shownContactsInCSV', auth='public')
    def index(self, **kw):
        output = "<h1> MY CONTACTS in CSV </h1> <ul>"
        lpn_res_partner = http.request.env['res.partner'].sudo().search([])

        for lpn_contact in lpn_res_partner:
            truecontactverified=False            
            truecontactverified = 'email' in lpn_contact and lpn_contact['email'] or ('mobile' in lpn_contact and lpn_contact['mobile']) or ('phone' in lpn_contact and lpn_contact['phone'])
            if truecontactverified:
                output += '<li>' + str(lpn_contact['name']) + ';'  
                output +=          str(lpn_contact['email']) + ';'
                if lpn_contact['phone']:
                    output +=      str(lpn_contact['phone']) 
                output +=  ';'
                if lpn_contact['mobile']:
                    output +=      str(lpn_contact['mobile'])
                output +=  ';'
                company = lpn_contact.parent_id
                if company:
                    output +=      str(f"{company.name}") 
                else:
                    output +=      "SOCIETE NON RENSEIGNEE" 
                output +=  ';'
                if lpn_contact['function']:
                    output +=      str(lpn_contact['function']) 

                output += ';</li>'
        output += '</ul>'
        return output

class lpnContactModule(http.Controller):
    @http.route('/lpn_contact_module/lpn_contact_module', auth='public')
    def index(self, **kw):


        lpn_res_partner = http.request.env['res.partner'].sudo().search([])
        output = "<h1> liste des contacts </h1>" + '<ul>'
        output += '<li>' + 'company_name' + ';' + 'function' + ';' + 'email' + ';' + 'name' + ';' + 'country_id' + ';' + 'phone' + ';' + 'mobile' + ';' + 'street' + ';' + 'zip' + ';' + 'city' + ';' + 'state_id' + '</li>'
        for lpn_contact in lpn_res_partner:
            output += '<li>'

            company = lpn_contact.parent_id
            if company:
                output +=      str(f"{company.name}") + ';'
            else:
                output +=      "SOCIETE NON RENSEIGNEE" + ';'

   

            if 'function' in lpn_contact and lpn_contact['function']:
                output += str(lpn_contact['function']) + ';'
            else:
                output += ';'

            if 'email' in lpn_contact and lpn_contact['email']:
                output += str(lpn_contact['email']) + ';'
            else:
                output += ';'

            if 'name' in lpn_contact and lpn_contact['name']:
                output += str(lpn_contact['name']) + ';'
            else:
                output += ';'

            if 'country_id' in lpn_contact and lpn_contact['country_id']:
                output += str(lpn_contact['country_id']) + ';'
            else:
                output += ';'

            if 'phone' in lpn_contact and lpn_contact['phone']:
                output += str(lpn_contact['phone']) + ';'
            else:
                output += ';'

            if 'mobile' in lpn_contact and lpn_contact['mobile']:
                output += str(lpn_contact['mobile']) + ';'
            else:
                output += ';'

            if 'street' in lpn_contact and lpn_contact['street']:
                output += str(lpn_contact['street']) + ';'
            else:
                output += ';'

            if 'zip' in lpn_contact and lpn_contact['zip']:
                output += str(lpn_contact['zip']) + ';'
            else:
                output += ';'

            if 'city' in lpn_contact and lpn_contact['city']:
                output += str(lpn_contact['city']) + ';'
            else:
                output += ';'

            if 'state_id' in lpn_contact and lpn_contact['state_id']:
                output += str(lpn_contact['state_id'])
            else:
                output += ';'

            output += '</li>'

        output += '</ul>'
        output += "<h1> Fin de la liste des contact issu de res.partner - AU REVOIR myPersonalOdooInstance.com </h1>"
        return output

    @http.route('/lpn_contact_module/lpn_contact_module/objects', auth='public')
    def list(self, **kw):
        return http.request.render('lpn_contact_module.listing', {
            'root': '/lpn_contact_module/lpn_contact_module',
            'objects': http.request.env['lpn_contact_module.lpn_contact_module'].search([]),
        })

    @http.route('/lpn_contact_module/lpn_contact_module/objects/<model("lpn_contact_module.lpn_contact_module"):obj>', auth='public')
    def object(self, obj, **kw):
        return http.request.render('lpn_contact_module.object', {
            'object': obj
        })
