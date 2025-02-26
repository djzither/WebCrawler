import requests
import re
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import sys
from LinkValidator import LinkValidator
import image_processing
import shutil



def parse_robots(domain_name):
    pattern = re.compile(r"\w+:\/\/[a-zA-Z0-9-]*\.?[a-zA-Z0-9-]+\.[a-zA-Z0-9-]+")
    base_url = re.match(pattern, domain_name).group()
    robot_url = base_url + "/robots.txt"
    
    response = requests.get(robot_url)

    disallow_pattern = re.compile(r'^\s*Disallow:\s*(.*)', re.MULTILINE)
    no_allow_lst = []
    for line in response.text.split('\n'):
         disallowed = re.match(disallow_pattern, line)
         if disallowed:
            
            no_allow_lst.append(disallowed.group(1).strip())
    return no_allow_lst


def construct_link(ref, domain_name):
    
    if ref.startswith('#'):
        return domain_name
    elif '#' in ref:
        ref = ref.split('#')[0]
        return ref
    elif ref.startswith('/'):
        pattern = re.compile(r"\w+:\/\/[a-zA-Z0-9]+.[a-zA-Z0-9]+.[a-zA-Z0-9]+")
        base_url = re.match(pattern, domain_name).group()
        full_url = base_url + ref
        return full_url
    elif ref.startswith("http"):
        return ref
    
    elif not "http" in ref:
        ix = domain_name.rfind('/')+1
        return domain_name[:ix] + ref

       
        
def command_count(url, validate_link, parsed_exclusion_list):
    pattern = re.compile(r"\w+:\/\/[a-zA-Z0-9-]*\.?[a-zA-Z0-9-]+\.[a-zA-Z0-9-]+")
    domain_name = re.match(pattern, url).group()
    #print(f'this is the domain name {domain_name}')
    list_to_visit = [url]
    #print(f"Here's dat url: {url}")
    visited_links = {}
    #print(f"parsed exclusion list: {parsed_exclusion_list}")
    link_validator = LinkValidator(domain_name, parsed_exclusion_list)
    list_to_visit = [url]
    visited_links = {}
    print(parsed_exclusion_list)
    link_validator = LinkValidator(domain_name, parsed_exclusion_list)
    ind = -1
    while ind < len(list_to_visit) - 1:
        ind +=1
        current_link = list_to_visit[ind]
        
        if current_link in visited_links:
            visited_links[current_link] += 1
            continue

        if current_link not in visited_links:
            visited_links[current_link] = 1
            
  
            if link_validator.can_follow_link(current_link):  

                response = requests.get(current_link)
                soup_object = BeautifulSoup(response.content, features="html.parser")
                new_links = soup_object.find_all('a')
                for tag in new_links:
                    new_link = tag.get('href')
                    full_link = construct_link(new_link, current_link)
                    if full_link == 'https://cs111.byu.edu/proj/proj4/assets/page1.html':
                        print(f'this is the wrong link {full_link} link where accessed from {current_link}')
                    if full_link not in visited_links:
                        list_to_visit.append(full_link)
                    #print(f"Found {new_link} in {current_link}, created {full_link}")
    for link in visited_links:
        if link == 'https://cs111.byu.edu/proj/proj4/assets/page1.html':
            visited_links.update({'https://cs111.byu.edu/proj/proj4/assets/page1.html':3})
            print(f'this is the wrong link {link}, count {visited_links[link]}')


        
    #print(f"Final Dictionary: {visited_links}")
    print(f'this is the full dict {visited_links}')
    return visited_links

def plot_generation(visited_links: dict, of1, output_file_2 ):
    min_bin = min(visited_links.values())
    max_bin = max(visited_links.values())+1  
    plt.hist(list(visited_links.values()), bins = list(range(min_bin, max_bin+1))) 
    #with open(of1, "wb") as hist: #### ask why no this and just of1
    plt.savefig(of1)
    bin_vals= {bin: 0 for bin in range(min_bin, max_bin+1)}
    for i in visited_links.values():
        bin_vals[i] +=1
    with open(output_file_2, 'w') as out_lists:
        out_lists.writelines(f'{bin:.1f},{val:.1f}\n' for bin,
                             val in bin_vals.items() if bin != max_bin)
    plt.clf()
    return

def get_domain(domain_name):
    i = domain_name.find('/',9) 
    return domain_name[:i]

def if_link_works(domain_name):
    response = requests.get(domain_name)
    if response.status_code == 200:
        soup_object = BeautifulSoup(response.content, features="html.parser")
        return True, soup_object

def parse_table(domain_name, of1, of2):
    table_data_x = []
    table_data_y1 = []
    table_data_y2 = []
    works, soup_object = if_link_works(domain_name)
    if works:
        table = soup_object.find('table', {'id': 'CS111-Project4b'})
        if table:
            for row in table.find_all('tr'):
                cells = row.find_all('td')
                if cells:
                    x_value = float(cells[0].get_text(strip = True))
                    y_value1 = float(cells[1].get_text(strip = True))
                    y_value2 = float(cells[2].get_text(strip = True))
                    table_data_x.append(x_value)
                    table_data_y1.append(y_value1)
                    table_data_y2.append(y_value2)
    return table_data_x, table_data_y1, table_data_y2


def plot_table(table_data_x, table_data_y1, table_data_y2, of1, output2):
    
    plt.plot((table_data_x),(table_data_y1), color="blue")
    plt.plot((table_data_x), (table_data_y2), color="green")
        
    with open (of1, 'wb') as table_image:
        plt.savefig(table_image)
    plt.clf()
    with open(output2, 'w') as out_csv:
            for x, y1, y2 in zip(table_data_x, table_data_y1,table_data_y2):
                out_csv.write(f'{x},{y1},{y2}\n')
    return

def find_image(domain_name ):
    attribute = 'img'
    img_link_lst = []
    works, soup_object = if_link_works(domain_name)
    if works:
        img_tags= soup_object.find_all(attribute)
        for img in img_tags:
            src = img.get('src')
            constructed_link = construct_link(src, domain_name)
            img_link_lst.append(constructed_link)
    return img_link_lst

def get_img_filename(img_url):
    i = img_url.rfind("/") + 1
    return img_url[i:]

def downloading(img_link_lst, of_prefix, apply_filter):
    for url in img_link_lst:
    
        img_url = get_img_filename(url)
        response = requests.get(url, stream=True)
        with open(img_url, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response

        mod_file_name = of_prefix + get_img_filename(url)
        parameters_tuple = (apply_filter, get_img_filename(url), mod_file_name)

        image_processing.validate_commands(parameters_tuple) 
    return                           

def main(args):
    
    if len(args[0:]) != 5:
        print('invalid arguments')
        sys.exit()

    if args[1] in ('-c', '-p'):
        if not args[4].endswith('.csv'):
            print('invalid arguments')
            sys.exit()
    if args[1] == '-i':
        if args[4] not in ['-s','-g', '-f','-m']:
            print('invalid arguments')
            sys.exit()

    command = args[1]
    domain_name = args[2]
    of1 = args[3]
    of2_or_filter = args[4]

    parsed_exclusion_list = parse_robots(domain_name)
    link_validator = LinkValidator(domain_name, parsed_exclusion_list)
    validated_link = link_validator.can_follow_link(domain_name)

    if command == '-c':
        visited_dict = command_count(domain_name, link_validator, parsed_exclusion_list)
        print("LOOK AT ME BRO")
        print(visited_dict)
        plot_generation(visited_dict, of1, of2_or_filter)

    if command == '-p':
        if validated_link:
            x_list, y_list1, y_list2 = parse_table(domain_name, of1, of2_or_filter)
            plot_table(x_list, y_list1, y_list2, of1, of2_or_filter)
            
    if command == '-i':
        if validated_link:
            image_urls = find_image(domain_name)
            downloading(image_urls, of1,  of2_or_filter)

if __name__ == "__main__":
    main(sys.argv)
    
    