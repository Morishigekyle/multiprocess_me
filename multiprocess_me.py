from multiprocessing import Process, Queue, freeze_support
import multiprocessing
from bs4 import BeautifulSoup
import requests
import queue
import urllib.request
import os
import re

num_threads = 4
q = Queue()
done_q = Queue()
finished_domains = []
finished_urls = []

def scrapper():
    while True:
        get_url()
        url = q.get()
        if url in finished_domains:
            q.get()
        if url not in finished_domains: 
            finished_domains.append(url)
            print("Scraping " + url)
            done_q.put(url)
            html = get_html(url)
            if html is None:
                continue
            scrape_html(html)
        if q.empty() == True:
            menu()
            
def get_url():
    if os.path.isfile("domain_names.txt"):
        with open("domain_names.txt", "r") as dm:
            for url in dm:
                q.put(url)
            dm.close()
    else:
        print("No domains added")
        menu()
        
def get_html(url):
    try:
        html = urllib.request.urlopen(url)
        return (html)
    except urllib.error.URLError as e:
        return None

def scrape_html(html):
    all_urls = [] 
    the_anchors = []
    bs = BeautifulSoup(html, features="lxml") 
    html.geturl()
    with open("Logs.txt", "a+") as logs:          
        for links in bs.findAll("a"):
            all_urls.append(str(links.get("href")))
        for anchor in all_urls:
            reg = re.match("^/", anchor)
            if reg:
                rem_slash = anchor[1:]
                the_anchors.append(rem_slash)
        for url in the_anchors:
            if url in finished_urls:
                continue
            if url.count(".com") == 1:
                continue
            else:
                finished_urls.append(url)
                logs.write(html.geturl() + url + "\n")
                q.put(html.geturl() + url)
                done_q.put(html.geturl() + url)
        logs.close()
        
def menu():    
    choose = "0"
    while choose == "0":
        print("\nChoose an option\n")
        print("1. Add a domain name")
        print("2. View added domain names")
        print("3. Start processing queue")
        print("4. Stop processing queue")
        print("5. Display Logs")
        print("6. Exit")        
        choose = input("\nChoose 1-5: ")

        if choose == "6":
            print("Exiting...")
            exit()

        elif choose == "5":
            print("\nOpening Logs...\n")
            with open("Logs.txt", "r")as logs:
                for lines in logs:
                    print(lines.split())

        elif choose == "4":
            print("3")

        elif choose == "3":
            print("\nStarting processing queue with added domain names\n")
            for i in range(num_threads):
                mp = Process(target = scrapper())
                mp.start()

        elif choose == "2":
            if os.path.isfile("domain_names.txt"):
                print("\nAdded Domain Names\n")
                with open("domain_names.txt", "r") as names:
                    for lines in names:
                        print(lines.split())
            else:
                print("\nNo domain names added\n")
                menu()
                
        elif choose == "1":
            with open("domain_names.txt", "a") as dm:   
                domain_name = input("\nDomain name: ")
                print("\nYou've added " + domain_name + ".")
                if domain_name.endswith("/"):
                    dm.write(domain_name + "\n")
                else:
                    dm.write(domain_name + "/\n")
                dm.close()
                menu()
        else:
            print("Invalid option. Exiting...")
            exit()
        
if __name__ == "__main__":   
    menu()