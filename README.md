# AI spēle 7. grupa

### Spēles apraksts
Spēles sākumā ir dots cilvēka-spēlētāja izvēlētais skaitlis diapazonā no 20 līdz 30. Kopīgs punktu skaits ir vienāds ar 0 (punkti netiek skaitīti katram spēlētājam atsevišķi). Turklāt spēlē tiek izmantota spēles banka, kura sākotnēji ir vienāda ar 0. Spēlētāji veic gājienus pēc kārtas, reizinot pašreizējā brīdī esošu skaitli ar 3, 4 vai 5. Ja reizināšanas rezultātā tiek iegūts pāra skaitlis, tad kopīgajam punktu skaitam tiek pieskaitīts 1 punkts, bet ja nepāra skaitlis – tad 1 punkts tiek atņemts. Savukārt, ja tiek iegūts skaitlis, kas beidzas ar 0 vai 5, tad bankai tiek pieskaitīts 1 punkts. Spēle beidzas, kad ir iegūts skaitlis, kas ir lielāks par vai vienāds ar 3000. Ja kopīgais punktu skaits ir pāra skaitlis, tad no tā atņem bankā uzkrātos punktus. Ja tas ir nepāra skaitlis, tad tam pieskaita bankā uzkrātos punktus. Ja kopīgā punktu skaita gala vērtība ir pāra skaitlis, uzvar spēlētājs, kas uzsāka spēli. Ja nepāra skaitlis, tad otrais spēlētājs.

### Demo
Ja ir Replit konts, var paspēlēties te: https://replit.com/@jbolozdina/MiPamati

### Lokāla palaišana
#### Dependencies
* Python: >=3.10.0,<3.12
* Typing module (iebūvēts)
#### Instrukcija
1. ```git clone <šis_repo.git>```
2. ```py main.py```
