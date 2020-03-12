import logging
import threading
import time

dato = 0


def lector(lock, barrier):
    global dato
    print(threading.current_thread().name,
          'Esperando en la barrera con {} lectores más'.format(barrier.n_waiting))
    worker_id = barrier.wait()
    logging.debug('Intento acceder al dato.')
    lock.acquire()
    try:
        logging.debug('Accedio al dato.')
        logging.debug('Lee {}'.format(dato))
        time.sleep(3.0)
    finally:
        lock.release()


def escritor(cond, n):
    global dato
    logging.debug('Intento acceder a la BD.')
    lock.acquire()
    try:
        logging.debug('Accedio a la BD.')
        dato = n
        logging.debug('Modifico el dato = {}'.format(dato))
        time.sleep(3.0)
    finally:
        lock.release()
        logging.debug('Dejo de modificar el dato.')


logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )

lock = threading.Lock()
barrier = threading.Barrier(2)
escritor1 = threading.Thread(target=escritor, args=(lock, 1), name='Escritor1', )
escritor2 = threading.Thread(target=escritor, args=(lock, 2), name='Escritor2', )
lector1 = threading.Thread(target=lector, args=(lock, barrier,), name='Lector1', )
lector2 = threading.Thread(target=lector, args=(lock, barrier,), name='Lector2', )
escritor1.start()
escritor2.start()
lector1.start()
lector2.start()
