# f = open('alumnos.txt', 'r')
# alumnos = f.read()
# print(alumnos)
# # f.seek(0)
# f.seek(20)
# alumnos2 = f.read()
# print(alumnos2)

# alumnos = f.readlines()
# print(alumnos)
# print(alumnos[0])
# for item in alumnos:
#     print(item, end = '')

# alumnos = f.readline()
# print(alumnos)

# f = open('alumnos2.txt', 'w')
# # f.write('Hola mundo!!!')
# f.write('Nuevo hola mundo!!!')

f = open('alumnos2.txt', 'a')
f.write('\n')
f.write('Hola mundo!!!\n')
f.write('Nuevo hola mundo!!!')

f.close()
