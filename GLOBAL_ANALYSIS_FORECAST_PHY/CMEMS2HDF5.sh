#!/bin/bash

# Carregar variáveis de ambiente

. /etc/profile
. ~/.bash_profile
. ~/.bashrc

# Vai para o diretório de execução do script
cd /home/mohid/Aplica/CMEMS/GLOBAL_ANALYSIS_FORECAST_PHY/

# Testes
echo " " >> /home/mohid/Aplica/CMEMS/GLOBAL_ANALYSIS_FORECAST_PHY/CMEMS2HDF5.log
echo "-------" >> /home/mohid/Aplica/CMEMS/GLOBAL_ANALYSIS_FORECAST_PHY/CMEMS2HDF5.log
echo $LDFLAGS >> /home/mohid/Aplica/CMEMS/GLOBAL_ANALYSIS_FORECAST_PHY/CMEMS2HDF5.log

# Executa

/home/mohid/Aplica/CMEMS/GLOBAL_ANALYSIS_FORECAST_PHY/CMEMS2HDF5.py >> /home/mohid/Aplica/CMEMS/GLOBAL_ANALYSIS_FORECAST_PHY/CMEMS2HDF5.log 2>&1

# printenv > /tmp/printenv.log
