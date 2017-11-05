import threading
import queue
import time
from stockmarket import StockMarket
from user import User


th_stop = threading.Event()
threads = []
q = queue.LifoQueue(5)


def trading_strategy(num, q, lev,t_number):
    a = User(num, q, lev)
    #from numpy import random as rand
    #from secrets import choice   choice(direction)
    #direction = [-1, 1]
    for i in range(1, t_number+1):  ## transaction number
        direct = User.random_direction(None, 0.50)
        a.make_transaction(direct)


def wait_for_users_job_inserted():
    for i in threads:
        print("waiting for thread {} to finish".format(i))
        i.join()


def users_jobs(number_of_users,leverage,t_number):
    create_users(number_of_users, trading_strategy, leverage,t_number)


def create_users(number_of_users, trading_strategy, leverage,t_number):
    global threads
    for i in range(1,number_of_users+1):
        th = threading.Thread(target=trading_strategy, args=(i, q, leverage,t_number)) ## num, q , leverage
        threads.append(th)


def run_stock_market():
    market = StockMarket(q)
    th = threading.Thread(target=market.listen_for_orders, args=(th_stop, ))
    th.start()


def start_user_threads():
    for i in threads:
        if not i.is_alive():
            i.start()


def wait_for_jobs_to_be_handled():
    global th_stop
    while q.empty():
        th_stop.set()
        break


def job(users,leverage, t_number):
    start = time.time()
    
    run_stock_market()
    users_jobs(users,leverage,t_number)
    start_user_threads()
    wait_for_users_job_inserted()
    wait_for_jobs_to_be_handled()

    print('It took {0:0.1f} seconds'.format(time.time() - start))
    

if __name__ == "__main__":
    
    from multiprocessing import Pool
    
    #job(50,1,50)
    #print('Job done')
    job(500,5,500)
    
    #with Pool(4) as p:
        #p.starmap(job, [(50,1,50),(500,1,500),(50,1000,50),(500,100,500)])

