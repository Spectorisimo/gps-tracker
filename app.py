import datetime
from tracker import database
import socket
import binascii
import logging

class DatabaseRepository():
    __database = database.Database()

    def add_data(self, data: tuple):
        self.__database.cursor.execute(
            f"INSERT INTO gps_tracker_gpsdata(date,latitude,longitude,altitude,sattelites,speed) VALUES{data}")
        self.__database.connection.commit()



# Настройки логирования
logging.basicConfig(
    filename='server.log',
    filemode='a',
    format='%(asctime)s %(levelname)s: %(message)s',
    level=logging.DEBUG
)

# Порт для прослушивания
port = 1025

# Создание сокета
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Привязка сокета к порту
s.bind(('', port))

# Функция декодирования данных
def decodethis(data):
    if not data:
        return ''

    try:
        codec = int(data[16:18], 16)

        if (codec == 8):
            length = int(data[8:16], 16)
            record = int(data[19:20], 16)
            timestamp = int(data[20:36], 16)
            priority = int(data[36:38], 16)
            lon = str(int(data[38:46], 16))
            lat = str(int(data[46:54], 16))
            alt = int(data[54:58], 16)
            angle = int(data[58:62], 16)
            sats = int(data[62:64], 16)
            speed = int(data[64:68], 16)

            db = DatabaseRepository()
            timestamp = str(timestamp)[:10]
            date = datetime.datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            latitude = lat[:2] + '.' + lat[2:]
            longitude = lon[:2] + '.' + lon[2:]
            data = (date, latitude, longitude, alt, sats, speed)
            db.add_data(data)

            logging.info("Received data: Record: %s, Timestamp: %s, Lat,Lon: %s, %s, Altitude: %s, Sats: %s, Speed: %s",
                record, timestamp, lat, lon, alt, sats, speed)

            return "0000" + str(record).zfill(4)
    except Exception as e:
        logging.error("Error decoding data: %s", str(e))

    return ''

# Функция запуска сервера
def start():
    # Начало прослушивания порта
    s.listen()

    logging.info("Server is listening on port %s", port)

    while True:
        # Ожидание нового соединения
        conn, addr = s.accept()

        logging.info("New connection from %s", addr)

        connected = True

        while connected:
            # Ожидание данных от устройства
            imei = conn.recv(1024)

            try:
                message = '\x01'

                message = message.encode('utf-8')

                conn.send(message)
            except Exception as e:
                logging.error("Error sending reply: %s", str(e))
                break

            try:
                # Получение данных от устройства
                data = conn.recv(1024)

                # Преобразование данных в hex-строку
                received = binascii.hexlify(data)

                # Декодирование данных и отправка ответа обратно на устройство
                record = decodethis(received).encode('utf-8')
                conn.send(record)
            except Exception as e:
                logging.error("Error receiving/sending data: %s", str(e))
                break

        conn.close()

    s.close()




if __name__ == '__main__':
    logging.info("Starting server...")
    start()


