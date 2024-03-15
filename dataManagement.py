from datetime import datetime

def parse_date(log):
   month=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
   date = log.split("/")
   return datetime.strptime(str(date[0][1:])+"/"+str(month.index(date[1]))+"/"+str(date[2][:4]), "%d/%m/%Y")

def read_log(file_path):
  with  open(file_path,"r", encoding="utf8") as file:
    log_list =[]
    iter = 0
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
      iter+=1
      log_list.append((rest[0],parse_date(rest[1]+rest[2]),request,int(rest[4]),int(edited)))
    return log_list
  
def sort_log(log_list,index):
  try:
    return sorted(log_list, key=lambda x:x[index])
  except:
    print("Invalid index! Please enter a valid")

def get_entries_by_addr(log_list,address):
  return [entry for entry in log_list if address in entry[0]]

def get_entries_by_code(log_list,status_code):
  return [entry for entry in log_list if status_code == entry[3]]

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
    return [entry for entry in log_list if 600>=entry[3]>=400]
  
def get_entires_by_extension(log_list,extn):
  return [entry for entry in log_list if extn in entry[2]]

def print_entries(log_list):
  for log in log_list:
    print(log)

if __name__ == "__main__":
  log_list = read_log("NASA")
  #Testowanie
  print(print_entries(get_entries_by_addr(log_list,"/style.css" )))
  print("\n\n")
  print(print_entries(sort_log(get_entries_by_code(log_list,404),1)))
  print("\n\n")
  print(len(get_failed_reads(log_list,False)))