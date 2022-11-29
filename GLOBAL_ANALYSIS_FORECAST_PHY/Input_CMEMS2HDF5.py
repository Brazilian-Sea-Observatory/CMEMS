import datetime, os

dirpath = os.getcwd()
download_dir = (dirpath+"/CMEMS_Download")
ConvertToHdf5_dir = (dirpath+"/ConvertToHdf5")
backup_path =  (dirpath+"/Backup")

forecast_mode = 1
refday_to_start = 0 
number_of_runs = 2

#Data de início e fim se forecast_mode = 0
start = datetime.date(2022,11,24)
end = datetime.date(2022,11,25)

#fill in your details for CMEMS login
user = ""
password = ""
lon_min = "-50.69"
lon_max = "-38.36"
lat_min = "-30.81"
lat_max = "-20.55"
start_depth = "0.494"
end_depth = "5727.9171"
output_file_name = "CMEMS"

#Tempo de espera para uma nova tentativa de download do arquivo (em segundos)
wait_time = 300
#Tempo de espera total em s para o download do arquivo (em segundos) 
wait_total_time = 1800
#Tamanho mínimo do arquivo em Bytes
min_file_size = 2000000

telegram_messages = 0
TOKEN = "YOUR TELEGRAM BOT TOKEN"
chat_id = "YOUR CHAT ID"