import json
import datetime
import sqlite3


class Store:
	"""Поля класса:
	__bd_cursor - курсор для работы с бд
	__our_ids - список ай ди работников.

	Дата хранится как int, но это timestamp
	"""
	def __init__(self, args):
		print(args)
		self.__our_ids = []
		self.__cache = {}
		self.__get_bd_cursor(args)
		self.__load_employee_ids()
		


	def __get_bd_cursor(self,database_path):
		con = sqlite3.connect(database_path)
		cur = con.cursor()
		self.__bd_con = con
		self.__bd_cursor = cur


	# это будет загрузка кэша из бд
	# def __load_cache(self):
	# 	for empl_id in self.__our_ids:
	# 		for row in self.__bd_cursor.execute('select delta from answers where user_id = %d' % empl_id):
	# 			print(row)
	# 		print('===')





	def __load_employee_ids(self):
		for value in self.__bd_cursor.execute('select id from employee'):
			self.__our_ids.append(value[0])

	def get_ids(self):
		return self.__our_ids


	# delete employee_id from id_list and db
	def delete_employee(self, del_id):
		if del_id in self.__our_ids:
			self.__our_ids.remove(del_id)
			self.__bd_cursor.execute('delete from employee where id = %d' % del_id)
			self.__bd_con.commit()

	# add employee_id to id_list and db
	def add_employee(self, new_id, new_name):
		if new_id not in self.__our_ids:
			self.__our_ids.append(new_id)
			print(self.__bd_cursor.execute('insert into employee(id, username) values (?, ?)' , (new_id, new_name)))
			self.__bd_con.commit()

	def add_answer(self, message_id, delta, date, chat_id, user_id):
		self.__bd_cursor.execute('insert into answers(id, delta, date, chat_id, user_id) values (?, ?, ?, ?, ?)' , (message_id, delta, date, chat_id, user_id))
		self.__bd_con.commit()


	# получать среднее время ожидания
	# времена подаются в формате datetime
	def get_average(self, t1, t2, chat_id):
		stamp_t1 = t1.timestamp()
		stamp_t2 = t2.timestamp()
		for row in self.__bd_cursor.execute('select avg(delta) from answers where (date <= ? and date >= ?) group by chat_id having chat_id = ?', ( stamp_t2, stamp_t1, chat_id)):
			return row[0]


store = Store('tracker_db.db')

print(store.get_average(datetime.datetime.today() - datetime.timedelta(days=3), datetime.datetime.today(), -1001504171709 ))




