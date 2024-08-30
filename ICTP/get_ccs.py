from obspy import read_events
import matplotlib.pyplot as plt

cat=read_events("events_cc/*.xml")

count_1 = 0
count_2 = 0
count_3 = 0
count_4 = 0

for event in cat:
	ccs = {}
	for pick in event.picks:
		ccs[pick.waveform_id.station_code] = float(pick.comments[0].text[7:])
	max_sta = max(ccs.items(), key=lambda k: k[1])
	max_sta_list = list(max_sta)

	for ele in max_sta_list:
		if max_sta_list[0] == "JAVS":
			max_sta_list[0] = 1
		elif max_sta_list[0] == "KNDS":
			max_sta_list[0] = 2
		elif max_sta_list[0] == "SKDS":
			max_sta_list[0] = 3
		elif max_sta_list[0] == "CEY":
			max_sta_list[0] = 4
		
		if max_sta_list[0] == 1:
			if max_sta_list[1] > 0.7:
				count_1 = count_1 + 1
		if max_sta_list[0] == 2:
			if max_sta_list[1] > 0.7:
				count_2 = count_2 + 1
		if max_sta_list[0] == 3:
			if max_sta_list[1] > 0.7:
				count_3 = count_3 + 1
		if max_sta_list[0] == 4:
			if max_sta_list[1] > 0.7:
				count_4 = count_4 + 1
			

	plt.plot(max_sta_list[0], max_sta_list[1]*100, "ro")

plt.ylim(0,100)
plt.xlim(0, 5)
plt.show()

print(count_1)
print(count_2)
print(count_3)
print(count_4)


