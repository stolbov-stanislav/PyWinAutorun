"""Набор классов и функций для установки/удаления автозапуска
	любого файла в системах Windows OS."""
	
import winreg as wr
import win32api #Необходим для функции get_path()
import json
	
class AutoRun():
	"""Основной объект установки/удаления автозапуска."""
	
	def __init__(self, name, path):
		
		#Имя автозапуска в реестре.
		self.name = name
		#Абсолютный путь к файлу(сохраняется как значение в реестре).
		self.path = path
		#Флаг использования автозапуска.
		self.flag = 0
		
		#Создаёт ключ в реестре, сохраняет его в переменную.
		self.key = wr.CreateKey(wr.HKEY_CURRENT_USER,
		"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run")

	def set_autorun(self):
		"""Устанавливает автозапуск файла."""
		
		#Создаёт файл в реестре автозапуска.
		wr.SetValueEx(self.key, self.name, 0, wr.REG_SZ, self.path)
		#Устанавливает флаг.
		self.flag = 1
		
	def remove_autorun(self):
		"""Удаляет автозапуск файла."""
		
		#Удаляет автозагрузку программы из реестра.
		wr.DeleteValue(self.key, self.name)
		self.flag = 0
		
	def flag_dump(self):
		"""Записывает флаг во внешний файл. Создаёт файл,
			если отсутствует. Формат файла - .json.
			Директория - общая с autorun.py"""
		
		flag_file = 'flag_autorun.json'
		with open(flag_file, 'w') as ff:
			json.dump(self.flag, ff)
	
	def flag_load(self):
		"""Загружает значение флага из файла. Создаёт файл,
			если отсутствует."""
		
		flag_file = 'flag_autorun.json'
		try:	
			with open(flag_file) as ff:
				self.flag = json.load(ff)
		except FileNotFoundError:
			with open(flag_file, 'w') as ff:
				json.dump(self.flag, ff)

def get_path(file_name):
	"""Функция для получения полного пути к файлу для его автозапуска.
	Файл должен находиться в той же директории,
	что и модуль 'autorun.py'."""
	
	path = win32api.GetFullPathName(file_name)
	return path
