# TBG Demo (Turn Based Game Demo) 
## มีหน้าจอหลัก 3 หน้าจอ (Screens):
    1. Title Screen (เริ่มต้น)
    2. World Screen (โลก สามารถเดินได้)
    3. Battle Screen (ต่อสู้)
## มี Popup 2 อัน:
    1. Backpack (เมนูกระเป๋า)
    2. Status (สเตตัสตัวละคร)
- Title Screen: มีปุ่มเริ่มเกมเข้า World Screen, ออกเกม และปเิด/ปิดเพลง
- World Screen: สามารถควบคุมให้ตัวละครเดินได้ทีละ 1 ช่อง มีทุ่งหญ้าที่จะสุ่มการพบเจอศัตรูภายในหญ้า เมื่อพบเจอศัตรูจะเข้า Battle Screen และมีปุ่มกระเป๋า, สเตตัสตัวละคร, เซฟเกม และปุ่มออกไปหน้าจอเริ่มต้น
- Battle Screen: หน้าจอสำหรับการต่อสู้ เป็นระบบ Turn Based ผลัดกันตีทีละเทิร์น โดยมีปุ่มสกิล 4 ปุ่ม, กระเป๋า และหนีจากการต่อสู้เข้าหน้า World Screen
## มีไฟล์ Python 9 ไฟล์ในการใส่ Logic เกม:
    1. main.py (ใช้รันเกม)
    2. gamedata.py (เก็บข้อมูลตัวละครต่าง ๆ ไอเทม และสกิล)
    3. hero.py (class ในการสร้างตัวละคร)
    4. enemy.py (class ในการสร้างศัตรู)
    5. title_screen.py (หน้าจอเริ่มต้น)
    6. world_screen.py (หน้าจอโลก)
    7. battle_screen.py (หน้าจอต่อสู้)
    8. backpack.py (Popup กระเป๋า)
    9. stats.py (Popup สเตตัสตัวละคร)
## มีไฟล์ Kivy 5 ไฟล์ในการใส่ GUI ของเกม:
    1. title_screen.kv (หน้าจอเริ่มต้น)
    2. world_screen.kv (หน้าจอโลก)
    3. battle_screen.kv (หน้าจอต่อสู้)
    4. backpack.kv (Popup กระเป๋า)
    5. stats.kv (Popup สเตตัสตัวละคร)
## วิธีการใช้งาน:
    1. ติดตั้ง Kivy เปิด Command Prompt แล้วพิมพ์ 
    ```bash 
    pip install kivy
    <!-- pip install kivy ``` -->
    2. รันเกม main.py 
    ```bash 
    python main.py 
    ```