# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    main.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/04/16 09:32:22 by jmykkane          #+#    #+#              #
#    Updated: 2024/04/16 16:17:51 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from fastapi import FastAPI

from .services.tor import tor_request

app = FastAPI()

url = 'https://query1.finance.yahoo.com/v7/finance/download/AAPL?period1=347155200&period2=1713267290&interval=1d&events=history&includeAdjustedClose=true'

@app.get("/")
def read_root():

	tor_request(url)
	
	# print(tor_addr2)
	return f'successfull 10 requests'
	

	# return f'1: {tor_addr1} --- 2: {tor_addr2}'