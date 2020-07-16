import logging

from logging.handlers import TimedRotatingFileHandler

import sys
import time

#logger = logging.getLogger(__name__)

import pymysql


CREATE_TABLE_SQL= '''create table applogs(
	log_id  int,
	log_message varchar(100),
	log_level varchar(100),
	log_lev_no int,
	create_time varchar(100),
	message varchar(255),
	primary key(log_id)
)'''

def id_gen():
    count = 0
    while True:
        count+=1
        yield count

gen = id_gen()




class MyDBHandler(logging.Handler):
    def emit(self, record): #call back methods
        tm = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(record.created)))
        INSERT_QUERY = f'''insert into applogs values({next(gen)},'{record.msg}','{record.levelname}',{record.levelno},'{tm}','msg1')'''
        conn = pymysql.connect('localhost', 'root', 'root','dbemp')
        channel = conn.cursor()
        channel.execute(INSERT_QUERY)
        conn.commit()


FILE_PATH='C:\\Users\\Yogesh\\Desktop\\pylog\\app1.log' #filehandler
FILE_PATH_TM='C:\\Users\\Yogesh\\Desktop\\pylog\\newapp.log'#timerotating
#logging.basicConfig(filemode='a',filename=FILE_PATH,level=logging.WARNING,
#                    format='%(asctime)s:%(created)f:%(levelname)s:%(levelno)s:%(lineno)d:%(message)s')

logger = logging.getLogger(__name__)

level = logging.DEBUG

f_handler = logging.FileHandler(filename=FILE_PATH, encoding="utf-8", mode="a")
cl_handler = logging.StreamHandler() #console
tm_handler = TimedRotatingFileHandler(filename=FILE_PATH_TM,when="m",backupCount=10)
db_handler = MyDBHandler()

dt_fmt = "%Y-%m-%d %H:%M:%S"
out_fmt1 = "[{asctime}] [{levelname:<6}] {name}: {message}"
logger_fmt_file = logging.Formatter(out_fmt1, dt_fmt, style="{")


out_fmt = "{message}"
logger_fmt_console = logging.Formatter(out_fmt,style="{")


cl_handler.setFormatter(logger_fmt_console)

f_handler.setFormatter(logger_fmt_file)
tm_handler.setFormatter(logger_fmt_file)
db_handler.setFormatter(logger_fmt_file)

logger.addHandler(cl_handler)
logger.addHandler(f_handler)
logger.addHandler(tm_handler)
logger.addHandler(db_handler)
logger.setLevel(level)

'''
for item in range(5):
    logging.info('This is information message')
    logging.warning('This is warning message')
    logging.critical('This is critical message')
    logging.error('This is error message')
    logging.debug('This is debug message')
    time.sleep(3)

sys.exit(0)
'''

def calculations(n1,n2):
    logger.info('inside calculations method {},{}'.format(n1,n2))
    try:
        result = n1/n2
    except ArithmeticError as e:
        logger.exception('Cannot perform -- operation')
    else:
        logger.info('Ans is : {}'.format(result))

import random
cnt = 1
for item in range(100):
    try:
        num1 = random.randint(111,999)
        num2 = random.randint(0,9)
    except ValueError :
        logger.exception('Invalid Input')
        logger.info('Invalid Input')
    else:
        calculations(num1,num2)
        logger.info('Step {} Completed '.format(cnt))
    cnt+=1
    time.sleep(5)
    #choice = input('Do want to continue : ')
    #if choice.lower() in ['n','no']:
    #    logger.info('Program execution completed..!')
    #    break



'''
https://www.programiz.com/python-programming/methods/string
https://www.programiz.com/python-programming/methods/built-in
https://learnbyexample.github.io/cheatsheet/python/python-regex-cheatsheet/


Loggers -- 
		
		Configurations  - basicconfig/logging.getLogger()
		Handlers -- appenders
					FileHandler -- logs the statements inside file
					TimeRotatingFileHandler--logs the statements inside file
					SMTPHandler -- Email
					SocketHandler -- 
					StreamHandler -- Console
		Levels
							**
				DEBUG,INFO,WARNING,ERROR,CRITICAL
				10		20	30		40		50
				lOCAL	QA	uat/PROD
				
		Formatters -- ?





'''