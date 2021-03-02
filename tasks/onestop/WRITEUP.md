# Служба одного порта: Write-up

Таск о скрытии нескольких сервисов за одним портом с помощью `sslh`.

## Ход решения.

Заходим на сайт службы. Видим новость, в которой сообщается, что служба открыла административный отдел. Это, а также название таска, намекает нам о возможности зайти на тот же порт по SSH. Если сделать это, мы обнаружим сообщение:

```
$ ssh ctf@onestop.q.2021.ugractf.ru -p 443
Добро пожаловать в систему одного порта, отдел административный!

Доступные также защищённые отделы: информационный, текстовый.
ctf@onestop.q.2021.ugractf.ru: Permission denied (publickey).
```

Как мы видим из описания, всего на одном порту действуют три службы: административная, информационная и текстовая. Мы уже получили доступ к двум службам из трёх; осталась лишь текстовая служба. Вместе с информационной она описывается как «защищённая», что намекает на HTTPS или TLS в принципе.

Ищем в Интернете информацию, как в принципе реализуются такие службы. Находим и открываем сайт [sslh](https://github.com/yrutschle/sslh) — наиболее популярного демона для реализации диспетчеризации по портам. Здесь в [примере конфигурации](https://github.com/yrutschle/sslh/blob/master/example.cfg) описываются различные способы диспетчеризации подключения. Смотрим на варианты диспетчеризации по TLS: используется либо SNI hostname, либо ALPN. Поскольку «отделами» в таске называются разные протоколы, логично предположить, что используется как раз ALPN. Для экспериментов можно использовать утилиту `openssl`, например: `openssl s_client -alpn example onestop.q.2021.ugractf.ru:443`.

Пробумем название сервиса `текстовый`: бинго!  Видим приглашение `PWD?`. Введя в него пароль из задания, получаем искомый флаг.

Флаг: **ugra_social_services_for_the_masses_ff76c5513401closed**