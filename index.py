import os
import datetime
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta

def clear():
	os.system('cls' if os.name == 'nt' else 'clear')

def round_seconds(item):
	result = "" 
	item = str(item)
	date = item.split()[0]
	h, m, s = [item.split()[1].split(':')[0],
	item.split()[1].split(':')[1],
	str(round(float(item.split()[1].split(':')[-1])))]
	result = date + ' ' + h + ':' + m + ':' + s
	return str(result)

def parse_date(string, old_format="%Y-%m-%d %H:%M:%S", new_format="%B %Y"):
	if string != '':
		string = str(string)
		string = round_seconds(string)
		date_obj = dt.strptime(string, old_format)
		res = dt.strftime(date_obj, new_format)
		return str(res)

def mpr(apr, amount):
	return (apr / 12 / 100) * amount

def percent(value, total):
	return value / total

def monthly_interest(figures):
	monthly_interest = 0
	for i in figures:
		if i[0] > 0:
			monthly_interest += mpr(i[0], i[1])
		else:
			monthly_interest += 0
	return monthly_interest

def reduce_figures(repayment, figures, interest, balance):
	for i in figures:
		proportion = percent(i[0], balance)
		i[0] -= repayment * proportion
		i[0] += interest * proportion
	return figures

def total_balance(figures):
	total_balance = 0
	for i in figures:
		total_balance += i[0]
	return total_balance

now = dt.now()
figures = []

clear()
print("Enter balance and APR for each creditor")

while True:
	amount = float(input("How much is the balance? (£) > "))
	interest_rate = float(input("How much is the APR? (%) > "))
	figures += [[amount, interest_rate]]
	clear()
	for fig in figures:
		print("£" + str(fig[0]) + " at " + str(fig[1]) + "% APR")
	again = input("Add another creditor? Y/n > ")
	if again.lower() == "n":
		break

balance = total_balance(figures)
total_interest = 0
month = 0

repayment = float(input("How much to repay each month > "))
initial_repayment = repayment
show_breakdown = input("Show breakdown? y/N > ")
initial_balance = str(balance)
print("")
print("STARTING BALANCE: " + initial_balance)

while balance > 0:
	month +=1
	this_month = monthly_interest(figures)
	if this_month >= initial_repayment:
		print("Repayment too low - You will never clear the balance!")
		break
	figures = reduce_figures(repayment, figures, this_month, balance)
	balance = total_balance(figures)
	if balance < 0:
		repayment = round(repayment + balance, 2)
		balance = 0
	total_interest += this_month
	if show_breakdown.upper() == "Y":
		print("")
		print("Month: " + str(month))
		print("Repayment: " + str(repayment))
		print("This month's interest: " + str(round(this_month,2)))
		print("Remaining balance: " + str(round(balance,2)))

repayment_date = parse_date(now + relativedelta(months=month))

if balance == 0:
	print("")
	print("Paying " + str(initial_repayment) 
					+ " per month would repay " + initial_balance + " (and " 
					+ str(round(total_interest,2)) + " interest) by " 
					+ repayment_date + " (" + str(round(month / 12, 1)) + " years)")