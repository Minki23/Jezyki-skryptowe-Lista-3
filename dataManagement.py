from datetime import datetime

def parse_date(log):
   month=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
   date = log.split("/")
   return datetime.strptime(str(date[0][1:])+"/"+str(month.index(date[1]))+"/"+str(date[2][:4]), "%d/%m/%Y")

def read_log(file_path):
  with  open(file_path, 'r') as file:
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
      log_list.append((rest[0],parse_date(rest[1]+rest[2]),request,int(rest[4]),int(edited)))
    return log_list
  
def sort_log(log_list,index):
  sorted_logs = []
  try:
    sorted_logs = sorted(log_list, key=lambda x:x[index])
  except:
    print("Invalid index! Please enter a valid")
  return sorted_logs

def get_entries_by_addr(log_list,address):
  logs_with_address = [entry for entry in log_list if address in entry[0]]
  return logs_with_address

for log in get_entries_by_addr(read_log("NASA"),'csa.bu.edu'):
   print(log)