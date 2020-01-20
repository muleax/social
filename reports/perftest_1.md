###Конфигруация стенда
 Docker запущен на MacbookPro, с лимитами CPUs: 6, Memory: 8 Gb

###Конфигруация сервера
nginx -- gunicorn -- mysql
- nginx: сконфигурирован как reverse-proxy, 1 воркер
- gunicorn: 4 воркера aiohttp.GunicornWebWorker
    
Для теста сгенерировано 8'000'000 аккаунтов со случайной информацией
 ```
user_id, first_name, last_name, city, birth_date, json_data 
```

Тестрование производилось инструментом [vegeta](https://github.com/tsenart/vegeta).

База без индексов, keepalive=true, RPS=1
```
Requests      [total, rate, throughput]  60, 1.02, 0.96
Duration      [total, attack, wait]      1m2.557205488s, 58.999619052s, 3.557586436s
Latencies     [mean, 50, 95, 99, max]    3.136964188s, 3.646988038s, 3.863441744s, 3.960404015s, 3.963545459s
Bytes In      [total, mean]              12630, 210.50
Bytes Out     [total, mean]              0, 0.00
Success       [ratio]                    100.00%
Status Codes  [code:count]               200:60  
```
![alt text](get_noindex_ka_1rps.png)
Уже на такой нагрузке слишком высокий latency.
Во время теста mysql брала 300-400% CPU, остальные контейнеры не потели.
Без индексов все очень плохо.  

Попробуем RPS=2
```
Requests      [total, rate, throughput]  120, 2.02, 0.57
Duration      [total, attack, wait]      1m26.137156396s, 59.498986148s, 26.638170248s
Latencies     [mean, 50, 95, 99, max]    18.721706703s, 19.824769474s, 30.004457832s, 30.005038029s, 30.005078046s
Bytes In      [total, mean]              12529, 104.41
Bytes Out     [total, mean]              0, 0.00
Success       [ratio]                    40.83%
Status Codes  [code:count]               0:45  200:49  502:26  
```
![alt text](get_noindex_ka_2rps.png)
mysql брала ~420% CPU, похоже, это максимум, который способен выдать докер в такой конфигурации.
Throughput ухудшился, потому что часть запросов отваливалась по таймауту.


[test](../client/index.html).
