import os
import signal
import time
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from pdfu import generate_pdf, merge_pdfs
from colorama import Fore, Style, init

if not os.path.exists("manuels"):
    os.makedirs("manuels")

editor_dict = {
    1: "Magnard",
    2: "Delagrave",
    3: "Belin",
    4: "la_librairie_des_ecoles"
}
init(autoreset=True)

start_time = time.time()
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument("--log-level=3")

    
driver = webdriver.Edge(
    options=options
)

os.system('cls' if os.name == 'nt' else 'clear')
print(f"""{Fore.RED}

$$\      $$\                                         $$\       $$$$$$$\                                                        
$$$\    $$$ |                                        $$ |      $$  __$$\                                                       
$$$$\  $$$$ | $$$$$$\  $$$$$$$\  $$\   $$\  $$$$$$\  $$ |      $$ |  $$ |$$\   $$\ $$$$$$\$$$$\   $$$$$$\   $$$$$$\   $$$$$$\  
$$\$$\$$ $$ | \____$$\ $$  __$$\ $$ |  $$ | \____$$\ $$ |      $$ |  $$ |$$ |  $$ |$$  _$$  _$$\ $$  __$$\ $$  __$$\ $$  __$$\ 
$$ \$$$  $$ | $$$$$$$ |$$ |  $$ |$$ |  $$ | $$$$$$$ |$$ |      $$ |  $$ |$$ |  $$ |$$ / $$ / $$ |$$ /  $$ |$$$$$$$$ |$$ |  \__|
$$ |\$  /$$ |$$  __$$ |$$ |  $$ |$$ |  $$ |$$  __$$ |$$ |      $$ |  $$ |$$ |  $$ |$$ | $$ | $$ |$$ |  $$ |$$   ____|$$ |      
$$ | \_/ $$ |\$$$$$$$ |$$ |  $$ |\$$$$$$  |\$$$$$$$ |$$ |      $$$$$$$  |\$$$$$$  |$$ | $$ | $$ |$$$$$$$  |\$$$$$$$\ $$ |      
\__|     \__| \_______|\__|  \__| \______/  \_______|\__|      \_______/  \______/ \__| \__| \__|$$  ____/  \_______|\__|      
                                                                                                 $$ |                          
                                                                                                 $$ |                          
                                                                                                 \__|                          

{Style.RESET_ALL}
{Fore.YELLOW}libmanuels.Fr edititon. {Style.RESET_ALL} To find books to dump, use this https://demo.edulib.fr/bibliotheque and check the book id in the url. Ex: 9782210783133
By {Fore.BLUE}Ulysse2211{Style.RESET_ALL}, thanks to the contribution of {Fore.RED}miickboy{Style.RESET_ALL} and {Fore.RED}noh.am{Style.RESET_ALL}
      """)

print("""
      
Editor choices:
1) Magnard
2) Delagrave
3) Belin
4) La Librairie des écoles
5) Other
      """)
editor = input("Choose a number for the name for the editor of the book you want to dump. ")
if editor == "5":
    editor = input("\nEnter the name of the editor you want to dump (case-sensitive): ")
else:
    try:
        editor = editor_dict[int(editor)]
    except (KeyError, ValueError):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(Fore.RED + "Invalid editor number. Please choose a number between 1 and 5." + Style.RESET_ALL)
        exit()

manid = input(Fore.CYAN + "\nEnter the ID of the manual: " + Style.RESET_ALL)
if not manid:
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.RED + "No ID provided. Please provide a manual id." + Style.RESET_ALL)
    exit()

utype = 1
os.system('cls' if os.name == 'nt' else 'clear')
t = f"https://storage.libmanuels.fr/{editor}/specimen/{manid}/1/OEBPS/page002.xhtml?interface=postMessage"
driver.get(t)
time.sleep(1)
try:
    pn = driver.title.split(" ")[3]
except IndexError:
    t = f"https://storage.libmanuels.fr/{editor}/manuel/{manid}/1/OEBPS/page002.xhtml?interface=postMessage"
    driver.get(t)
    utype = 2
    try:
        pn = driver.title.split(" ")[3]
    except IndexError:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(Fore.RED + "Failed to detect manual. Please check the id and the editor and try again." + Style.RESET_ALL)
        exit()

print(Fore.GREEN + f"Total {pn} pages detected." + Style.RESET_ALL)
os.makedirs(f'out_{manid}', exist_ok=True)

def signal_handler(signal, frame):
    print(Fore.RED + "\nKeyboard interrupt detected. Cleaning up temporary files..." + Style.RESET_ALL)
    driver.quit()
    pdf_files = [f'out_{manid}/{file}' for file in os.listdir(f'out_{manid}') if file.endswith('.pdf')]
    for file in pdf_files:
        os.remove(file)
        print(Fore.RED + f"Removed temporary file {file}." + Style.RESET_ALL)
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.RED + "Process interrupted." + Style.RESET_ALL)
    exit(1)

signal.signal(signal.SIGINT, signal_handler)

if utype == 1:
    url = f'https://storage.libmanuels.fr/{editor}/specimen/{manid}/1/OEBPS/cover.xhtml?interface=postMessage'
else:
    url = f'https://storage.libmanuels.fr/{editor}/manuel/{manid}/1/OEBPS/cover.xhtml?interface=postMessage'
pdf_file = generate_pdf(driver, url)
with open(f'out_{manid}/000.pdf', "wb") as outfile:
    outfile.write(pdf_file.getbuffer())
print(Fore.BLUE + "Generated PDF for cover." + Style.RESET_ALL)
for i in range(2, int(pn) + 1):
    page_number = str(i).zfill(3)
    if utype == 1:
        url = f'https://storage.libmanuels.fr/{editor}/specimen/{manid}/1/OEBPS/page{page_number}.xhtml?interface=postMessage'
    else:
        url = f'https://storage.libmanuels.fr/{editor}/manuel/{manid}/1/OEBPS/page{page_number}.xhtml?interface=postMessage'
    pdf_file = generate_pdf(driver, url)
    with open(f'out_{manid}/{i}.pdf', "wb") as outfile:
        outfile.write(pdf_file.getbuffer())
    print(Fore.BLUE + f"Generated PDF for page {i}." + Style.RESET_ALL)

driver.quit()

pdf_files = sorted(
    [f'out_{manid}/{file}' for file in os.listdir(f'out_{manid}') if file.endswith('.pdf')],
    key=lambda e: int(e.split("/")[1].split(".")[0])
)
merge_pdfs(pdf_files, f"manuels/{manid}.pdf")
print(Fore.MAGENTA + f"Created manual in manuels/{manid}.pdf" + Style.RESET_ALL)

for file in pdf_files:
    os.remove(file)
    print(Fore.RED + f"Removed temporary file {file}." + Style.RESET_ALL)
os.removedirs(f'out_{manid}')

os.system('cls' if os.name == 'nt' else 'clear')
print(Fore.GREEN + "Process completed successfully!" + Style.RESET_ALL)
print(f"It took {Fore.GREEN} %s seconds{Style.RESET_ALL}." % (time.time() - start_time))
os.startfile(f"manuels\\{manid}.pdf")