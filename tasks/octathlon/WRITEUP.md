# Восьмиборье: Write-up

Таск — стеганография в метаданных ISO.

Скачиваем образ диска. При его осмотре выясняется, что внутри ровно восемь разнообразных файлов. Вряд ли информация спрятана в каждом из них по отдельности, да и ISO-образ тут был дан неспроста. На это же намекает файл `cdrtools-source.zip`. Поэтому предплагаем, что информация сокрыта в метаданных диска.

Найти зацепку можно было несколькими способами:

* С помощью утилиты `isoinfo`:

```
$ isoinfo -f -i image.iso   
/PFPWC427.003;1
/MQ4DANDE.007;1
/L5RGKOJT.006;1
/NZXXIX3B.001;1
/OVTXEYK7.000;1
/MVSF65DP.005;1
/ONPWKYLT.002;1
/NF2F65LT.004;1
```

* С помощью утилиты `isodump`:

```
$ isodump image.iso
144 [ 1]    1c     2048 02/*.             [SP,RR=1,PX=2,TF,CE=[1e,0,237][ER]]
110 [ 1]    1c     2048 02/*..            [RR=1,PX=2,TF]
150 [ 1]    1f    73529 00/ PFPWC427.003;1[RR=1,NM=2d_rigid_bodies.ipynb,PX=1,TF]
148 [ 1]    43  2165175 00/ MQ4DANDE.007;1[RR=1,NM=big_buck_bunny.webm,PX=1,TF]
148 [ 1]   465  3796533 00/ L5RGKOJT.006;1[RR=1,NM=cdrtools-source.zip,PX=1,TF]
142 [ 1]   ba3  1162810 00/ NZXXIX3B.001;1[RR=1,NM=challenge.png,PX=1,TF]
146 [ 1]   ddb     8631 00/ OVTXEYK7.000;1[RR=1,NM=iris-dataset.xlsx,PX=1,TF]
148 [ 1]   de0   144165 00/ MVSF65DP.005;1[RR=1,NM=olympiads_order.pdf,PX=1,TF]
146 [ 1]   e27   105243 00/ ONPWKYLT.002;1[RR=1,NM=sound_example.ogg,PX=1,TF]
152 [ 1]   e5b   693170 00/ NF2F65LT.004;1[RR=1,NM=youll_need_this_too.swf,PX=1,TF]

 Zone, zone offset:     1c 0000  
```

* С помощью шестнадцатеричного редактора, просматривая таблицу файлов на диске:

![Вид таблицы](writeup/hexeditor.png)

В любом случае, можно было заметить, что сокращённые названия файлов (так называемые имена в формате 8.3) сильно отличаются от тех, которые мы видим на диске. Эти названия также можно увидеть, смонтировав образ специальным образом: `mount -o norock,nojoliet image.iso /mnt/image`.

Названия файлов представляют собой флаг, закодированный в base32, а числа в расширении намекают на порядок. Обнаружить используемый алгоритм можно, например, с помощью [CyberChef](https://gchq.github.io/CyberChef/#recipe=Magic%283%2Cfalse%2Cfalse%2C%27%27%29&input=T1ZUWEVZSzdOWlhYSVgzQk9OUFdLWUxUUEZQV0M0MjdORjJGNjVMVE1WU0Y2NURQTDVSR0tPSlRNUTREQU5ERQ). В нём есть рецепт Magic, автоматически ищущий кодировку на основе энтропии. Подробнее об этом можно почитать [в нашем курсе](https://course.ugractf.ru/crypto/codes.html).

Флаг: **ugra_not_as_easy_as_it_used_to_be93d804d**
