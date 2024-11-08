import serial


def get_data_from_rangefinder():
    uart = serial.Serial(port='COM3' ,baudrate = 115200)

    if uart.is_open:
        step = 3

        st = f"$LDESP,0,0,0,0,180,{step},"
        uart.write(st.encode())

        ad = []
        x = []
        while uart.is_open:
            dirty_data = uart.readline().decode().strip()
            _, angle, dist = map(int, dirty_data.split())

            ad += [[angle, dist]]

            if angle == 180:
                for i in range(len(ad) - 1):
                    leg = (abs(ad[i][1] ** 2 - ad[i + 1][1] ** 2)) ** 0.5
                    x += [leg]
                return ad, x




clean_data = get_data_from_rangefinder()

#clean_data = ([[0, 100], [10, 55], [20, 31], [30, 23], [40, 19], [50, 16], [60, 15], [70, 14], [80, 14], [90, 14], [100, 14], [110, 15], [120, 17], [130, 19], [140, 22], [150, 31], [160, 49], [170, 94], [180, 266]], [83.51646544245033, 45.43126676640219, 20.784609690826528, 12.96148139681572, 10.246950765959598, 5.5677643628300215, 5.385164807134504, 0.0, 0.0, 0.0, 5.385164807134504, 8.0, 8.48528137423857, 11.090536506409418, 21.840329667841555, 37.94733192202055, 80.21845174272562, 248.83729623993264])


z_list = tuple(map(lambda s: round(s[1] / 100, 4), clean_data[0]))
x_list = tuple(map(lambda s: round(s / 100, 4), clean_data[1]))
angle_list = tuple(map(lambda s: s[0], clean_data[0]))



def get_vertices(x1, x2, z1, z2):
    return (x1, 0, z1, 1), (x1, 1, z1, 1), (x2, 1, z2, 1), (x2, 0, z2, 1)


vertices = [(0, 0, z_list[0], 1), (0, 1, z_list[0], 1), (x_list[0], 1, z_list[0], 1), (x_list[0], 0, z_list[0], 1)]

for index in range(len(z_list) - 1):
    if index < 17:
        vertices += get_vertices(x_list[index] + vertices[-3][0], x_list[index + 1] + vertices[-1][0], z_list[index], z_list[index + 1])


def get_clean_data():
    faces = [tuple(range(i - 4, i)) for i in range(4, len(vertices) + 4, 4)]
    return vertices, faces

