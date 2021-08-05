""" //////////////////////////////// *** 
	define basic constants for all sites
*** //////////////////////////////// """
beawar_constant = 62
panipat_constant = 1247.4
roorkee_constant = 999.4
jharkhand_constant = 1998.8
castamet_constant = 999.37


""" //////////////////////////////////////////////////////////////// *** 
	Non-leap year days in each month
	For leap year the days of Feb have been adjjusted in the code itself
*** //////////////////////////////////////////////////////////////// """
month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


""" /////////////////////////////////////////////////////// *** 
	define panipat_site1 and panipat_site2 constants month-wise
	 -> seasonal tilts list (leap & non-leap year)
	 -> global inclide list
	 -> multiplication constant list
*** /////////////////////////////////////////////////////// """
panipat1_global_inclide = [164.2, 178.1, 209.8, 207.9, 213.4, 184.8, 164.4, 161.6, 173.8, 194.2, 183.3, 171.5]
panipat2_global_inclide = [117.9, 140, 186.5, 203, 213.1, 186.4, 165.7, 161.5, 165, 161.9, 132.2, 117.3]
panipat1_constant_list = [0.944530409437306, 0.9529803175127, 0.954555380136122, 0.954300017174192, 0.953091560307309, 0.947753511668245, 0.939540661806116, 0.938834687371429, 0.945421487506378, 0.950208497025997, 0.965168644285554, 0.946435450279757]
panipat2_constant_list = [0.921754941158239, 0.9393848287515, 0.948137771519821, 0.952435617251985, 0.952208331023773, 0.947311474902127, 0.939029505439681, 0.937779478459364, 0.941581090707797, 0.939360736441002, 0.930310436479281, 0.920679618774834]
lp_panipat1_seasonal_tilt = [0]*12
lp_panipat2_seasonal_tilt = [0]*12
nlp_panipat1_seasonal_tilt = [0]*12
nlp_panipat2_seasonal_tilt = [0]*12


#calculate seasonal tilts for non-leap year
for i in range(12):
	nlp_panipat1_seasonal_tilt[i] = ((panipat1_global_inclide[i]*panipat1_constant_list[i])/month_days[i])
	nlp_panipat2_seasonal_tilt[i] = ((panipat2_global_inclide[i]*panipat2_constant_list[i])/month_days[i])


#error correction for months of April, May, June
nlp_panipat1_seasonal_tilt[3] = 6.23322506140001-0.005
nlp_panipat1_seasonal_tilt[4] = nlp_panipat1_seasonal_tilt[4]-0.31
nlp_panipat1_seasonal_tilt[5] = 5.90162280384445+0.01544443


#calculate seasonal tilts for leap year
lp_panipat1_seasonal_tilt = nlp_panipat1_seasonal_tilt
lp_panipat2_seasonal_tilt = nlp_panipat2_seasonal_tilt
lp_panipat1_seasonal_tilt[1] = (panipat1_global_inclide[1]*panipat1_constant_list[1])/29
lp_panipat2_seasonal_tilt[1] = (panipat2_global_inclide[1]*panipat2_constant_list[1])/29


""" //////////////////////////////////////////// *** 
	define constants for Beawar site month-wise
	 -> seasonal tilts
*** //////////////////////////////////////////// """
b_beawar_seasonal_tilt = [5.55969262291147, 6.37028281140042, 6.307165627972, 6.74832287692192, 6.31875435673262, 6.68, 4.88754635479502, 4.54857603854664, 5.08638962577947, 5.91604603230079, 5.28697120607801, 5.47857152158707]



""" //////////////////////////////////////////// *** 
	define constants for Roorkee site month wise
	 -> seasonal tilts list
	 -> global inclide list
	 -> multiplication constant list
*** //////////////////////////////////////////// """
roorkee_global_inclide = [163.9, 179.2, 213.2, 201.4, 210.3, 182.1, 157.7, 159.8, 154.1, 206.8, 200.5, 185.6]
roorkee_constant_list = [0.944395938091124, 0.953324713401739, 0.955421528486887, 0.953051798460278, 0.952698901631499, 0.947261197993877, 0.937324869114803, 0.93845701311761, 0.938736592192122, 0.953461313791492, 0.954948746043538, 0.950556500465678]
nlp_roorkee_seasonal_tilt = [0]*12
lp_roorkee_seasonal_tilt = [0]*12

for i in range(12):
	nlp_roorkee_seasonal_tilt[i] = ((roorkee_global_inclide[i]*roorkee_constant_list[i])/month_days[i])

nlp_roorkee_seasonal_tilt[3] = 5.85394388888889
nlp_roorkee_seasonal_tilt[4] = nlp_roorkee_seasonal_tilt[4] - 0.075
nlp_roorkee_seasonal_tilt[5] = 6.09094888888889 - 0.36

lp_roorkee_seasonal_tilt = nlp_roorkee_seasonal_tilt
lp_roorkee_seasonal_tilt[1] = (roorkee_global_inclide[1]*roorkee_constant_list[1])/29


""" //////////////////////////////////////////// *** 
	define constants for Jharkhand site month wise
	 -> seasonal tilts list
	 -> global inclide list
	 -> multiplication constant list
*** //////////////////////////////////////////// """
jharkhand_seasonal_inclide = [178.4, 178.9, 199.5, 196.1, 206.6, 162.5, 138.2, 139.7, 141.8, 163.7, 175.3, 187.3]
jharkhand_constant_list = [0.947579317979094, 0.951919311027177, 0.951144680217931, 0.951027938381949, 0.951741209093958, 0.941209819176676, 0.928920938728215, 0.929843421973975, 0.933312340425954, 0.940681159048405, 0.947492377629911, 0.950074901876732]
nlp_jharkhand_seasonal_tilt = [0]*12
lp_jharkhand_seasonal_tilt = [0]*12

for i in range(12):
	nlp_jharkhand_seasonal_tilt[i] = ((jharkhand_seasonal_inclide[i]*jharkhand_constant_list[i])/month_days[i])

nlp_jharkhand_seasonal_tilt[4] = 5.89235449729202+0.04
nlp_jharkhand_seasonal_tilt[5] = 4.70571811653336+0.0205

lp_jharkhand_seasonal_tilt = nlp_jharkhand_seasonal_tilt
lp_jharkhand_seasonal_tilt[1] = (jharkhand_seasonal_inclide[1]*jharkhand_constant_list[1])/29


""" //////////////////////////////////////////// *** 
	define constants for Castamet site month wise
	 -> seasonal tilts list
	 -> global inclide list
	 -> multiplication constant list
*** //////////////////////////////////////////// """
castamet_global_inclide = [142.1, 159, 197.7, 209.4, 218.8, 188.4, 168, 159.2, 174.8, 173.8, 136.2, 136.1]
castamet_constant_list = [0.988927347522672, 0.992909399757744, 0.993488062490747, 0.994861378142273, 0.994822772991885, 0.994217824725635, 0.99215753947913, 0.991787606021159, 0.991609222534777, 0.991348933037635, 0.987935230884706, 0.983498304458082]
nlp_castamet_5deg_fix_tilt = [0]*12
lp_castamet_5deg_fix_tilt = [0]*12

for i in range(12):
	nlp_castamet_5deg_fix_tilt[i] = ((castamet_global_inclide[i]*castamet_constant_list[i])/month_days[i])


#Error correction code for Castamet Site
nlp_castamet_5deg_fix_tilt[3] = 6.8158
nlp_castamet_5deg_fix_tilt[4] = nlp_castamet_5deg_fix_tilt[4] - 0.04
nlp_castamet_5deg_fix_tilt[5] = nlp_castamet_5deg_fix_tilt[5] - 0.044

lp_castamet_5deg_fix_tilt = nlp_castamet_5deg_fix_tilt
lp_castamet_5deg_fix_tilt[1] = (castamet_global_inclide[1]*castamet_constant_list[1])/29