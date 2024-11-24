import serial


def get_data_from_rangefinder():
    uart = serial.Serial(port='COM3' ,baudrate = 115200)

    if uart.is_open:
        step = 5

        st = f"$LDESP,0,0,0,0,180,{step},"
        uart.write(st.encode())

        ad = []
        x = []
        while uart.is_open:
            dirty_data = uart.readline().decode().strip()
            _, angle, dist = map(int, dirty_data.split())

            ad += [[angle, dist]]



            if angle == 180:
                for l in range(len(ad) - 1):
                    leg = (abs(ad[l][1] ** 2 - ad[l + 1][1] ** 2)) ** 0.5
                    x += [leg]
                return ad, x




#clean_data = get_data_from_rangefinder()
clean_data = ([[0, 88], [5, 92], [10, 64], [15, 44], [20, 36], [25, 30], [30, 28], [35, 25], [40, 23], [45, 21], [50, 19], [55, 18], [60, 18], [65, 17], [70, 17], [75, 17], [80, 16], [85, 16], [90, 16], [95, 17], [100, 17], [105, 17], [110, 18], [115, 19], [120, 20], [125, 20], [130, 22], [135, 25], [140, 27], [145, 31], [150, 38], [155, 50], [160, 66], [165, 83], [170, 128], [175, 116], [180, 116]], [26.832815729997478, 66.09084656743322, 46.475800154489, 25.298221281347036, 19.8997487421324, 10.770329614269007, 12.609520212918492, 9.797958971132712, 9.38083151964686, 8.94427190999916, 6.082762530298219, 0.0, 5.916079783099616, 0.0, 0.0, 5.744562646538029, 0.0, 0.0, 5.744562646538029, 0.0, 0.0, 5.916079783099616, 6.082762530298219, 6.244997998398398, 0.0, 9.16515138991168, 11.874342087037917, 10.198039027185569, 15.231546211727817, 21.97726097583591, 32.49615361854384, 43.08131845707603, 50.32891812864648, 97.44229061347029, 54.11099703387473, 0.0])

#clean_data = ([[0, 100], [10, 55], [20, 31], [30, 23], [40, 19], [50, 16], [60, 15], [70, 14], [80, 14], [90, 14], [100, 14], [110, 15], [120, 17], [130, 19], [140, 22], [150, 31], [160, 49], [170, 94], [180, 266]], [83.51646544245033, 45.43126676640219, 20.784609690826528, 12.96148139681572, 10.246950765959598, 5.5677643628300215, 5.385164807134504, 0.0, 0.0, 0.0, 5.385164807134504, 8.0, 8.48528137423857, 11.090536506409418, 21.840329667841555, 37.94733192202055, 80.21845174272562, 248.83729623993264])


z_list = list(map(lambda s: round(s[1] / 100, 4), clean_data[0]))
x_list = list(map(lambda s: round(s / 100, 4), clean_data[1]))
angle_list = tuple(map(lambda s: s[0], clean_data[0]))
print(z_list)
check_angle = False
z_angle = -1

for i in range(len(z_list) - 2):
    if (z_list[i] > z_list[i + 1] > z_list[i + 2] or z_list[i] < z_list[i + 1] < z_list[i + 2]) and not check_angle:
            z_list[i] = 1 / 100
    elif z_list[i] < z_list[i + 1] > z_list[i + 2]:
        #z_angle -= 1
        #z_list[i] += 1 / 100

        print(z_list[i])
        #x_list[i] *= -1
        z_list[i] = z_angle
        #z_list[i + 1] = -1

        x_list[i + 1] = 0


        #print(z_angle)
print(z_list)




def get_vertices(x1, x2, z1, z2):
    return (x1, 0, z1, 1), (x1, 1, z1, 1), (x2, 1, z2, 1), (x2, 0, z2, 1)


vertices = [(0, 0, z_list[0], 1), (0, 1, z_list[0], 1), (x_list[0], 1, z_list[0], 1), (x_list[0], 0, z_list[0], 1)]

for index in range(len(z_list) - 1):
    if index < len(z_list) - 2:
        vertices += get_vertices(x_list[index] + vertices[-3][0], x_list[index + 1] + vertices[-1][0], z_list[index], z_list[index + 1])


def get_clean_data():
    faces = [tuple(range(k - 4, k)) for k in range(4, len(vertices) + 4, 4)]
    return vertices, faces
