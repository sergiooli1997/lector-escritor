import logging
import threading
import time

dato = 0


def lector(lock, barrier):
    global dato
    print(threading.current_thread().name,
          'Esperando en la barrera con {} lectores más'.format(barrier.n_waiting))
    worker_id = barrier.wait()
    logging.debug('Intento acceder a la BD.')
    lock.acquire()
    try:
        logging.debug('Accedio a la BD.')
        logging.debug('Lee {}'.format(dato))
        time.sleep(3.0)
    finally:
        lock.release()
        logging.debug('Dejo de usar la BD.')


def escritor(cond):
    global dato
    logging.debug('Intento acceder a la BD.')
    lock.acquire()
    try:
        logging.debug('Accedio a la BD.')
        dato = 1
        logging.debug('Modifico la BD. Dato = {}'.format(dato))
        time.sleep(3.0)
    finally:
        lock.release()
        logging.debug('Dejo de usar la BD.')


logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )

lock = threading.Lock()
barrier = threading.Barrier(2)
escritor1 = threading.Thread(target=escritor, args=(lock,), name='Escritor1', )
escritor2 = threading.Thread(target=escritor, args=(lock,), name='Escritor2', )
lector1 = threading.Thread(target=lector, args=(lock, barrier,), name='Lector1', )
lector2 = threading.Thread(target=lector, args=(lock, barrier,), name='Lector2', )
escritor1.start()
escritor2.start()
lector1.start()
lector2.start()
