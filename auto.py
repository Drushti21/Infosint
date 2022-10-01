#!/usr/bin/env python3
#
# OsInT Sc4N3r - Tool for automated recon process on bug bounty
# @author: Israel C. dos Reis [@z3xddd]

from os import popen, geteuid


class OsInT_Sc4N3r(object):
    def __init__(self, domain):
        self.domain = domain

    def validate_run_as_root(self):
        if not geteuid() == 0:
            print("[-] Please run this script as root... [-]")
            exit()
        else:
            pass

    def create_folder_results(self):
        validate_folder_command = "ls -la"
        validate_var = popen(validate_folder_command).read()
        if "results" in validate_var:
            pass
        else:
            results_command = 'mkdir results'
            print('[+] Creating folder /results to archive logs... [+]')
            popen(results_command)
            print('[+] Folder created... [+]')

    def enumerate_subdomains_assetfinder(self):
        enumerate_command = 'assetfinder -subs-only '+self.domain + \
            ' > results/result_assetfinder_'+self.domain+'.txt'
        print("[*] Assetfinder execute process starting... [*]")
        print(popen(enumerate_command).read())
        print('[+] Assetfinder scan finished... See details on results/result_assetfinder_' +
              self.domain+'.txt [+]')

    def enumerate_webservers(self):
        enumerate_command = 'cat results/result_assetfinder_'+self.domain + \
            '.txt | httpx --silent > results/result_httpx_'+self.domain+'.txt'
        print("[*] Httpx execute process starting... [*]")
        print(popen(enumerate_command).read())
        print('[+] Httpx scan finished... See details on results/result_httpx_' +
              self.domain+'.txt [+]')

    def portscan(self):
        portscan_command = 'nmap -sSV -n -f -Pn T 3 --script=/usr/share/nmap/scripts/firewall-bypass.nse --allports --randomize-hosts --data-length 127 -iL results/result_assetfinder_' + \
            self.domain+'.txt > results/result_portscan_'+self.domain+'.txt'
        print("[*] Portscan execute process starting... [*]")
        popen(portscan_command).read()
        print('[+] Portscan scan finished... See details on results/result_portscan_' +
              self.domain+'.txt [+]')

    def search_json(self):
        search_json_command = 'cat results/result_assetfinder_'+self.domain + \
            '.txt |  waybackurls | grep -E "\.json(?:onp?)?$" | anew > results/result_search_json_' + \
            self.domain+'.txt'
        print("[*] Search .json files execute process starting... [*]")
        popen(search_json_command).read()
        print('[+] Scan finished... See details on results/result_search_json_' +
              self.domain+'.txt [+]')

    def search_js(self):
        search_js_command = 'cat results/result_assetfinder_'+self.domain + \
            '.txt |  waybackurls | grep -E "\.js(?:onp?)?$" | anew > results/result_search_js_' + \
            self.domain+'.txt'
        print("[*] Search .js files execute process starting... [*]")
        popen(search_js_command).read()
        print('[+] Scan finished... See details on results/result_search_js_' +
              self.domain+'.txt [+]')

    def xss_scan(self):
        xss_command = 'cat results/result_assetfinder_'+self.domain + \
            '.txt |  waybackurls | kxss > results/result_xss_scan_'+self.domain+'.txt'
        print("[*] XSS Scan execute process starting... [*]")
        popen(xss_command).read()
        print('[+] XSS Scan finished... See details on results/result_xss_scan_' +
              self.domain+'.txt [+]')

    def nuclei_attack(self):
        attack_command = 'nuclei -l results/result_httpx_'+self.domain + \
            '.txt -t ../nuclei-templates/ > results/result_nuclei_'+self.domain+'.txt'
        print("[*] Nuclei attack execute process starting... [*]")
        print(popen(attack_command).read())
        print('[+] Nuclei attack finished... See details on results/result_nuclei_' +
              self.domain+'.txt [+]')


print("""\
:'#######:::'######::'####:'##::: ##:'########:::::'######:::'######::'##::::::::'##::: ##::'#######::'########::
'##.... ##:'##... ##:. ##:: ###:: ##:... ##..:::::'##... ##:'##... ##: ##:::'##:: ###:: ##:'##.... ##: ##.... ##:
 ##:::: ##: ##:::..::: ##:: ####: ##:::: ##::::::: ##:::..:: ##:::..:: ##::: ##:: ####: ##:..::::: ##: ##:::: ##:
 ##:::: ##:. ######::: ##:: ## ## ##:::: ##:::::::. ######:: ##::::::: ##::: ##:: ## ## ##::'#######:: ########::
 ##:::: ##::..... ##:: ##:: ##. ####:::: ##::::::::..... ##: ##::::::: #########: ##. ####::...... ##: ##.. ##:::
 ##:::: ##:'##::: ##:: ##:: ##:. ###:::: ##:::::::'##::: ##: ##::: ##:...... ##:: ##:. ###:'##:::: ##: ##::. ##::
. #######::. ######::'####: ##::. ##:::: ##:::::::. ######::. ######:::::::: ##:: ##::. ##:. #######:: ##:::. ##:
:.......::::......:::....::..::::..:::::..:::::::::......::::......:::::::::..:::..::::..:::.......:::..:::::..::
                                                                   
#################################################################################################################                                                                   
                                                                   Tool for automated recon process on Bug Bounty
                                                                                 by: Israel C. dos Reis [@z3xddd]
    """)
user_domain_input = str(
    input("[+] Enter domain to scan >>  [ EX: domain.com.br ]  "))
domain_to_scan = OsInT_Sc4N3r(user_domain_input)
domain_to_scan.validate_run_as_root()
domain_to_scan.create_folder_results()
domain_to_scan.enumerate_subdomains_assetfinder()
domain_to_scan.search_json()
domain_to_scan.search_js()
domain_to_scan.xss_scan()
domain_to_scan.portscan()
domain_to_scan.enumerate_webservers()
domain_to_scan.nuclei_attack()
