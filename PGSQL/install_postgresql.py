import paramiko  # для работы с SSH
import psycopg2  # для работы с PostgreSQL
import sys  # для работы с командной строкой 
import time  # для выставления задержки по времени

def install_postgresql(hostname):  # функция для подключения по ssh и установки/настройки PostgreSQL
    try:
        username = "your_username"  # Имя пользователя для подключения по SSH
        password = "your_password"  # Пароль для подключения по SSH
        
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, username=username, password=password)  # подключение по SSH
        
        # Команды для установки PostgreSQL
        commands = [
            "sudo apt update", 
            "sudo apt -y install postgresql postgresql-contrib"  # Установка PostgreSQL и дополнительных пакетов
        ]
        for command in commands:  # выполнение и вывод результата команд по установке PostgreSQL
            stdin, stdout, stderr = client.exec_command(command)
            print(stdout.read().decode())  # Вывод результата 
            print(stderr.read().decode())  # Вывод ошибок 
        
        # Команды для настройки PostgreSQL для внешних подключений
        config_commands = [
            "sudo sed -i \"s/#listen_addresses = 'localhost'/listen_addresses = '*'/\" /etc/postgresql/12/main/postgresql.conf",  # Разрешение внешних подключений
            "echo \"host all all 0.0.0.0/0 md5\" | sudo tee -a /etc/postgresql/12/main/pg_hba.conf",  # Настройка аутентификации для внешних подключений
            "sudo systemctl restart postgresql"  # Перезапуск PostgreSQL
        ]
        for command in config_commands:  # выполнение и вывод результата команд по настройке PostgreSQL
            stdin, stdout, stderr = client.exec_command(command)
            print(stdout.read().decode())  # Вывод результата команды
            print(stderr.read().decode())  # Вывод ошибок команды

        # Проверка работы PostgreSQL
        time.sleep(5)  # ожидание 5 секунд
        connection = psycopg2.connect(
            dbname="postgres",  # Имя базы данных
            user="postgres",  # Пользователь базы данных
            password="postgres",  # Пароль пользователя базы данных
            host=hostname,  # Хост базы данных
            port=5432  # Порт базы данных
        )
        cursor = connection.cursor()
        cursor.execute("SELECT 1")  # Выполнение тестового запроса
        result = cursor.fetchone()
        if result and result[0] == 1:  # Проверка результата запроса 
            print("PostgreSQL установлен и работает корректно")
        else:
            print("Ошибка")
        
        cursor.close()
        connection.close()
        
    except Exception as e:  # обработка ошибок 
        print(f"Ошибка: {e}")
    finally:
        client.close()  # отключение SSH-соединения

if __name__ == "__main__":
    if len(sys.argv) != 2:  # Проверяем количество аргументов командной строки, где sys.argv - список аргументов переданных списку
        print("Запуск: python install_postgresql.py <hostname>")
        sys.exit(1)
    
    hostname = sys.argv[1]
    
    install_postgresql(hostname)  # вызов основной функции
