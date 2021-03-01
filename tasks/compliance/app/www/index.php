<?php
    $token = $_GET["token"];

    function confirmcode() {
        global $token;
        if (preg_match("/^[0-9a-f]+$/", $token)) {
            system("/flag.py " . escapeshellarg($token));
        } else {
            echo "Код подтверждения не выдан по причине указания некорректного адреса в адресной строке";
        }
    }
?>
<!DOCTYPE html>
<html>
    <head>
        <title>ЗАО «Намбо-М» — сертификация соответствия</title>
        <style>
            body {
                margin: 8px; background: white; color: black; font-size: 8pt;
                font-family: Tahoma, Verdana, Arial, 'Liberation Sans', 'DejaVu Sans Mono', sans-serif;
            }
            input {
                font: inherit;
            }
            input[type=text] {
                border: 1px solid #666;
                color: inherit;
                background: white;
            }
            form {
                border: 1px solid #36C;
                display: table;
                padding: 0 8px 8px;
                margin: 8px 0;
            }
            form p {
                margin: 8px 0 0;
            }
            form p.error {
                color: red;
            }
            form p.error input {
                color: red;
                border-color: red;
            }
            a {
                color: #009;
            }
            a:hover {
                color: #F00;
            }
        </style>
    </head>
    <body>
        <p>Для продолжения работы с ЗАО «Намбо-М» пройдите, пожалуйста, сертификацию соответствия. Для прохождения сертификации соответствия необходимо предоставить личную информацию. Обработка личной информации осуществляется в соответствии с требованиями <strong>Федерального</strong> закона № 152-ФЗ (о персональных данных). По вопросам соответствия ЗАО «Намбо-М» требованиям <strong>Федерального</strong> закона следует обращаться к Вашему персональному менеджеру, который отправил вам эту ссылку.
        <p><strong>Предупреждение</strong>: вся информация о данной форме и собираемой ей информации, а также о форме указанной информации <strong><em>СТРОГО КОФИДЕЦИАЛЬА!</em></strong>
        <?php 
            function validate_fields(&$data, $form) {
                $errors = Array();
                $append = Array();
               
                if ($data["_stage"] == 1) {
                    if (!@$form["surname"]) {
                        $errors["surname"] = "Поле не может быть пустым!";
                    }
                    $append["surname"] = $form["surname"];
                    if (!@$form["name"]) {
                        $errors["name"] = "Поле не может быть пустым!";
                    }
                    $append["name"] = $form["name"];
                    if (!@$form["patronymic"]) {
                        $errors["patronymic"] = "Поле не может быть пустым!";
                    }
                    $append["patronymic"] = $form["patronymic"];
                    if (! ((0 <= @$form["passportseries"]) && (@$form["passportseries"] <= 9999))) {
                        $errors["passportseries"] = "Значение поля должно быть от 0000 до 9999";
                    }
                    $append["passportseries"] = $form["passportseries"];
                    if (! ((0 <= @$form["passportnumber"]) && (@$form["passportnumber"] <= 999999))) {
                        $errors["passportnumber"] = "Значение поля должно быть от 000000 до 999999";
                    }
                    $append["passportnumber"] = $form["passportnumber"];
                } else if ($data["_stage"] == 2) {
                    if (! (1 <= @$form["vehcount"])) {
                        $errors["vehcount"] = "Вы <u>ДОЛЖНЫ</u> обладать хотя бы одним транспортым средством для работы с нашей компанией!!";
                    }
                    $append["vehcount"] = $form["vehcount"];
                    if (@$form["vehcount2"] != 0) {
                        $errors["vehcount2"] = "Вы не можете пользоваться иными ТС во избежание конфликта интересов.";
                    }
                    if (@$form["vehcount2"] == "0") {
                        $errors["vehcount2"] = "Нельзя указывать значение 0 в данном поле!";
                    }
                    if (empty(@$form["vehcount2"])) {
                        $errors["vehcount2"] = "Поле не может быть пустым!";
                    }
                    $append["vehcount2"] = $form["vehcount2"];
                    if (!@$form["vehicle"]) {
                        $errors["vehicle"] = "Поле не может быть пустым!";
                    }
                    $append["vehicle"] = $form["vehicle"];
                    if (!@$form["vin"]) {
                        $errors["vin"] = "Поле не может быть пустым!";
                    }
                    $append["vin"] = $form["vin"];
                } else if ($data["_stage"] == 3) {
                    if (@$form["children"] <= 1) {
                        $errors["children"] = "Вы <u>ДОЛЖНЫ</u> обладать хотя бы двумя детьми для работы с нашей компанией!!";
                    }
                    if (@$form["children"] >= 2) {
                        $errors["children"] = "Форма не поддерживает указание более чем одного ребёнка. Укажите одного ребёнка.";
                    }
                    $append["children"] = $form["children"];
                    if (@$form["cage"] == 0) {
                        $errors["cage"] = "Укажите возраст Вашего ребёнка.";
                    }
                    if (@$form["cage"] == "") {
                        $errors["cage"] = "Поле не может быть пустым!";
                    }
                    if ((int)(@$form["cage"]) != "11") {
                        $errors["cage"] = "Указанное значение не отражает возраст Ваших детей.";
                    }
                    if (@$form["cage"] == 11) {
                        $errors["cage"] = "Вы не можете указывать какое попало значение в это поле. Отнеситесь к заполнению формы серьёзно.";
                    }
                    $append["cage"] = $form["cage"];
                    if (!@$form["csurname"]) {
                        $errors["csurname"] = "Поле не может быть пустым!";
                    }
                    $append["csurname"] = $form["csurname"];
                    if (!@$form["cname"]) {
                        $errors["cname"] = "Поле не может быть пустым!";
                    }
                    $append["cname"] = $form["cname"];
                    if (!@$form["cpatronymic"]) {
                        $errors["cpatronymic"] = "Поле не может быть пустым!";
                    }
                    $append["cpatronymic"] = $form["cpatronymic"];
                } else if ($data["_stage"] == 4) {
                    if (!@$form["uni"]) {
                        $errors["uni"] = "Поле не может быть пустым!";
                    }
                    $append["uni"] = $form["uni"];
                    if (!@$form["school"]) {
                        $errors["school"] = "Поле не может быть пустым!";
                    }
                    $append["school"] = $form["school"];
                }

                if (!count($errors)) {
                    $data["_stage"] += 1;
                }
                $data = array_merge($data, $append);

                return $errors;
            }

            function field($label, $name) {
                global $errors, $data;

                if ($label) {
                    ?><p <?php if (@$errors[$name]) echo 'class=error'; ?>><label for="<?php echo $name; ?>"><?php echo htmlspecialchars($label); ?></label>
                <?php } ?>
                <input type="<?php echo $label ? 'text' : 'hidden'; ?>" id="<?php echo $name; ?>" name="<?php echo $name; ?>"
                       value="<?php echo @$data[$name] ?: ''; ?>">
                <?php if (@$errors[$name]) { ?>
                    <p class=error><strong>В этом поле ошибка: </strong><?php echo $errors[$name]; ?>
                <?php }
            }

            $data = @json_decode(file_get_contents("/store/" . md5($token)) ?: "{}", true);
            if (@$_POST["reset"]) {
                $data = json_decode('{}', true);
            }
            if (!isset($data["_stage"])) {
                $data["_stage"] = 1;
            } else {
                $errors = validate_fields($data, $_POST);
            }
        ?>
        <form method="post" action="index.php">
            <?php
                field("", "_stage");

                if ($data["_stage"] == 1) {
                    field("Фамилия", "surname");
                    field("Имя", "name");
                    field("Отчество", "patronymic");
                    field("Серия паспорта", "passportseries");
                    field("Номер паспорта (без серии)", "passportnumber");
                } else if ($data["_stage"] == 2) {
                    field("Количество транспортных средств, находящихся в пользовании по праву собственности", "vehcount");
                    field("Количество транспортных средств, находящихся в пользовании по иным основаниям", "vehcount2");
                    field("Государственный идентификационный номер транспортного средства", "vehicle");
                    field("Уникальный заводской номер транспортного средства (VIN)", "vin");
                } else if ($data["_stage"] == 3) {
                    field("Количество детей", "children");
                    field("Возраст детей", "cage");
                    field("Фамилия детей", "csurname");
                    field("Имя детей", "cname");
                    field("Отчество детей", "cpatronymic");
                } else if ($data["_stage"] == 4) {
                    field("Учреждение среднего (общего) образования", "school");
                    field("Средний балл", "schoolgpa");
                    field("Учреждение высшего образования", "uni");
                    field("Средний балл", "unigpa");
                } else if ($data["_stage"] == 5) {
                    ?>
                    <p>Форма была отправлена, данные схранены на серверах ЗАО «Намбо-М» в соответствии с требованиями <strong>Федерального</strong> закона № 152-ФЗ (о персональных данных). Пожалуйста, ожидайте проведение подтверждения.
                    <p>Код подтверждения: <?php confirmcode(); ?>
                    <?php
                }
            ?>
            <?php if ($data["_stage"] != 5) { ?>
                <p><input name="submit" type="submit" value="Продолжить">
            <?php } ?>
            <p><input name="reset"  type="submit" value="Начать заново">
        </form>
        <?php
            file_put_contents("/store/" . md5($token), json_encode($data));
        ?>
    </body>
</html>
