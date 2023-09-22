import matplotlib.pyplot as plt

x = [1, 2, 3, 4, 5, 6]
y = [1, 5, 3, 5, 7, 8]

plt.plot(x, y)
plt.show()

with open('/home/pi/co2.log', 'r') as f:
    co2_data = f.read().split('\n')

    print(co2_data)
