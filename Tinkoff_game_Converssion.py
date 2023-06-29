# -*- coding: utf-8 -*-
"""
# Подключение библиотек
"""

import psycopg2
import pandas as pd
from plotly.graph_objs import layout
import plotly.graph_objects as go
from matplotlib import legend
from plotly.subplots import make_subplots

"""# Подключение к БД"""

from sqlalchemy import create_engine
engine = create_engine(
    "postgresql://login:password@localhost_adress:port/postgres",
)

sql_month = """select
((to_char(visit_dttm, 'Mon ') || to_char(visit_dttm, 'YYYY')) ) as name_month,
date_trunc('month',visit_dttm)as d_month,
count(distinct c.client_rk) as site_user,
count(distinct a.account_rk) as account_user,
count(distinct a2.account_rk)  as book_user,
count(distinct a2.account_rk) FILTER(WHERE g.game_flg = 1) as player_user
FROM msu_analytics.client c
left join msu_analytics.account a on c.client_rk =a.client_rk
left join msu_analytics.application a2 on a.account_rk =a2.account_rk
left join msu_analytics.game g on a2.game_rk  = g.game_rk
group by name_month, d_month
order by 2"""
dm = pd.read_sql(sql_month,engine,) # динамика по месяцам

sql_week = """select
to_char(visit_dttm, 'IW') as num_week,--|| ' week ' ||to_char(visit_dttm, 'YYYY')) ) as num_week,
date_trunc('week',visit_dttm) as d_week,
(case EXTRACT(week from visit_dttm)
	when 1 then (EXTRACT(week from visit_dttm)+52)
	when 2 then (EXTRACT(week from visit_dttm)+52)
	when 3 then (EXTRACT(week from visit_dttm)+52)
	when 4 then (EXTRACT(week from visit_dttm)+52)
	when 5 then (EXTRACT(week from visit_dttm)+52)
    else EXTRACT(week from visit_dttm)
end) as n_week,
count(distinct c.client_rk) as site_user,
count(distinct a.account_rk) as account_user,
count(distinct a2.account_rk)  as book_user,
count(distinct a2.account_rk) FILTER(WHERE g.game_flg = 1) as player_user
FROM msu_analytics.client c
left join msu_analytics.account a on c.client_rk =a.client_rk
left join msu_analytics.application a2 on a.account_rk =a2.account_rk
left join msu_analytics.game g on a2.game_rk  = g.game_rk
group by d_week, num_week, n_week
order by 3 """
dw = pd.read_sql(sql_week,engine,) # динамика по неделям
dw.head()

"""# Обработка"""

dw.info()

dm.info()

dm.fillna(0)

dw.fillna(0)

#Подсчет конверсий по неделям
dw['week_conv_1'] = round(100*dw['account_user']/dw['site_user']) #Конверсия из посещения сайта в регистрацию на сайте
dw['week_conv_2'] = round(100*dw['book_user']/dw['site_user']) #Конверсия из посещения сайта в создание заявки на игру
dw['week_conv_3'] = round(100*dw['player_user']/dw['site_user'])#Конверсия из посещения сайта в посещение игры
dw.head()

#Подсчет конверсий по месяцам
dm['month_conv_1'] = round(100*dm['account_user']/dm['site_user']) #Конверсия из посещения сайта в регистрацию на сайте
dm['month_conv_2'] = round(100*dm['book_user']/dm['site_user']) #Конверсия из посещения сайта в создание заявки на игру
dm['month_conv_3'] = round(100*dm['player_user']/dm['site_user'])#Конверсия из посещения сайта в посещение игры
dm.head()

"""Визуализация

##Динамика по месяцам
Реализация на двух подграфиках с возможностью изменить тип отображения
"""

trace_m1=go.Bar(x=dm['name_month'], y=dm['site_user'], name='Посетители сайта', text = dm['site_user'], textfont= dict(size=14),hovertemplate='<br>Месяц:%{x}<br>Количество посетителей: %{y}',hoverinfo='x+y',marker = dict(color = '#f5cb5c') )
trace_m2=go.Bar(x=dm['name_month'], y=dm['month_conv_1'], name='Конверсия из посещения сайта в регистрацию на сайте', text = dm['month_conv_1'], textfont= dict(color='white', size=12),hovertemplate='<br>Конверсия: %{y} %',hoverinfo='x+y',marker = dict(color = '#619b8a'))
trace_m3=go.Bar(x=dm['name_month'], y=dm['month_conv_2'], name='Конверсия из посещения сайта в создание заявки на игру', text = dm['month_conv_2'], textfont= dict(color='white', size=12),hovertemplate='<br>Конверсия: %{y} %',hoverinfo='x+y',marker = dict(color = '#f26419') )
trace_m4=go.Bar(x=dm['name_month'], y=dm['month_conv_3'], name='Конверсия из посещения сайта в посещение игры', text = dm['month_conv_3'], textfont= dict(color='white', size=12), hovertemplate='<br>Конверсия:%{y} % ',hoverinfo='x+y',marker = dict(color = '#233d4d') )
fig_m = make_subplots(rows=2, cols=1,  vertical_spacing=0.05)
fig_m.add_trace(trace_m1,row=1, col=1)
fig_m.add_trace(trace_m2,row=2, col=1)
fig_m.add_trace(trace_m3,row=2, col=1)
fig_m.add_trace(trace_m4,row=2, col=1)
fig_m.update_layout(plot_bgcolor='rgba(0,0,0,0)', height=600, width=1200, title_text="Динамика по месяцам" )
#fig_m.update_traces()
# Set x-axis title
fig_m.update_yaxes(row = 1, title_text="Количество посетителей, чел.", linecolor ='gray')
fig_m.update_yaxes(row = 2, title_text="Конверсия, %", linecolor ='gray')
fig_m.update_xaxes(linecolor ='gray')
# Add dropdown
fig_m.update_layout(
    updatemenus=[go.layout.Updatemenu(
        active=0,
        x = 1.18,
        xanchor = 'auto',
        y = 0.78,
        yanchor = 'auto',
        buttons=list([dict(args=["type", "bar"],label="Bar Chart",method="restyle"),dict(args=["type", "line"],label="Line Plot",method="restyle")]),direction="down")]
        )

"""Динамика по неделям
Реализация на одном графике
"""

# Create figure with secondary y-axis
fig_w = make_subplots(specs=[[{"secondary_y": True}]])

trace_w1=go.Bar(x=dw['d_week'], y=dw['site_user'], name='Посетители сайта', text = dw['site_user'], textposition = 'outside',  outsidetextfont= dict(size=12), textangle= 0, hoverinfo='x+y', hovertemplate='<br>Количество посетителей: %{y}', marker = dict(color = '#f5cb5c'))
trace_w2=go.Scatter(x=dw['d_week'],y=dw['week_conv_1'], name='Конверсия из посещения сайта в регистрацию на сайте', hoverinfo='x+y', hovertemplate='<br>Конверсия: %{y} %',line=dict(color="#619b8a"))
trace_w3=go.Scatter(x=dw['d_week'],y=dw['week_conv_2'], name='Конверсия из посещения сайта в создание заявки на игру', hoverinfo='x+y', hovertemplate='<br>Конверсия: %{y} %',line=dict(color="#f26419"))
trace_w4=go.Scatter(x=dw['d_week'],y=dw['week_conv_3'], name='Конверсия из посещения сайта в посещение игры', hoverinfo='x+y', hovertemplate='<br>Конверсия: %{y} %', line=dict(color="#233d4d"))

# Add traces
fig_w.add_trace(trace_w1,secondary_y=False,)
fig_w.add_trace(trace_w2,secondary_y=True,)
fig_w.add_trace(trace_w3,secondary_y=True,)
fig_w.add_trace(trace_w4,secondary_y=True,)

# Add figure title
fig_w.update_layout(hovermode='x unified', plot_bgcolor='rgba(0,0,0,0)', height=400, width=1250, title_text="Динамика по неделям" )
# Set x-axis title
fig_w.update_xaxes(tickangle = -70)

# Set y-axes titles
fig_w.update_yaxes(title_text="Количество посетителей, чел.", secondary_y=False, linecolor ='gray' , range = [0,220])
fig_w.update_yaxes(title_text="Конверсия, %", secondary_y=True, linecolor ='gray', range = [0,45])
fig_w.update_xaxes(linecolor ='gray')

"""Вывод одновременно динамики по месяца и неделям для наглядного анализа"""
fig_m.show()
fig_w.show()

"""Вывод

---
Динамика по месяцам:
* По сравнению с октябрем произошло резкое уменьшение количества посетителей сайта. Возможная проблема может заключается в ухудшении рекламы сервиса либо доступности сайта.
* Количество уникальных посетителй сайта с ноября растет
* Доля зарегистрировавшихся клиентов усредненно стабильная 25 % в динамике по месяцам
* Доля клиентов, резервирующих хотя бы одну одну игру после посещения сайта в динамике по месяцам составляет 7-8 процентов
* В динамике по месяцам с ноября наблюдается прогрессирующее снижение доли клиентов, посетивших игру.
* В январе конверсия посещения игр составляет всего 2%. Возможно данное явление обусловлено праздничными днями.


Динамика по неделям:
* В ноябре и со второй половины января количество посетилей сайта заметно ниже показателей по другим неделям.
* С конца ноября демонстрирует устойчивый тренд на снижение конверсия по посетителям, пришедшим на игру. При этом конверсия по зарезервировавшим игру не имеет такого резкого и устойчивого тренда.
* В третью неделю ноября наблюдается заметное снижение по всем этапам вороки. Необходимо проверить, что было могло послужить препятсвием со технической стороны (смена интерфеса, плохая работа серевера, сбой в работе сайта и т.д)
* В первую неделю января выросло количество посетителей сайта, увеличилась доля зарегистрировавшихся клинетов, и даже несколько подрасла доля клиентов, зарезервировавших игру, но корнверсия по пришедшим на игру упала до 2 %.
* Визуализируется резкое снижение доли клиентов, производивших резервирование и посещение игр в последнюю неделю декабря. Что, вероятнее, всего обусловлено праздничными днями.   

---
Точки роста продукта

* Для увеличения доли клиентов, зарезервировавших игру, необходимо убедиться в удобстве навигации, улучшить/наполнить "карточки товара" на сайте (или в приложении), ввести систему выгод для клиента (поощерение за создание пользовательского контента — обзоров и отзывов).
* Для устранения проблемы "забывчивости" необходимо улучшить процесс напоминания о дате и времени игры, увеличить стимул к реальному посещению."""