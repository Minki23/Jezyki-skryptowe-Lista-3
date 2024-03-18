from datetime import datetime

def parse_date(time):
   months=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
   date = time.split("/")
   return datetime.strptime(str(date[0][1:])+"/"+str(months.index(date[1])+1)+"/"+str(date[2]), "%d/%m/%Y:%H:%M:%S")

def read_log(file_path):
  with open(file_path,"r", encoding="utf8") as file:
    log_list =[]
    for entry in file:
      contents = entry.split('"')
      request = contents[1]
      if contents[2][1].isnumeric():
        rest = str(contents[0]) + str(contents[2:])
      else:
        i=3
        while not contents[i-1][1].isnumeric():
          request+=contents[i-1]
          i+=1
        rest = str(contents[0]) + str(contents[i-1:])
      rest = list(filter(lambda elem: elem != '-', rest.split(" ")))
      edited = '0' if rest[5][0:-4] == '-' else rest[5][0:-4]
      log_list.append((rest[0],parse_date(rest[1]),request,int(rest[4]),int(edited)))
    return log_list
  
def sort_log(log_list,sort_index):
  try:
    return sorted(log_list, key=lambda x:x[sort_index])
  except:
    print("Invalid index! Please enter a valid")

def get_entries_by_addr(log_list,address):
  return [entry for entry in log_list if address in entry[0]]

def get_entries_by_code(log_list,status_code):
  return [entry for entry in log_list if entry["code"] == status_code]

def get_failed_reads(log_list, split:bool):
  if split:
    log400=[]
    log500=[]
    for log in log_list:
      if log[3]>=400:
        if log[3]>=500:
          log500.append(log)
        else:
          log400.append(log)
    return (log400,log500)
  else:
    return [entry for entry in log_list if 600>entry[3]>=400]
  
def get_entires_by_extension(log_list,extn):
  return [entry for entry in log_list if extn in entry[2]]

def print_entries(log_list):
  for log in log_list:
    print(log)

def entry_to_dict(log):
  dict = {
    "ip" : log[0],
    "time" : log[1],
    "method" : log[2],
    "code" : log[3],
    "size_in_bytes" : log[4]
  }
  return dict

def log_to_dict(log_list):
  log_dict= {}
  for log in log_list:
    ip = log[0] 
    if ip in log_dict:
      log_dict[ip].append(entry_to_dict(log))
    else:
      log_dict[ip] = [entry_to_dict(log)]  
  return log_dict

def get_addrs(log_dict):
  return list(log_dict.keys())

def print_dict_entry_dates(log_dict):
  for ip, entries in log_dict.items():
    amount_of_entries = len(entries)
    amount_of_entries_with_200 = len(get_entries_by_code(entries, 200))
    sorted_entries = sort_log(entries, "time")
           
    print(f"""
    Address: {ip}
    How many requests: {amount_of_entries}
    Date of the first one: {sorted_entries[0]['time']}
    Date of the last one: {sorted_entries[-1]['time']}
    Ratio od requests with code 200 to the rest:
    Code 200: {amount_of_entries_with_200}
    Rest: {amount_of_entries - amount_of_entries_with_200}
    Ratio: {amount_of_entries_with_200/amount_of_entries}
    """)


if __name__ == "__main__":
  log_list = read_log("NASA")
  print_dict_entry_dates(log_to_dict(log_list))