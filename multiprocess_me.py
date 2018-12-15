from multiprocessing import Process, Queue, freeze_support
import multiprocessing
from bs4 import BeautifulSoup
import requests
import queue
import urllib.request
import re

q = Queue()
num_threads = 4
finished_domains = []

def start_process():
    while True:
        get_url()
        url = q.get()
        if url in finished_domains:
            menu()
        if url not in finished_domains: 
            finished_domains.append(url)
            print("Scraping " + url)
            html = get_html(url)
            scrape_html(html)
        if q.empty() == True:
            menu()

def get_url():
    with open("domain_names.txt", "r") as dm:
        for url in dm:
            q.put(url)
        dm.close()
        
def get_html(url):
    html = urllib.request.urlopen(url)
    return (html)

def scrape_html(html):
    all_urls = [] 
    bs = BeautifulSoup(html, features="lxml")   
    with open("Logs.txt", "a") as logs:          
        for links in bs.findAll("a"):
            all_urls.append(str(links.get("href")) + "\n")
        for urls in all_urls:
            logs.write(urls)          
        logs.close()
    
        
def menu():
    
    choose = "0"
    while choose == "0":
        print("\nChoose an option\n")
        print("1. Add a domain name")
        print("2. Start processing queue")
        print("3. Stop processing queue")
        print("4. Display Logs")
        print("5. Exit")
        
        choose = input("\nChoose 1-5: ")

        if choose == "5":
            print("Exiting...")
            exit()
        elif choose == "4":
            print("4")
        elif choose == "3":
            print("3")
        elif choose == "2":
            print("Starting processing queue with added domain names\n")
            for i in range(num_threads):
                mp = multiprocessing.Process(target = start_process())
                menu = multiprocessing.Process(target = menu())
                menu.start()
                mp.start()

        elif choose == "1":
            with open("domain_names.txt", "a") as dm:   
                domain_name = input("\nDomain name: ")
                print("You've added " + domain_name + ".")
                dm.write(domain_name + "\n")
                dm.close()
                start_process()
                menu()
        else:
            print("Invalid option. Exiting...")
            exit()
        
if __name__ == "__main__":   
    menu()
