import logging
import threading
import time


def lector(lock):
    logging.debug('Intento acceder a la BD.')
    lock.acquire()
    try:
        logging.debug('Accedio a la BD.')
        time.sleep(3.0)
    finally:
        lock.release()
        logging.debug('Dejo de usar la BD.')


def escritor(lock):
    logging.debug('Intento acceder a la BD.')
    lock.acquire()
    try:
        logging.debug('Accedio a la BD.')
        time.sleep(3.0)
    finally:
        lock.release()
        logging.debug('Dejo de usar la BD.')


logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )

lock = threading.Lock()
lector1 = threading.Thread(target=lector, args=(lock,), name='Lector1',)
lector2 = threading.Thread(target=lector, args=(lock,), name='Lector2',)
escritor1 = threading.Thread(target=escritor, args=(lock,), name='Escritor1', )
escritor2 = threading.Thread(target=escritor, args=(lock,), name='Escritor2', )
lector1.start()
lector2.start()
escritor1.start()
escritor2.start()
