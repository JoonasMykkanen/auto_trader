# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    tor.py                                             :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/04/16 15:45:27 by jmykkane          #+#    #+#              #
#    Updated: 2024/04/20 06:22:21 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# This module will contain logic to route requests trough tor proxies
# Tor is designed to be ran on a different container exposing ports 9050 and 9051

from stem.control import Controller
from stem import Signal
import requests
import socket
import random

agents = [
	'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
	'Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Mobile/15E148 Safari/604.1',
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134',
	'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36 OPR/66.0.3515.27',
	'Mozilla/5.0 (Linux; Android 10; SM-A205U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Mobile Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Safari/605.1.15',
	'Mozilla/5.0 (Linux; Android 10; SM-A205U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
]

def generate_agent():
	return agents[random.randint(0, 9)] 


def renew_ip():
	""" Sends signal to local tor binary to renew ip and identity \n\n Parameters: None \n\n Returns: None"""
	ip = socket.gethostbyname('tor')
	with Controller.from_port(address=ip, port=9051) as controller:
		controller.authenticate(password="password")
		controller.signal(Signal.NEWNYM)


def tor_request( url: str ):
	""" Makes a request trough tor proxy \n\n Parameters: None \n\n Returns: (response) object"""
	session = requests.session()
	session.proxies = { 'http': 'socks5h://tor:9050', 'https': 'socks5h://tor:9050' }
	headers = { 'User-Agent': f'{generate_agent()}' }
	response = session.get(url, headers=headers)
	return response
