import logging
import threading
import time

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )


class Dato(object):
    def __init__(self, start=''):
        self.value = start

    def cambiar(self, variable):
        self.value = variable


def lector(lock, barrier, dato):
    num_acquire = 0
    print(threading.current_thread().name,
          'Esperando en la barrera con {} hilos más'.format(barrier.n_waiting))
    worker_id = barrier.wait()
    print(threading.current_thread().name, 'Después de la barrera', worker_id)
    time.sleep(1)
    logging.debug('Intento acceder al dato.')
    have_it = lock.acquire()
    while num_acquire < 1:
        try:
            if have_it:
                logging.debug('Accedio al dato. Lee {}'.format(dato.value))
                num_acquire += 1
            else:
                logging.debug('Ocupado')
        finally:
            time.sleep(4.0)
            if have_it:
                lock.release()


def escritor(lock, var, dato):
    logging.debug('Intento acceder a la BD.')
    lock.acquire()
    try:
        logging.debug('Accedio a la BD.')
        dato.cambiar(var)
        logging.debug('Modifico el dato = {}'.format(dato.value))
        time.sleep(1.0)
    finally:
        logging.debug('Dejo de modificar el dato.')
        lock.release()


lock = threading.Lock()
dato = Dato()

NUM_THREADS = 2

barrier = threading.Barrier(NUM_THREADS)

threads_escritor = [threading.Thread(name='Escritor%s' % i, target=escritor, args=(lock, 'Hola Soy E%s' % i, dato,), )
                    for i in range(NUM_THREADS)]
threads_lector = [threading.Thread(name='Lector%s' % i, target=lector, args=(lock, barrier, dato,), )
                  for i in range(NUM_THREADS)]

for e in threads_escritor:
    print(e.name, 'Iniciando')
    time.sleep(0.5)
    e.start()

for e in threads_escritor:
    e.join()

for t in threads_lector:
    print(t.name, 'Iniciando')
    time.sleep(0.5)
    t.start()

for t in threads_lector:
    t.join()

