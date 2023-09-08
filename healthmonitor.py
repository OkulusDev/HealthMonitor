#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""Программа для мониторинга психического и физического здоровья.
Copyright (C) 2023  Okulus Dev
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>."""
import json
import sys
from datetime import datetime
import matplotlib.pyplot as plt


class Tracker:
	def __init__(self, filename: str):
		self.filename = filename

	def add_to_file(self, info, date, mood, stress_level, health_level, additional_info):
		try:
			with open(self.filename, 'r') as file:
				data = json.load(file)
		except FileNotFoundError:
			data = []

		data.append({f'{date}': {
					'info': info,
					'mood': mood,
					'stress_level': stress_level,
					'health_level': health_level,
					'additional_info': additional_info}})

		with open(self.filename, 'w') as file:
			json.dump(data, file, indent=4)

	def get_all_info(self):
		try:
			with open(self.filename, 'r') as file:
				data = json.load(file)
		except:
			return None
		else:
			return data


class GraphicsHealth:
	def __init__(self, mood, stress_level, health_level, info):
		self.mood = mood
		self.stress_level = stress_level
		self.health_level = health_level
		self.info = info

	def show(self):
		plt.title(f"{self.info}")
		params = ["Настроение", 'Стресс', 'Здоровье']
		levels = [self.mood, self.stress_level, self.health_level]
		plt.bar(params, levels)
		plt.xlabel("Характеристика")
		plt.ylabel("Оценка")
		plt.show()


def get_current_date():
	return datetime.now()


def add_entry(date, mood: int, stress_level: int, health_level: int, additional_info) -> list:
	if mood > 0 and mood < 6 and stress_level > 0 and stress_level < 6 and health_level > 0 and health_level < 6:
		return [True, f'Уровень настроения: {mood}\nУровень стресса: {stress_level}\nУровень физического здоровья: {health_level}\nДополнительная информация: {additional_info}',
				date, mood, stress_level, health_level, additional_info]
	else:
		return [False, 'Проверьте корректность данных', date, 0, 0, 0, None]


def get_middle_digit(numbers: list):
	list_length = len(numbers)
	count_of_all = 0

	for num in numbers:
		if str(num).isdigit():
			count_of_all += num
		else:
			raise ValueError(f'{num} is not integer')

	result = int(count_of_all / list_length)

	return result


def main():
	tracker = Tracker('health.json')
	#print(tracker.get_all_info())
	print('Health Monitor - исследуйте ваше психическое и физическое здоровье')

	if len(sys.argv) > 1:
		if sys.argv[1] == 'showall':
			data = tracker.get_all_info()
			dates = []
			moodies = []
			stresses = []
			health_levels = []

			ymd_dates = []

			dates_used = 'Состояния здоровья за '

			for i in data:
				for entry in i.items():
					date = str(entry[0]).split('.')[0].split(' ')
					
					if len(ymd_dates) > 0:
						if ymd_dates[-1] != date[0]:
							ymd_dates.append(date[0])
							dates_used += f'{date[0]}; '
					else:
						ymd_dates.append(date[0])
						dates_used += f'{date[0]}; '

					dates.append(date[1])
					moodies.append(entry[1]['mood'])
					stresses.append(entry[1]['stress_level'])
					health_levels.append(entry[1]['health_level'])

			mood, stress, health = get_middle_digit(moodies), get_middle_digit(stresses), get_middle_digit(health_levels)

			plt.plot(dates, moodies, label='Настроение')
			plt.plot(dates, stresses, label='Уровень стресса')
			plt.plot(dates, health_levels, label='Уровень здоровья')
			
			plt.legend(loc='upper left', frameon=False)
			plt.yticks([1, 2, 3, 4, 5])

			plt.xlabel(f'Даты')
			plt.ylabel('Значения') 
			plt.title(dates_used)

			plt.show()

		elif sys.argv[1] == 'add':
			date = get_current_date()
			print(f'[{date}] Добавление новых данных')

			try:
				mood = int(input('Введите уровень вашего настроения (от 1 до 5): '))
				stress = int(input('Введите уровень вашего стресса (от 1 до 5): '))
				health = int(input('Введите уровень вашего физического здоровья (от 1 до 5): '))
			except ValueError:
				print('Один из полей был заполнен некорректно')
				return
			else:
				additional_data = input('Введите дополнительную информацию (Enter для пропуска): ')

				data = add_entry(date, mood, stress, health, additional_data)

				if data[0]:
					tracker.add_to_file(data[1], data[2], data[3], data[4], data[5], data[6])
					
					if len(sys.argv) > 2:
						if sys.argv[2] == 'show':
							graphics = GraphicsHealth(mood, stress, health, data[1])
							graphics.show()
				else:
					print(data[1])
	else:
		return


if __name__ == '__main__':
	main()
