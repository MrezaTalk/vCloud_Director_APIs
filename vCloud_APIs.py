import requests
from requests.auth import HTTPBasicAuth
import re
import json

with open("config.json", "r") as f:
    config = json.load(f)
    
class vcloud():

    def __init__(self):

        self.auth_url = config['base_url_new'] + "/sessions/provider"
        self.base_url_old = config['base_url_old']
        self.base_url_new = config['base_url_new']
        self.api_version = config['api_version']
        self.username = config['username']
        self.password = config['password']

    def get_token(self):

        url = self.auth_url
        api_version = self.api_version
        basic = HTTPBasicAuth(self.username, self.password)
        x = requests.post(url, auth = basic, verify=False, 
                        headers = {"Accept" : "application/json;version=" + api_version                                    
                        }
                            )

        if x.status_code == 200:
            print (x.headers['X-VMWARE-VCLOUD-ACCESS-TOKEN'])
            self.vcloud_access_token = x.headers['X-VMWARE-VCLOUD-ACCESS-TOKEN']
            return {'result' : '0', 'message' : 'token acquired successfully'}
        
        else:
            raise Exception(x.status_code,x.text)
    
    
    
# ---- Function getOrgs  ---- 
# return a list of organizations as :
# {'name' : org['name'], 'href' : org['href'], 'id' : org_id[0]}
# you can revise org_details in any format you need
# to view the full result you can return or monitor the value stored in data

    def getOrgs(self):
    
        url = self.base_url_old + '/org'
        api_version = self.api_version
        vcloud_access_token = self.vcloud_access_token
        x = requests.get(url, verify=False, 
                        headers = {"Accept" : "application/*+json;version=" + api_version,
                                    "Authorization" : "Bearer " + vcloud_access_token                             
                        }
                            )

        if x.status_code == 200:
            data = x.json()
            org_details = list()
            for org in data['org']:
                org_id = re.findall(r".*\/org\/(.*)", org['href'])
                org_details.append({'name' : org['name'], 'href' : org['href'], 'id' : org_id[0]})
            return org_details
        
        else:
            raise Exception(x.status_code,x.text)

# ---- Function getOrgDetails  ---- 
# accepts org_id (pure) as input (returned by getOrgs Function)
# return the complete details of organization including links and vdcs
# to view the full result you can return or monitor the value stored in data

    def getOrgDetails(self, org_id):
        api_version = self.api_version
        url = self.base_url_old + '/admin/org/' + org_id
        
        
        vcloud_access_token = self.vcloud_access_token
        x = requests.get(url, verify=False, 
                        headers = {"Accept" : "application/*+json;version=" + api_version,
                                    "Authorization" : "Bearer " + vcloud_access_token                             
                        }
                            )

        if x.status_code == 200:
            data = x.json()

            return data
        else:
            raise Exception(x.status_code,x.text)

# ---- Function disableOrg  ---- 
# accepts org_admin_href as input and disables the specified organization
# you cn find the org_admin_href in result of getOrgDetails() function
# x (returned data) in case of 204 status code contains a TASK ID that you can track to see the result of action

    def disableOrg(self, org_admin_href):
        api_version = self.api_version
        url = org_admin_href + '/action/disable'
        
        
        vcloud_access_token = self.vcloud_access_token
        x = requests.post(url, verify=False, 
                        headers = {"Accept" : "application/*+json;version=" + api_version,
                                    "Authorization" : "Bearer " + vcloud_access_token                             
                        }
                            )

        if x.status_code == 204:
            data = x.text
            return {'result' : 'success', 'message' : data}
        else:
            raise Exception(x.status_code,x.text)


# ---- Function enableOrg  ---- 
# accepts org_admin_href as input and enables the specified organization
# you cn find the org_admin_href in result of getOrgDetails() function
# x (returned data) in case of 204 status code contains a TASK ID that you can track to see the result of action

    def enableOrg(self, org_admin_href):
        api_version = self.api_version
        url = org_admin_href + '/action/enable'
        
        
        vcloud_access_token = self.vcloud_access_token
        x = requests.post(url, verify=False, 
                        headers = {"Accept" : "application/*+json;version=" + api_version,
                                    "Authorization" : "Bearer " + vcloud_access_token                             
                        }
                            )

        if x.status_code == 204:
            data = x.text
            return {'result' : 'success', 'message' : data}
        else:
            raise Exception(x.status_code,x.text)

# ---- Function getOrgvDCs  ---- 
# accepts organization {href} as input (returned by getOrgDetails Function)
# you cn find the org_admin_href in result of getOrgDetails() function
# return list of vDCs in specified organization as below:
# {'name' : vdc['name'], 'href' : vdc['href'], 'id' : vdc['id']}
# you can revise vdc_list in any format you need
# to view the full result you can return or monitor the value stored in data

    def getOrgVdcs(self, org_admin_href):
        api_version = self.api_version
        url = org_admin_href
        
        
        vcloud_access_token = self.vcloud_access_token
        x = requests.get(url, verify=False, 
                        headers = {"Accept" : "application/*+json;version=" + api_version,
                                    "Authorization" : "Bearer " + vcloud_access_token                             
                        }
                            )

        if x.status_code == 200:
            data = x.json()
            vdc_list = list()
            for vdc in data['vdcs']['vdc']:
                vdc_list.append({'name' : vdc['name'], 'href' : vdc['href'], 'id' : vdc['id']})
            return vdc_list
        else:
            raise Exception(x.status_code,x.text)

# ---- Function getVdcDetails  ---- 
# accepts vdc_href as input (returnned by getOrgvDCs() function)
# return list of vApps (including standalone VMs vApps) as:
# {'name' : vapp['name'], 'href' : vapp['href'], 'id' : vapp['id']}
# you can revise vapp_list in any format you need
# to view the full result you can return or monitor the value stored in data

    def getVdcDetails(self, vdc_href):

        api_version = self.api_version
        url = vdc_href

        vcloud_access_token = self.vcloud_access_token
        x = requests.get(url, verify=False, 
                        headers = {"Accept" : "application/*+json;version=" + api_version,
                                    "Authorization" : "Bearer " + vcloud_access_token                             
                        }
                            )

        if x.status_code == 200:
            data = x.json()
            vapp_list = list()
            for vapp in data['resourceEntities']['resourceEntity']:
                if vapp['type'] == 'application/vnd.vmware.vcloud.vApp+xml':
                    vapp_list.append({'name' : vapp['name'], 'href' : vapp['href'], 'id' : vapp['id']})
            return (vapp_list)
        else:
            raise Exception(x.status_code,x.text)


# ---- Function disableVdc  ---- 
# accepts vdc_href as input (returnned by getOrgvDCs() function)
# x (returned data) in case of 204 status code contains a TASK ID that you can track to see the result of action

    def disableVdc(self, vdc_href):
        api_version = self.api_version
        url = vdc_href + '/action/disable'
        
        
        vcloud_access_token = self.vcloud_access_token
        x = requests.post(url, verify=False, 
                        headers = {"Accept" : "application/*+json;version=" + api_version,
                                    "Authorization" : "Bearer " + vcloud_access_token                             
                        }
                            )

        if x.status_code == 204:
            data = x.text
            return {'result' : 'success', 'message' : data}
        else:
            raise Exception(x.status_code,x.text)


# ---- Function enableVdc  ---- 
# accepts vdc_href as input (returnned by getOrgvDCs() function)
# x (returned data) in case of 204 status code contains a TASK ID that you can track to see the result of action

    def enableVdc(self, vdc_href):
        api_version = self.api_version
        url = vdc_href + '/action/enable'
        
        
        vcloud_access_token = self.vcloud_access_token
        x = requests.post(url, verify=False, 
                        headers = {"Accept" : "application/*+json;version=" + api_version,
                                    "Authorization" : "Bearer " + vcloud_access_token                             
                        }
                            )

        if x.status_code == 204:
            data = x.text
            return {'result' : 'success', 'message' : data}
        else:
            raise Exception(x.status_code,x.text)

# ---- Function getVappDetails  ---- 
# accepts vapp_href as input (returnned by getVdcDetails function)
# return list of VMs in specified vApp as:
# {'name' : vm['name'], 'href' : vm['href'], 'id' : vm['id'],'status' : vm['status']}
# you can revise vm_list in any format you need
# to view the full result you can return or monitor the value stored in data

    def getVappDetails(self, vapp_href):

        api_version = self.api_version
        url = vapp_href

        vcloud_access_token = self.vcloud_access_token
        x = requests.get(url, verify=False, 
                        headers = {"Accept" : "application/*+json;version=" + api_version,
                                    "Authorization" : "Bearer " + vcloud_access_token                             
                        }
                            )

        if x.status_code == 200:
            data = x.json()
            vm_list = list()
            if data['children']:
                for vm in data['children']['vm']:
                    vm_list.append({'name' : vm['name'], 'href' : vm['href'], 'id' : vm['id'],
                                    'status' : vm['status']
                    })    
            return (vm_list)
        else:
            raise Exception(x.status_code,x.text)


# ---- Function powerOff_VM  ---- 
# accepts vm_href as input (returnned by getvappDetails function)
# and power off the VM
# x (returned data) in case of 202 status code contains a TASK ID that you can track to see the result of action

    def powerOff_VM(self, vm_href):

        api_version = self.api_version
        url = vm_href + "/power/action/powerOff"

        vcloud_access_token = self.vcloud_access_token
        x = requests.post(url, verify=False, 
                            headers = {"Accept" : "application/*+json;version=" + api_version,
                                        "Authorization" : "Bearer " + vcloud_access_token                             
                        }
                        )

        if x.status_code == 202:
            return x.json()
        else:
            raise Exception(x.status_code,x.text)


# ---- Function discardSuspend_VM  ---- 
# accepts vm_href as input (returnned by getvappDetails() function)
# and power off the VM which is in suspend status
# x (returned data) in case of 202 status code contains a TASK ID that you can track to see the result of action

    def discardSuspend_VM(self, vm_href):

        api_version = self.api_version
        url = vm_href + "/action/discardSuspendState"

        vcloud_access_token = self.vcloud_access_token
        x = requests.post(url, verify=False, 
                            headers = {"Accept" : "application/*+json;version=" + api_version,
                                        "Authorization" : "Bearer " + vcloud_access_token                             
                        }
                        )

        if x.status_code == 202:
            return x.json()
        else:
            raise Exception(x.status_code,x.text)


# ---- Function delete_VM  ---- 
# accepts vm_href as input (returnned by getvappDetails() function)
# and deletes the specified VM
# x (returned data) in case of 202 status code contains a TASK ID that you can track to see the result of action

    def delete_VM(self, vm_href):

        api_version = self.api_version
        vm_id = 'bb1d2844-df11-4f67-8f52-9f7f914245ea'
        url = vm_href

        vcloud_access_token = self.vcloud_access_token
        x = requests.delete(url, verify=False, 
                        headers = {"Accept" : "application/*+json;version=" + api_version,
                                    "Authorization" : "Bearer " + vcloud_access_token                             
                        }
                            )

        if x.status_code == 202:
            print(x.json())    
        
        else:
            raise Exception(x.status_code,x.text)


# ---- Function getVdcEdge  ---- 
# accepts vdc_href as input (returnned by getOrgVdcs() function)
# returns list of EdgeGateways as:
# {'name' : edge['name'], 'href' : edge['href']}
# you can revise edge_list in any format you need
# to view the full result you can return or monitor the value stored in data
    
    def getVdcEdge(self, vdc_href):

        api_version = self.api_version
        
        url = vdc_href + "/edgeGateways"

        vcloud_access_token = self.vcloud_access_token
        x = requests.get(url, verify=False, 
                        headers = {"Accept" : "application/*+json;version=" + api_version,
                                    "Authorization" : "Bearer " + vcloud_access_token                             
                        }
                            )

        if x.status_code == 200:
            data = x.json()
            edge_list = list()
            for edge in data['record']:
                edge_list.append({'name' : edge['name'], 'href' : edge['href']})
            
            return edge_list
        else:
            raise Exception(x.status_code,x.text)


# ---- Function deleteEdge  ---- 
# accepts vdc_href as input (returnned by getVdcEdge() function)
# delets the specified edgegateway
# x (returned data) in case of 202 status code contains a TASK ID that you can track to see the result of action


    def deleteEdge(self, edge_href):

        api_version = self.api_version
        
        url = edge_href

        vcloud_access_token = self.vcloud_access_token
        x = requests.delete(url, verify=False, 
                        headers = {"Accept" : "application/*+json;version=" + api_version,
                                    "Authorization" : "Bearer " + vcloud_access_token                             
                        }
                            )

        if x.status_code == 202:
            print(x.json())    
        
        else:
            raise Exception(x.status_code,x.text)



