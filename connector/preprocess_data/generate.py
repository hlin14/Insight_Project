import time
import csv

def read_raw_file(data, _id_start):
	_id = _id_start
	row_count = 0
	with open('MTA-Bus-Time-2014-08-01_small_csv.csv', 'r') as csvfile:
	#with open('MTA-Bus-Time-2014-08-01.csv', 'r') as csvfile:
		csvreader = csv.reader(csvfile)
		for row in csvreader:
			if row_count > 0:
				if not row[0] or not row[1] or not row[2] or not row[3] or not row[7]:
					break
				else:
					data.append("{\"transaction_id\": \"" + str(_id) + \
								"\", \"latitude\":\"" + str(row[0]) + \
								"\", \"longitude\":\"" + str(row[1]) + \
								"\", \"time_received\":\"" + str(row[2]) + \
								"\", \"vehicle_id\":\"" + str(row[3]) + \
								"\", \"inferred_route_id\":\""+ str(row[7]) + "\"}"
								)

				_id += 1
			row_count += 1
			#print (row)
        	#rows.append(row)
	return data

def generate_streaming_data(data_list):
	idx = 0
	lenth_data = len(data_list)

	while idx < lenth_data:
		with open("preprocessed-data.txt", "a") as myfile:
				myfile.write(data_list[idx] + "\n")
				#time.sleep(0.0005)
				time.sleep(0.1)
				idx += 1

def main():
	data = []
	_id_start = 8
	data_list = read_raw_file(data, _id_start)
	#print(data_list)
	generate_streaming_data(data_list)


if __name__ == "__main__":
	main()
