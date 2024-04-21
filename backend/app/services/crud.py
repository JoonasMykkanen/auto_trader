# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    crud.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/04/21 07:55:49 by jmykkane          #+#    #+#              #
#    Updated: 2024/04/21 08:16:47 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from sqlalchemy.orm import Session

from ..core.models import WeeklyCandle
from ..core.models import DailyCandle
from ..core.models import Ticker

