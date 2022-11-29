import re
import datetime
import time
import glob, os, shutil
import subprocess
from Input_CMEMS2HDF5 import *

#####################################################
def next_date (run):
        global next_start_date
        global next_end_date
            
        next_start_date = initial_date + datetime.timedelta(days = run)
        next_end_date = next_start_date + datetime.timedelta(days = 1)

#####################################################
def download_file():

        #Take also the previous day for running Mohid
        start_date = next_start_date - datetime.timedelta(days = 1)
        
        f_size = 0.
        
        tempoIni = time.time()

        while f_size < min_file_size:
                print("Downloading:", output_file_name,".nc for", str(next_start_date.strftime("%Y-%m-%d")))
                
                os.system("python -m motuclient --motu http://nrt.cmems-du.eu/motu-web/Motu --service-id GLOBAL_ANALYSIS_FORECAST_PHY_001_024-TDS --product-id global-analysis-forecast-phy-001-024 --longitude-min " +
                lon_min + " --longitude-max " + lon_max + " --latitude-min " + lat_min + " --latitude-max " + lat_max + " --date-min " + '"' + str(start_date.strftime("%Y-%m-%d"))+" 12:00:00"+'"'+ 
                " --date-max " + '"'+str(next_end_date.strftime("%Y-%m-%d"))+" 12:00:00"+'"'+ " --depth-min " + start_depth + " --depth-max " + end_depth + " --variable thetao --variable so --variable zos --variable uo --variable vo --out-dir " + 
                download_dir + " --out-name " + output_file_name + ".nc --user " + user + " --pwd " + password)
                
                f_size = os.path.getsize(output_file_name + '.nc')
              
                if f_size < min_file_size: 
                        print ("File not found or is too small")
                        print ("Trying again in ", wait_time, " s...")
                        ## aguarda
                        time.sleep(wait_time)
                        tempoAtual = time.time()
                        tempoTotal = tempoAtual-tempoIni

                        if tempoTotal > wait_total_time: 
                                msg = 'Failed to download files from CMEMS for ' + str(next_start_date.strftime("%Y-%m-%d")) + ' after ' + wait_total_time + ' s.'
                                print(msg)
                                telegram_msg(msg) 
                                return False
                                break #encerra o loop
                


#####################################################
#Funcao para envio de mensagem pelo Bot do Telegram
def telegram_msg(message):
        if telegram_messages == 1:
                #message = "hello from your telegram bot"
                urlbot = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
                print(requests.get(urlbot).json()) # this sends the message
#####################################################

if forecast_mode == 1:

        initial_date = datetime.datetime.combine(datetime.datetime.today(), datetime.time.min) + datetime.timedelta(days = refday_to_start)
        
else:
        interval = end - start
        number_of_runs = interval.days
        initial_date = datetime.datetime.combine(start, datetime.time.min)
        
for run in range (0,number_of_runs):    
    
        #Update dates
        next_date (run)
        
        #Download
        os.chdir(download_dir)
        
        files = glob.glob("*.nc")
        for filename in files:
                os.remove(filename)

        
        if download_file() != False:
        
                nc_files = glob.iglob(os.path.join(download_dir,"*.nc"))
                for file in nc_files:
                        shutil.copy(file, ConvertToHdf5_dir)
                
                #ConvertToHdf5
                os.chdir(ConvertToHdf5_dir)
                
                files = glob.glob("*.hdf*")
                for filename in files:
                        os.remove(filename)
                    
                output = subprocess.call([ConvertToHdf5_dir + "/ConvertToHDF5.exe"])
                
                if output == 0: 
                        output_dir = backup_path+"//"+str(next_start_date.strftime("%Y%m%d")) + "_" + str(next_end_date.strftime("%Y%m%d"))
                            
                        if not os.path.exists(output_dir):
                                os.makedirs(output_dir)
                        
                        hdf_files = glob.iglob(os.path.join(ConvertToHdf5_dir,"*.hdf*"))
                        for file in hdf_files:
                                shutil.copy(file, output_dir)
                        
                        files = glob.glob("*.nc")
                        for filename in files:
                                os.remove(filename)
                else:
                        msg = 'Failed to Convert to HDF5 files from CMEMS for ' + str(next_start_date.strftime("%Y-%m-%d")) 
                        print(msg)
                        telegram_msg(msg) 
