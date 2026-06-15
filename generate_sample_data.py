from simulator import generate_bin_data, save_data

for i in range(50):
    save_data(generate_bin_data())

print("50 records generated")