import requests
import os

class Mintos:

	def __init__(self, iso_code, token=None):
		if token is None:
			if os.getenv('MINTOS_TOKEN') is not None:
				self.token = os.getenv('MINTOS_TOKEN')
			else: 
				print('No token provided. Exiting')
				exit()
		else: self.token = token
			
		self.currency_iso_code = iso_code
		self.data = self.get(iso_code)['data']

	
	def get(self, currency_iso_code):
		cookies = {
			'PHPSESSID': self.token,
		}
		headers = {
			'X-Requested-With': 'XMLHttpRequest',
		}
		params = (
			('currencyIsoCode', currency_iso_code),
		)
		response = requests.get('https://www.mintos.com/en/overview-aggregates', headers=headers, params=params, cookies=cookies)
		response.raise_for_status()
		return response.json()

	def get_net_annual_returns(self):
		return self.data['netAnnualReturns'][self.currency_iso_code]
	def get_investments(self):
		return self.data['investmentData'][self.currency_iso_code]
	def get_pending_payments(self):
		return self.data['pendingPayments'][self.currency_iso_code]

if __name__ == '__main__':
	from pprint import pprint
	
	import sys
	
	if len(sys.argv) == 3 and sys.argv[1] == '--iso-code' and len(sys.argv[2]) == 3:
		iso_code =  sys.argv[2]
	else:
		iso_code = '978' #Default EUR
	m = Mintos(iso_code=iso_code)
	investments = m.get_investments()
	from termcolor import colored

	print(colored(' Mintos overview\n', 'cyan'))

	print('\033[1m', '>>> Current investment data:', '\033[0m')
	for inv in investments:
		loop = len(max(investments, key=len)) - len(inv)
		print('\t>>>', colored(inv, 'blue'), ' ' * loop + '-',  round(float(investments[inv]), 2) if '.' in str(investments[inv]) else investments[inv])

	pending = round(float(m.get_pending_payments()),2)
	print('\033[1m', colored('>>> Pending payments for eur:', 'yellow'), pending)
