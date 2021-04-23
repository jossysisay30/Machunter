from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_scrapli.tasks import send_command
from nornir_scrapli.tasks import send_configs
from scrapli import Scrapli
from pprint import pprint
from nornir.core.filter import F
import ipdb
import json
import colorama
from colorama import Fore, Style

nr = InitNornir(config_file="config.yaml")
nn=nr.inventory.hosts
results = nr.run(task=send_command, command="show mac address-table")
results2 = nr.run(task=send_command, command="show interfaces status")
ver = nr.run(task=send_command, command="show version")
macinput=input('please enter the mac last 4 digit:')
try:
 for nnn in nn:
     results3=results[nnn][0].scrapli_response.textfsm_parse_output()
     results4=results2[nnn][0].scrapli_response.genie_parse_output()
     ver1=ver[nnn][0].scrapli_response.textfsm_parse_output()
     for int in results3:
          if int['destination_address'].endswith(macinput,10,14):
             w=int['destination_port']
             ww=w.split('i')
             www=ww[1]
     for x in results4['interfaces']:
          z=x.split('t')
          y=z[3]
          if y == www:
              d='GigabitEthernet{}'.format(www)
     for int in ver1:
         w=int['version']
         s=int['serial']
         u=int['uptime']
         h=int['hostname']

     for int in results3:
        if int['destination_address'].endswith(macinput,10,14) and results4['interfaces'][d]['vlan']!='trunk':
            print('The switch for Given mac is:',Fore.RED + nnn)
            #print('The hostname for Given switch is:',Fore.RED + h)
            #print('The serial for Given switch is:',Fore.RED + s[0])
            #print('The up time  Given switch is:',Fore.RED + u)
            print('The vlan for the Given mac is:',Fore.RED+ int['vlan'])
            print('The interface for the Given mac is:',Fore.RED+ int['destination_port'])
            #print('The switchport mode for the given mac is:',Fore.RED+ results4['interfaces'][d]['vlan'])
            answer=input('Do you want to change VLAN for the given mac ? Enter yes or No:')
            if answer =="yes":
               vlann=input('Enter vlan')
               x='interface {}'.format(int['destination_port'])
               commands=[x,'switchport access vlan {}'.format(vlann)]
               vlans=nr.run(task=send_configs, configs=commands)
               print('The vlan for port {} changed to vlan {}'.format(Fore.RED +int['destination_port'],(vlann)))
except NameError:
    print('the given mac is not present')
