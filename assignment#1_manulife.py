from operator import itemgetter
import os, ipaddress, fnmatch    

my_root_dir = '/Users/olganoranovich'
try:
 os.chdir(my_root_dir)
except Exception as e:
    print("Wrong name of root dir: ", e)
else:
    #1) find the folder 'Engineering Test Files'
    #2) prepare list of files for processing
    #3) create new file 'Combined.csv'

    my_dirname = ''
    my_folder = 'Engineering Test Files'
    my_combined_file = 'Combined.csv'

    for dirpath, dirnames, filenames in os.walk(my_root_dir):
        for basename in dirnames:
            if fnmatch.fnmatch(basename, my_folder):
                my_dirname = os.path.join(dirpath, basename)
                for dirpath, dirnames, filenames in os.walk(my_dirname):
                    list_of_files = [os.path.join(dirpath, i) for i in filenames if 'Asia' in i or 'NA' in i]
                try:
                    combined_file = open(os.path.join(my_dirname, my_combined_file), 'w')
                    combined_file.write('Source IP,Environment\n')
                except Exception as err:
                    print(f"Can't create file <{my_combined_file}>: ", e)

    if not my_dirname:
        print(f"Folder <{my_folder}> was not uploaded.")
    else:
        #list of files for processing is created by this time as well as Combined.csv
        #now we can generate the content of Combined.csv
        
        content=[]
        for filename in list_of_files:
            with open(filename, mode="r") as file:
                for line in file.readlines()[1:]: # don't need the first line with headers
                    try:
                        source_ip, count, events_per_sec = line.strip().split(',')
                        if 'Asia' in filename:
                            content.append([ipaddress.ip_address(source_ip), "Asia Prod\n"])
                        elif 'NA' in filename:
                            content.append([ipaddress.ip_address(source_ip), "NA Prod\n"])
                    except:
                        print(f"Unexpected content in file <{filename}>: \nLine: {line}")

        #content is ready.
        #Now we will do proper sorting by ip-addresses and remove duplicates

        content.sort(key = itemgetter(0))
        content = [str(ipaddress.IPv4Address(i[0])) + ',' + i[1] for i in content]
        content = list(dict.fromkeys([''.join(i) for i in content]))
        combined_file.write(''.join(content))
        combined_file.close()



