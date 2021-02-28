# Новейшая разработка: Write-up

Архив содержит исходный код программы [kafkacat](https://github.com/edenhill/kafkacat) и директорию .git со всей историей разработки. Её изучение не даёт ничего интересного — она в точности совпадает с публичной историей на Гитхабе. Проверим, нет ли в репозитории каких-нибудь неучтённых объектов, выполнив команду `git fsck`:

```
$ git fsck
Checking object directories: 100% (256/256), done.
Checking objects: 100% (1347/1347), done.
dangling commit 4693d471cb035704931d4d28f70b999dd158f4fb
```

Посмотрим содержимое коммита:

```diff
$ git show 4693d471cb035704931d4d28f70b999dd158f4fb
commit 4693d471cb035704931d4d28f70b999dd158f4fb
Author: Validian <validian@validian.name>
Date:   Wed Dec 11 06:00:30 2019 +0845

    added info.txt.

diff --git a/info.txt b/info.txt
new file mode 100644
index 0000000..0a70bb9
--- /dev/null
+++ b/info.txt
@@ -0,0 +1,7 @@
+If you are reading this, I am definitely dead by now.
+
+I also know that by reaching this file, you have demonstrated
+the best of your ability and courage. Here is the key to my
+lifetime secret: ugra_the_yellow_purse_bfc187edca9a70c8
+
+You will understand what to do next. Good luck!
```

Взгрустнув о тяжёлой судьбе никогда не существовавшего разработчика, сдаём флаг.

Флаг: **ugra_the_yellow_purse_bfc187edca9a70c8**
