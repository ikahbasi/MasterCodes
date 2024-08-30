echo 1
echo global_station run...
python 1_global_station.py
echo 

echo 2.1
echo iiees_make_inv_and_plot run...
python 2_iiees_make_inv_and_plot.py
echo 

echo 2.2
echo irsc_make_inv_and_plot run...
python 2_irsc_make_inv_and_plot.py
echo 

echo 2.3
echo magnitude_inv_station.py run...
python 2_magnitude_inv_station.py
echo 

echo 3.1
echo iiees_triger run...
python 3_iiees_triger.py
echo 

echo 3.2
echo irsc_triger run...
python 3_irsc_triger.py
echo 

echo 4and5.1
echo global_rm_resp_plot run...
python 4and5_global_rm_resp_plot.py
echo 

echo 4and5.2
echo iiees_rm_resp run...
python 4and5_iiees_rm_resp.py
echo 

echo 4and5.3
echo irsc_rm_resp. run...
python 4and5_irsc_rm_resp.py
echo 

echo 7.1
echo ML_MS_iiees. run...
python 7_ML_MS_iiees.py
echo 

echo 7.2
echo ML_MS_irsc run...
python 7_ML_MS_irsc.py
echo 

echo 9.1
echo plot_catalog_map run...
python 9_plot_catalog_map.py
echo


