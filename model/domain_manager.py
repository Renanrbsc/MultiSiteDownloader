from typing import Dict, Union
from model.youtube_downloader import YoutubeDownloader
from urllib.parse import urlparse
import re
import os

class DomainManagerDownloader:
    PROJECT_NAME = "MultySiteDownloader"
    USER_FOLDER = os.environ['USERPROFILE']
 
    def __init__(self) -> None:
        self.supported_domain_variations: Dict = {"www.youtube.com": ['youtube.com', 'youtu.be']}
        self.supported_domains_functions: Dict = {"www.youtube.com": YoutubeDownloader}
        self.running = True
        self.url = None


    def menu_start(self) -> None:
        """
        Display the main menu and handle user input.
        
        Returns: None
        """
        while self.running:
            print("\n -  -------------------  - ")
            print(" - Multy Site Downloader - ")
            print(" -     by Renanrbsc      - ")
            print(" -  -------------------  - ")
            print(" - Menu:")
            print(" - 1. Process Download")
            print(" - 2. Exit")
            choice: str = input(" - Choose an option: ")
            if choice == "1":
                self.process_download()
            elif choice == "2":
                self.running = False
            else:
                print(" - Invalid choice.")


    def get_url(self) -> None:
        """
        Prompts the user to enter a URL and returns the input.
        The regular expression used in this method is used to validate the entered url,
        it matches the url with the pattern http or https, then match with the www or not,
        and then match with the rest of the url pattern .com .org .net .io.

        Returns: None
        """
        while True:
            url = input("\n - Please enter a URL: ")
            url_regex = re.compile(r"https?://(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)")
            if url_regex.match(url):
                self.url = url
                break
            else:
                print(" - Invalid URL. Please enter a valid URL.")


    def _handle_url_parse(self) -> None:
        """
        This function takes the url attribute, parse it and extract the domain name. 
        It assigns the parsed url to parsed_url attribute 
        and the domain name to user_url_domain attribute.

        Returns: None
        """
        self.parsed_url = urlparse(self.url)
        self.user_url_domain = self.parsed_url.netloc


    def _handle_different_short_domains(self, domain_name: str) -> str:
        """
        This function takes in a domain_name as input and 
        check if the user_url_domain is a short version of the domain_name. 
        If it is, it prints the short url and replaces 
        it with the full version of the domain_name in the url attribute.

        Args: domain_name: str, the domain name of the full version of the website.
        Returns: domain_name: str, the domain name of the full version of the website.
        """
        print("\n - Short Url:", self.url)
        self.url = self.parsed_url._replace(netloc=domain_name).geturl()
        print(" - Fixed Url:", self.url)
        return domain_name


    def _handle_supported_domains(self) -> Union[str, None]:    
        """
        This function iterates through the keys of the supported_domain_variations 
        attribute and checks if the user_url_domain attribute matches the current 
        domain_name or is found within the values of the current domain_name. 
        If a match is found, it returns the matching domain_name. 
        If the user_url_domain is found within the values of the current domain_name, 
        it calls the _handle_different_short_domains function and returns the result. 
        If there is no match, the function returns None.

        Returns: domain_name: the matching domain_name or None.
        """
        for domain_name in self.supported_domain_variations.keys():
            if self.user_url_domain == domain_name:
                return domain_name
            elif self.user_url_domain in self.supported_domain_variations[domain_name]:
                return self._handle_different_short_domains(domain_name)
            else:
                return None


    def _handle_website_function_download(self, domain_url: Union[str, None]) -> None:
        """
        This function takes in a domain_url (str or None) as input and checks 
        if it is a supported website. If it is a supported website, the function runs 
        the site_functions (passing in url and path_output as arguments) 
        and returns the result. If the domain_url is not a supported website, 
        the function prints a message and returns None.

        Args: 
        domain_url: str or None, the domain url of the website to be downloaded.
        Returns: None
        """
        if domain_url:
            site_functions = self.supported_domains_functions.get(domain_url)
            return site_functions(self.url, self.USER_FOLDER, self.PROJECT_NAME).run()  
        else:
            print(f"{domain_url} is not a supported website!")
            return None
        

    def process_download(self) -> None:
        """
        This function is responsible for initiating the download process. 
        It first calls the get_url() method to prompt the user for a URL, 
        then it parses the URL and extracts the domain name using the _handle_url_parse() method. 
        After that, it checks whether the domain name is supported by calling the _handle_supported_domains() method. 
        If it is supported, the function calls _handle_website_function_download() 
        method passing in the supported domain as an argument.

        Returns: None
        """
        self.get_url()
        self._handle_url_parse()
        supported_domain = self._handle_supported_domains()
        self._handle_website_function_download(supported_domain)


    def run(self):
        """
        This function is responsible for starting the program. 
        It calls the menu_start() method that runs the menu 
        and prompts the user to select an option.

        Returns: None
        """
        self.menu_start()