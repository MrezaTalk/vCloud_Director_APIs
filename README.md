# vCloud_Director_APIs

## Instructions
### Import code and fill config.json file
import code to your project folder and enter your infrastructure information in config.json file:

- \<api_version\>: the version of API schema you are going to use, for example 36.2, you can fetch available version related to our infrastructure by calling below API:

URL: https://\<vCloud-Director-FGDN-or-IPAddress\>/api/versions

Method: Get

Authentication: Basic

 Or you can find supported API versions related to your vCloud directore version in link below:
 
 https://docs.vmware.com/en/VMware-Cloud-Director/index.html
 
- \<base_url_old\>: enter \<vCloud-Director-FGDN-or-IPAddress\>
 
- \<base_url_new\>: enter \<vCloud-Director-FGDN-or-IPAddress\>
 
- \<username\>: your username with appropriate priviledge on vCloud director in format : username@organization for example admin@system
 
- \<password\>: password of username you provided
 
 Save the config.json file and go to next step
 
 ### Create vcloud() class object
 
 vCloud_Obj = vcloud()
 
 ### Get Authentication Token
 first you need to generate an authentication token for further API calls, to generate authentication Token call the get_token() method of vcloud class for the object you created in last step as below:
 
  vCloud_Obj.get_token()
 
 new generated token will be stored in class object as:
 
 self.vcloud_access_token
 
 since it's been stored in your class object you do not need to pass it as parameter to other APIs, if token is expired you can call vCloud_Obj.get_token() again to generate new one.
 token will be expired after specific amount of time that you can find the accurate time from vcloud director documentation.
 you can check the expiration time before calling an API and generate new one if it's expired or even you can ignore the expiration time and generate new token every time you want to call an API.
 
 ### Call vCloud Director APIs
 below you can find the list of implemented APIs as methods in code, fill free to add extra API call methods in vcloud class.
 
 - get_token()
 
 get authentication token and store in class object as  self.vcloud_access_token

 - getOrgs()
 
 fetch list of organizations exists in vCloud Director - extra info is available in code
 
 - getOrgDetails()
 
 fetch details of specific organization - extra info is available in code
 
 - disableOrg()
 
 disables specific organization - extra info is available in code
 
 - enableOrg()
 
 enables specific organization - extra info is available in code
 
 - getOrgVdcs()
 
 fetch list of vDCs in a specific organization - extra info is available in code
 
 - getVdcDetails()
 
 fetch details of specifi vDC - extra info is available in code
 
 - disableVdc()
 
 disables specific vDC - extra info is available in code
 
 - enableVdc()
 
 enables specific vDC - extra info is available in code
 
 - getVappDetails()
 
 fetch list of vApps / standalone VMs in specific vDC - extra info is available in code
 
 - powerOff_VM()
 
 Powers off specific VM in vApp / standalone VM - extra info is available in code
 
 - discardSuspend_VM()
 
 powers off / discard suspend state of specific VM in vApp / standalone VM - extra info is available in code
 
 - getVdcEdge()
 
 fetch list of EdgeGateways associated with specific vDC - extra info is available in code
 
 - deleteEdge()
 
 deletes / removes specific EdgeGateway - extra info is available in code
 
 
 

